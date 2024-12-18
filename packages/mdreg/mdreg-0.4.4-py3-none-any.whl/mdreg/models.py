
import numpy as np
from tqdm import tqdm
from mdreg import utils

    


def constant(signal, **kwargs):

    """
    Constant model fit

    Parameters
    ----------
    
    signal : numpy.ndarray 
            Signal data.
            Spatial array with signal intensities over an additional temporal 
            dimension.

    **kwargs :
            Additional keyword arguments
    
    Returns
    -------

    fit : numpy.ndarray
        Fitted data.

    par : numpy.ndarray
        The parameters of the fitted signal model.
        The parameters are: S0, giving N=1.

    """

    shape = np.shape(signal)
    avr = np.mean(signal, axis=-1) 
    par = avr.reshape(shape[:-1] + (1,))
    fit = np.repeat(avr[...,np.newaxis], shape[-1], axis=-1)
    return fit, par



def _exp_decay_func(t, S, T):
    return S*np.exp(-t/T)

def _exp_decay_func_init(t, signal, init):
    S0 = np.amax([np.amax(signal),0])
    return [S0*init[0], init[1]]
    
def exp_decay(signal,
        time = None,
        bounds = (
            [0,0],
            [np.inf, np.inf], 
        ),
        p0 = [1,1], 
        parallel = False,
        **kwargs):
    
    """
    Exponential decay model fit

    Parameters
    ----------
        signal : numpy.ndarray
            Signal data 
            Spatial array with signal intensities over a temporal dimension.
        time : numpy.ndarray
            Timepoints of the signal data
        bounds : tuple
            Bounds for the fit
        p0 : list
            Initial parameters
        parallel : bool
            Use parallel processing
        **kwargs :
            Additional keyword arguments
    
    Returns
    -------
    fit : numpy.ndarray
        Fitted data.
    
    par : numpy.ndarray
        The parameters of the fitted signal model.
        The parameters are: S0, T, giving N=2.

    """
    
    if time is None:
        raise ValueError('time is a required argument.')
    
    return utils.fit_pixels(signal,
        model = _exp_decay_func, 
        xdata = np.array(time),
        func_init = _exp_decay_func_init,
        bounds = bounds,
        p0 = p0, 
        parallel = parallel,
        **kwargs)



def _abs_exp_recovery_2p_func(t, S0, T1):
    return np.abs(S0 * (1 - 2 * np.exp(-t/T1)))

def _abs_exp_recovery_2p_func_init(t, signal, init):
    S0 = np.amax(np.abs(signal))
    return [S0*init[0], init[1]]

def abs_exp_recovery_2p(signal, 
        TI = None,
        bounds = (
            [0,0],
            [np.inf, np.inf], 
        ),
        p0 = [1,1.3], 
        parallel = False,
        **kwargs):
    
    """
    2-parameter absolute exponential recovery model fit

    Parameters
    ----------
        signal : numpy.ndarray
            Signal data 
            Spatial array with signal intensities over different 
            inversion times.
        TI : numpy.array
            Inversion times
        bounds : tuple
            Bounds for the fit
        p0 : list
            Initial parameters
        parallel : bool
            Use parallel processing
        **kwargs :
            Additional keyword arguments
    
    Returns
    -------
    fit : numpy.ndarray
        Fitted data.
    par : numpy.ndarray
        Parameters. 
        The parameters are: S0, T1, giving N=2.
        
    """
    
    if TI is None:
        raise ValueError('TI is a required parameter.')
    
    return utils.fit_pixels(signal, 
        model=_abs_exp_recovery_2p_func, 
        xdata = np.array(TI),
        func_init = _abs_exp_recovery_2p_func_init,
        bounds = bounds,
        p0 = p0, 
        parallel = parallel,
        **kwargs)



def _exp_recovery_2p_func(t, S0, T1):
    return S0 * (1 - 2 * np.exp(-t/T1))

def _exp_recovery_2p_func_init(t, signal, init):
    S0 = np.amax(np.abs(signal))
    return [S0*init[0], init[1]]

def exp_recovery_2p(signal, 
        TI = None,
        bounds = (
            [0,0],
            [np.inf, np.inf], 
        ),
        p0 = [1,1.3], 
        parallel = False,
        **kwargs):
    
    """
    2-parameter exponential recovery model fit
    
    Parameters
    ----------
        signal : numpy.ndarray
            Signal data 
            Spatial array with signal intensities over different 
            inversion times.
        TI : numpy.array
            Inversion times
        bounds : tuple
            Bounds for the fit
        p0 : list
            Initial parameters
        parallel : bool
            Use parallel processing
        **kwargs :
            Additional keyword arguments
    
    Returns
    -------
        fit : numpy.ndarray
            Fitted data
            
        par : numpy.ndarray
            Parameters
            The parameters are: S0, T1, giving N=2.
        
    """
    
    if TI is None:
        raise ValueError('TI is a required parameter.')
    
    return utils.fit_pixels(signal, 
        model=_exp_recovery_2p_func, 
        xdata = np.array(TI),
        func_init = _exp_recovery_2p_func_init,
        bounds = bounds,
        p0 = p0, 
        parallel = parallel,
        **kwargs)




def _abs_exp_recovery_3p_func(t, S0, T1, eff):
    return np.abs(S0 * (1 - eff * np.exp(-t/T1)))

def _abs_exp_recovery_3p_func_init(t, signal, init):
    S0 = np.amax(np.abs(signal))
    return [S0*init[0], init[1], init[2]]
    
def abs_exp_recovery_3p(signal, 
        TI = None,
        bounds = (
            [0,0,0],
            [np.inf, np.inf, 2], 
        ),
        p0 = [1,1.3,2], 
        parallel = False,
        **kwargs):
    
    """
    3-parameter absolute exponential recovery model fit
    
    Parameters
    ----------
        signal : numpy.ndarray
            Signal data 
            Spatial array with signal intensities over different 
            inversion times.
        TI : numpy.array
            Inversion times
        bounds : tuple
            Bounds for the fit
        p0 : list
            Initial parameters
        parallel : bool
            Use parallel processing
        **kwargs :
            Additional keyword arguments
    
    Returns
    -------
        fit : numpy.ndarray
            Fitted data
        par : numpy.ndarray
            Parameters
            The parameters are: S0, T1, eff, giving N=3.
        
    """
    
    if TI is None:
        raise ValueError('TI is a required parameter.')
    
    return utils.fit_pixels(signal, 
        model = _abs_exp_recovery_3p_func, 
        xdata = np.array(TI),
        func_init = _abs_exp_recovery_3p_func_init,
        bounds = bounds,
        p0 = p0, 
        parallel = parallel,
        **kwargs)



def _exp_recovery_3p_func(t, S0, T1, eff):
    return S0 * (1 - eff * np.exp(-t/T1))

def _exp_recovery_3p_func_init(t, signal, init):
    S0 = np.amax(np.abs(signal))
    return [S0*init[0], init[1], init[2]]
    
def exp_recovery_3p(signal, 
        TI = None,
        bounds = (
            [0,0,0],
            [np.inf, np.inf, 2], 
        ),
        p0 = [1,1.3,2], 
        parallel = False,
        **kwargs):
    
    """
    3-parameter exponential recovery model fit
    
    Parameters
    ----------
        signal : numpy.ndarray
            Signal data 
            Spatial array with signal intensities over different 
            inversion times.
        TI : numpy.array
            Inversion times
        bounds : tuple
            Bounds for the fit
        p0 : list
            Initial parameters
        parallel : bool
            Use parallel processing
        **kwargs :
            Additional keyword arguments

    Returns
    -------
        fit : numpy.ndarray
            Fitted data
        par : numpy.ndarray
            Parameters
            The parameters are: S0, T1, eff, giving N=3.
        
        """
    
    if TI is None:
        raise ValueError('TI is a required parameter.')
    
    return utils.fit_pixels(signal, 
        model = _exp_recovery_3p_func, 
        xdata = np.array(TI),
        func_init = _exp_recovery_3p_func_init,
        bounds = bounds,
        p0 = p0, 
        parallel = parallel,
        **kwargs)

def spgr_vfa_nonlin(signal, 
        FA = None,
        bounds = (
            [0, 0],
            [np.inf, 1], 
        ),
        p0 = [1, 0.5], 
        parallel = False,
        **kwargs):
    
    """
    Non-linear SPGR model fit

    Parameters
    ----------
        signal : numpy.ndarray
            Signal data 
            Spatial array with signal intensities over different 
            flip angles.
        FA : numpy.array
            Flip Angles
        bounds : tuple
            Bounds for the fit
        p0 : list
            Initial parameters
        parallel : bool
            Use parallel processing
        **kwargs :
            Additional keyword arguments

    Returns
    -------
        fit : numpy.ndarray
            Fitted data 
        pars : numpy.ndarray
            Fitted model parameters
            The parameters are: S0, T1, giving N=2.
            
    
    """
    
    if FA is None:
        raise ValueError('Flip Angles (FA) are a required parameter.')
    
    # Precompute sin and cos
    FA = np.deg2rad(FA)
    trigFA = np.stack((np.sin(FA), np.cos(FA)), axis=0)

    fit, par = utils.fit_pixels(signal, 
        model = _spgr_vfa_nonlin_func, 
        xdata = trigFA,
        func_init = _spgr_vfa_nonlin_func_init,
        bounds = bounds,
        p0 = p0, 
        parallel = parallel,
        **kwargs)

    return fit, par

def _spgr_vfa_nonlin_func(trigFA, S0, E):
    if 0 in (1 - trigFA[1,:] * E):
        return S0 * trigFA[0,:] 
    else:
        return S0 * trigFA[0,:] * (1-E) / (1 - trigFA[1,:] * E) 

def _spgr_vfa_nonlin_func_init(trigFA, signal, init):
    S0 = np.amax(np.abs(signal))/np.amax(trigFA[0,:])
    return [S0*init[0], init[1]]



def spgr_vfa_lin(signal, FA = None, progress_bar=False):
    
    """
    Linearised SPGR model fit

    Parameters
    ----------
        signal : numpy.ndarray
            Signal data 
            Spatial array with signal intensities over different 
            flip angles.
        FA : numpy.array
            Flip Angles in degrees
        progress_bar: bool
            Display a progress bar (default = False)
    
    Returns
    -------
        fit : numpy.ndarray
            Fitted data
        pars : numpy.ndarray
            Parameters
            The parameters are: A (slope) and B (intercept).
    
    """
    if FA is None:
        raise ValueError('FLip Angles (FA) are a required parameter.')
    
    FA = np.deg2rad(FA)

    # Construct FA array in matching shape to signal data
    FA_array = np.ones_like(signal)*FA
    sFA_array = np.sin(FA_array)

    X = signal / sFA_array
    Y = signal * np.cos(FA_array) / sFA_array

    shape = signal.shape
    X = X.reshape(-1, shape[-1])
    Y = Y.reshape(-1, shape[-1])
    signal = signal.reshape(-1, shape[-1])

    pars = np.empty((X.shape[0], 2))
    fit = np.empty(X.shape)

    sFA, cFA = np.sin(FA), np.cos(FA)
    ones = np.ones(shape[-1])

    for i in tqdm(range(X.shape[0]), desc='Fitting VFA model', disable=not progress_bar):
        A = np.vstack([X[i,:], ones])
        pars[i,:] = np.linalg.lstsq(A.T, Y[i,:], rcond=None)[0]
        if 0 in (cFA - pars[i,0]):
            fit[i,:] = signal[i,:]
        else:
            fit[i,:] = pars[i,1] * sFA / (cFA - pars[i,0])
        smax = np.amax(signal[i,:])
        fit[i,:][fit[i,:] > smax] = smax

    fit[fit<0] = 0
    fit[np.isnan(fit)] = 0
    
    return fit.reshape(shape), pars.reshape(shape[:-1] + (2,))



def array_2cfm_lin(signal, 
        aif = None,
        time = None,
        baseline = None,
        Hct = None, **kwargs):
    
    """
    Linearised 2-compartment filtration model fit

    Parameters
    ----------
        signal : numpy.ndarray
            Signal data 
            Spatial array with signal intensities over an additional
            time dimension.
        aif : numpy.ndarray
            Arterial input function. 1D array of input artery signal 
            intensities, length equal to the number of time points in the 
            signal data.
        time : numpy.ndarray
            Timepoints of the signal data
        baseline : int
            Baseline. Number of time points to use for the baseline signal.
        Hct : float
            Haematocrit.
    
    Returns
    -------
        fit : numpy.ndarray
            Fitted data
        par : numpy.ndarray
            Fitted model parameters
            The parameters are: Fp, Tp, PS, Te, giving N=4.

    """

    if aif is None:
        raise ValueError('aif is a required parameter.')
    elif time is None:
        raise ValueError('Time is a required parameter.')
    elif baseline is None:
        raise ValueError('Baseline is a required parameter.')
    elif Hct is None:    
        raise ValueError('Hct is a required parameter.')
    
    return _array_2cfm_lin_func(signal, aif, time, baseline, Hct, **kwargs)

def _array_2cfm_lin_func(signal:np.ndarray, 
                   aif:np.ndarray=None, 
                   time:np.ndarray=None, 
                   baseline:int=1, 
                   Hct=0.45,
                   **kwargs):

    # Reshape to 2D (x,t)
    shape = np.shape(signal)
    signal = signal.reshape((-1,shape[-1]))

    S0 = np.mean(signal[:,:baseline], axis=1)
    Sa0 = np.mean(aif[:baseline])
    ca = (aif-Sa0)/(1-Hct)
    
    A = np.empty((signal.shape[1],4))
    A[:,2], A[:,3] = utils._ddint(ca, time)

    fit = np.empty(signal.shape)
    par = np.empty((signal.shape[0], 4))
    for x in range(signal.shape[0]):
        c = signal[x,:] - S0[x]
        ctii, cti = utils._ddint(c, time)
        A[:,0] = -ctii
        A[:,1] = -cti
        p = np.linalg.lstsq(A, c, rcond=None)[0] 
        fit[x,:] = S0[x] + p[0]*A[:,0] + p[1]*A[:,1] + p[2]*A[:,2] + p[3]*A[:,3]
        par[x,:] = _array_2cfm_lin_params(p)

    # Apply bounds
    smax = np.amax(signal)
    fit[fit<0]=0
    fit[fit>2*smax]=2*smax

    # Return in original shape
    fit = fit.reshape(shape)
    par = par.reshape(shape[:-1] + (4,))

    return fit, par

def _array_2cfm_lin_params(X):

    alpha = X[0]
    beta = X[1]
    gamma = X[2]
    Fp = X[3]
    
    if alpha == 0: 
        if beta == 0:
            return [Fp, 0, 0, 0]
        else:
            return [Fp, 1/beta, 0, 0]

    nom = 2*alpha
    det = beta**2 - 4*alpha
    if det < 0 :
        Tp = beta/nom
        Te = Tp
    else:
        root = np.sqrt(det)
        Tp = (beta - root)/nom
        Te = (beta + root)/nom

    if Te == 0:
        PS = 0
    else:   
        if Fp == 0:
            PS = 0
        else:
            T = gamma/(alpha*Fp) 
            PS = Fp*(T-Tp)/Te   

    # Convert to conventional units and apply bounds
    Fp*=6000
    if Fp<0: Fp=0
    if Fp>2000: Fp=2000
    if Tp<0: Tp=0
    if Tp>600: Tp=600
    PS*=6000
    if PS<0: PS=0
    if PS>2000: PS=2000
    if Te<0: Te=0
    if Te>600: Te=600
    
    return [Fp, Tp, PS, Te]