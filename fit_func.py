
import numpy as np
import pandas as pd

from scipy.signal import find_peaks
from statsmodels.nonparametric.smoothers_lowess import lowess

# def fit(spectra):
#     filtered = lowess(spectra[1].values, spectra[1].index, is_sorted=True, frac=0.015, it=0).T
#     peaks, dict = find_peaks(filtered[1], height=0)
#     return np.sort(filtered[0][peaks[np.argpartition(dict['peak_heights'],-3)[-3:]]])
def fit(spectra,peak_num,sm_frac):
    filtered = lowess(spectra[1].values, spectra[1].index, is_sorted=True, frac=sm_frac, it=0).T
    peaks, dict = find_peaks(filtered[1], height=0)
    return np.sort(filtered[0][peaks[np.argpartition(dict['peak_heights'],-peak_num)[-peak_num:]]])
