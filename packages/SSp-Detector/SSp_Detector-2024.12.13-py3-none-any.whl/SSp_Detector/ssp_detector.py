#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#   Copyright (c) 2024. Simon J. Guillot. All rights reserved.                            +
#   Redistribution and use in source and binary forms, with or without modification, are strictly prohibited.
#                                                                                         +
#   THIS CODE IS PROVIDED BY THE COPYRIGHT HOLDER "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
#   BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#   IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#   OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#   STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS CODE,
#   EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import logging

import mne
import numpy as np
from mne.filter import filter_data
from scipy import signal
from scipy.interpolate import interp1d

LOGGING_TYPES=dict(
    DEBUG=logging.DEBUG,
    INFO=logging.INFO,
    WARNING=logging.WARNING,
    ERROR=logging.ERROR,
    CRITICAL=logging.CRITICAL,
)


def spindles_abs(raw,sf,thresh=None) -> int:
    """Detects sleep spindles using absolute Sigma power.

    Notes
    ----------
    If you use this toolbox, please cite as followed:

    * Guillot S.J., (2023). Sleep spindles detector (2024.12.10). GitHub, Zenodo.
    https://doi.org/10.5281/zenodo.10066031

    We provide below some key points on the toolbox.

    If you have any questions, feel free to reach out on `GitHub <https://github.com/sjg2203/>`_.

    Example
    ----------
    >>> from SSp_Detector import spindles_abs
    >>> #Load an EDF file using MNE
    >>> raw=mne.io.read_raw_edf("myfile.edf",preload=True)
    >>> sfreq=raw.info['sfreq']
    >>> #Return sleep spindles count into an array
    >>> spindles_abs(raw,sf=sfreq,thresh={'abs_pow':1.25})

    Parameters
    ----------
    raw : :py:class:`mne.io.BaseRaw`
            An MNE Raw instance.
    sf : float
            Sampling frequency in Hz.
    thresh : dict, optional
            Detection thresholds:
            ``'abs_pow'``: Absolute Sigma power (=power ratio freq_sigma/freq_broad; 1.25).

            If None is given, ``'abs_pow'``:0.2 automatically.

    Returns
    -------
    int
            count of sleep spindles using absolute Sigma power.
    """

    if 'abs_pow' not in thresh.keys():
        thresh['abs_pow']=1.25
    # If sf>100Hz, then data will be resampled to meet the 100Hz requirement
    if sf>100:
        raw.resample(100)
        sf=100
    freq_broad=[1,30]
    raw_data=raw.get_data()[0]*1e6
    data=filter_data(raw_data,sf,freq_broad[0],freq_broad[1],method="fir",verbose=0)
    # Apply a low and high bandpass filter
    nyquist=sf/2
    data_sigma=signal.sosfiltfilt(signal.iirfilter(20,[11/nyquist,16/nyquist],btype='bandpass',output='sos'),
                                  data.copy())
    duration=0.3
    step=0.1
    total_duration=len(data_sigma)/sf
    len_out=int(total_duration/step)
    out=np.zeros(len_out)
    tt=np.zeros(len_out)
    for i,j in enumerate(np.arange(0,total_duration,step)):
        beg=max(0,int((j-duration/2)*sf))
        end=min(len(data_sigma)-1,int((j+duration/2)*sf))
        tt[i]=np.column_stack((beg,end)).mean(1)/sf
        out[i]=np.mean(np.square(data_sigma[beg:end]))
    abs_sig_pow=np.log10(np.clip(out,1e-9,None))
    abs_sig_pow_interp=interp1d(tt,abs_sig_pow,kind='cubic',bounds_error=False,fill_value=0,assume_sorted=True)(
        np.arange(len(data_sigma))/sf)
    # Count of sleep spindles using absolute sigma power
    #spindles_abs_count=sum(abs_sig_pow_interp>=thresh["abs_pow"])
    spindles_count={}
    name=0
    for item in abs_sig_pow_interp:
        if item>=thresh['abs_pow']:
            spindles_count[f'item{name}']=[item]
        else:
            name+=1
    spindles_abs_count=len(spindles_count)
    text='spindle' if spindles_abs_count==1 else 'spindles'
    print(f'Using absolute Sigma power: {spindles_abs_count} {text}')
    return spindles_abs_count


def spindles_rel(raw, sf, thresh=None) -> int:
    """Detects sleep spindles using relative Sigma power.

    Notes
    ----------
    If you use this toolbox, please cite as followed:

    * Guillot S.J., (2023). Sleep spindles detector (2024.12.10). GitHub, Zenodo.
    https://doi.org/10.5281/zenodo.10066031

    We provide below some key points on the toolbox.

    If you have any questions, feel free to reach out on `GitHub <https://github.com/sjg2203/>`_.

    Example
    ----------
    >>> from SSp_Detector import spindles_rel
    >>> #Load an EDF file using MNE
    >>> raw=mne.io.read_raw_edf("myfile.edf",preload=True)
    >>> sfreq=raw.info['sfreq']
    >>> #Return sleep spindles count into an array
    >>> spindles_abs(raw,sf=sfreq,thresh={'rel_pow':0.2})

    Parameters
    ----------
    raw : :py:class:`mne.io.BaseRaw`
            An MNE Raw instance.
    sf : float
            Sampling frequency in Hz.
    thresh : dict, optional
            Detection thresholds:
            ``'rel_pow'``: Relative Sigma power (=power ratio freq_sigma/freq_broad; 0.2).

            If None is given, ``'rel_pow'``:0.2 automatically.

    Returns
    -------
    int
            count of sleep spindles using relative Sigma power.
    """

    if 'rel_pow' not in thresh.keys():
        thresh['rel_pow']=0.2
    # If sf>100Hz, then data will be resampled to meet the 100Hz requirement
    if sf>100:
        raw.resample(100)
        sf=100
    raw_data=raw.get_data()[0]*1e6
    data=mne.filter.filter_data(raw_data,sf,1,30,method='fir',verbose=0)
    # Apply a low and high bandpass filter
    f,t,SXX=signal.stft(data,sf,nperseg=int((2*sf)),noverlap=int((2*sf-0.2*sf)))
    # Using STFT to compute the point-wise relative power
    idx_band=(f>=1)&(f<=30)
    # Keeping only the frequency of interest and Interpolating
    f=f[idx_band]
    SXX=np.square(np.abs(SXX[idx_band,:]))
    SXX/=SXX.sum(0,keepdims=True)
    idx_sigma=(f>=11)&(f<=16)
    rel_power=SXX[idx_sigma].sum(0)
    # Count of sleep spindles using relative sigma power
    spindles_rel_count=sum(rel_power>=thresh["rel_pow"])
    text='spindle' if spindles_rel_count==1 else 'spindles'
    print(f'Using relative Sigma power: {spindles_rel_count} {text}')
    return spindles_rel_count
