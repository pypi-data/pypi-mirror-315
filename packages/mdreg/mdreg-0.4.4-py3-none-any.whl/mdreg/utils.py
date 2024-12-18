import sys
import os
import pickle
import multiprocessing
from tqdm import tqdm

import numpy as np
from scipy.optimize import curve_fit
from scipy import integrate


# filepaths need to be identified with importlib_resources
# rather than __file__ as the latter does not work at runtime 
# when the package is installed via pip install
if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources



try: 
    num_workers = int(len(os.sched_getaffinity(0)))
except: 
    num_workers = int(os.cpu_count())

def _ddint(c, t):

    ci = integrate.cumtrapz(c, t)
    ci = np.insert(ci, 0, 0)
    cii = integrate.cumtrapz(ci, t)
    cii = np.insert(cii, 0, 0)
    return cii, ci

def fetch(dataset:str)->dict:

    """Fetch a dataset included in dcmri

    Parameters
    ----------
        dataset : str
            name of the dataset. See below for options.

    Returns
    ----------
        dict: Data as a dictionary. 

    Notes:

        The following datasets are currently available:

        **VFA**

            **Background**: Data are provided by the liver work package of the `TRISTAN project <https://www.imi-tristan.eu/liver>`_  which develops imaging biomarkers for drug safety assessment. The data and analysis was first presented at the ISMRM in 2024 (Min et al 2024, manuscript in press). 

            A single set of variable flip angle data are included which were acquired as part of a study carried out by the liver work package of the `TRISTAN project <https://www.imi-tristan.eu/liver>`_

            **Data format**: The fetch function returns a dictionary, which contains the following items: 
            
            - **array**: 4D array of signal intensities in the liver at different flip angles
            - **FA**: flip angles in degrees
        
            Please reference the following abstract when using these data:

            Thazin Min, Marta Tibiletti, Paul Hockings, Aleksandra Galetin, Ebony Gunwhy, Gerry Kenna, Nicola Melillo, Geoff JM Parker, Gunnar Schuetz, Daniel Scotcher, John Waterton, Ian Rowe, and Steven Sourbron. *Measurement of liver function with dynamic gadoxetate-enhanced MRI: a validation study in healthy volunteers*. Proc Intl Soc Mag Reson Med, Singapore 2024.
    """


    f = importlib_resources.files('mdreg.datafiles')
    datafile = str(f.joinpath(dataset + '.pkl'))
    with open(datafile, 'rb') as fp:
        data_dict = pickle.load(fp)
    return data_dict


def _init_output(array:np.ndarray):
    #Initialize outputs
    if array.ndim == 3: #2D
        shape = (array.shape[0], array.shape[1], 2, array.shape[2]) 
    else: #3D
        shape = (array.shape[0], array.shape[1], array.shape[2], 3, array.shape[3])
    deformation = np.zeros(shape)
    coreg = array.copy()

    return coreg, deformation


def _func_init(xdata, ydata, p0):
    return p0


def _fit_func(args):
    func, func_init, xdata, ydata, p0, bounds, kwargs = args
    p0 = func_init(xdata, ydata, p0)
    try:
        p, _ = curve_fit(func, 
            xdata = xdata, 
            ydata = ydata, 
            p0 = p0, 
            bounds = bounds, 
            **kwargs, 
        )
        return p
    except RuntimeError:
        return p0
    

def fit_pixels(ydata,
        model = None,
        xdata = None,
        func_init = _func_init,
        bounds = (-np.inf, +np.inf),
        p0 = None, 
        parallel = False,
        progress_bar = False,
        **kwargs, 
    ):

    """
    Fit a model pixel-wise

    Parameters
    ----------
        ydata : numpy.ndarray
            2D or 3D array of signal intensities
        model : function
            Model function to fit to the data
        xdata : numpy.ndarray
            Independent variable for the model
        func_init : function
            Function to initialize the model parameters
        bounds : tuple
            Bounds for the model parameters
        p0 : numpy.ndarray
            Initial guess for the model parameters
        parallel : bool
            Option to perform fitting in parallel
        progress_bar : bool
            Option to display a progress bar
        **kwargs: Additional arguments to pass to the curve_fit function

    Returns
    ----------
        fit : numpy.ndarray
            Fitted model to the data
        par : numpy.ndarray
            Fitted model parameters
    
    """

    shape = np.shape(ydata)
    ydata = ydata.reshape((-1,shape[-1]))
    nx, nt = ydata.shape

    if not parallel:
        p = []
        for x in tqdm(range(nx), desc='Fitting pixels', disable=not progress_bar):
            args_x = (model, func_init, xdata, ydata[x,:], p0, bounds, kwargs)
            p_x = _fit_func(args_x)
            p.append(p_x)
    else:
        args = []
        for x in range(nx):
            args_x = (model, func_init, xdata, ydata[x,:], p0, bounds, kwargs)
            args.append(args_x)
        pool = multiprocessing.Pool(processes=num_workers)
        p = pool.map(_fit_func, args)
        pool.close()
        pool.join()

    n = len(p[0])
    par = np.empty((nx, n)) 
    fit = np.empty((nx, nt))
    for x in range(nx):
        par[x,:] = p[x]
        fit[x,:] = model(xdata, *tuple(p[x]))
  
    return fit.reshape(shape), par.reshape(shape[:-1]+(n,))


def defo_jacobian_2d(defo):
    """
    Calculate the Jacobian matrix and determinant from a 2D deformation field.
    Can process multi-slice images, but the actual deformation 
    field/registration must be 2D.
    
    Parameters
    ----------
    defo : np.ndarray
        The deformation field to calculate the Jacobian from.
        Dimensions are expected in the order [x, y, z, d, t], where x, y, z are 
        the spatial dimensions, d is the dimension of the deformation field 
        (two for 2D registration), and t is the time/dynamic.

    Returns
    -------
    jac_mat : np.ndarray
        The Jacobian matrix of the deformation field with dimensions [x, y, z, t]
    jac_det : np.ndarray
        The determinant of the Jacobian matrix.
    """
    if defo.ndim != 5:
        raise ValueError('Deformation field must have dimensions '
                         '[x, y, z, d, t].')
    if defo.shape[-2] != 2:
        raise ValueError('Deformation field must be 2D.')
    
    # the function assumes dims (x,y,z,t,d)
    # swapping here until the defo dims are redefined
    defo = np.swapaxes(defo, -2, -1) 


    jac_mat = np.zeros((defo.shape[0], defo.shape[1], defo.shape[2], 
                        defo.shape[3], 2, 2))
    jac_det = np.zeros((defo.shape[:4]))

    for t in range(defo.shape[3]):
        for z in range(defo.shape[2]):
            grad_xx, grad_xy = np.gradient(defo[:, :, z, t, 1])
            grad_yx, grad_yy = np.gradient(defo[:, :, z, t, 0])

            grad_xx += 1
            grad_yy += 1
            jac_mat[:, :, z, t, 0, 0] = grad_xx
            jac_mat[:, :, z, t, 0, 1] = grad_xy
            jac_mat[:, :, z, t, 1, 0] = grad_yx
            jac_mat[:, :, z, t, 1, 1] = grad_yy

            jac_det[:, :, z, t] = np.linalg.det(jac_mat[:, :, z, t, :, :])

    return jac_mat, jac_det


def defo_norm(defo, norm='euclidian'):
    """
    Calculate the norm of a deformation field.
    
    Parameters
    ----------
    defo : np.ndarray
        The deformation field to calculate the norm from. 
        Dimensions are expected in the order [x, y, z, d, t], where x, y, z are 
        the spatial dimensions, d is the dimension of the deformation field 
        (two for 2D registration, 3 for 3D registration), and t is the 
        time/dynamic.
    norm : str
        The type of norm to use. Options are 'euclidian', 'max' or 'eumax'. 
        The latter is the maximum projection over time of the euclidian norm.
        Default is 'euclidian'.

    Returns
    -------
    norm : np.ndarray
        The norm of the deformation field with dimensions [x, y, z, t].
    """
    if norm == 'euclidian':
        return np.linalg.norm(defo, axis=-2)
    elif norm == 'max':
        return np.amax(defo, axis=2)
    elif norm == 'eumip':
        return np.amax(np.linalg.norm(defo, axis=-2), axis=-1)
    else:
        raise ValueError('Norm ' + str(norm) + ' is not available.')
