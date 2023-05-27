
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from statsmodels.nonparametric.smoothers_lowess import lowess
from tqdm import tqdm

class MoS2_Raman():
    def __init__(self, filename, height, width=400, smooth_factor=0.015):
        self.data = pd.read_csv(filename, sep='\t', header=None, index_col=0).T.iloc[:-1]
        self.height = height
        self.width = width
        self.smooth_factor = smooth_factor
        self.E_map_raw = np.zeros(self.width * self.height)
        self.A_map_raw = np.zeros(self.width * self.height)
        self.Si_map_raw = np.zeros(self.width * self.height)
        
    def fit(self):
        for i in tqdm(range(self.width*self.height)):
            spectra = self.data.iloc[i]
            filtered = lowess(spectra.values, spectra.index, is_sorted=True, frac=self.smooth_factor, it=0).T
            peaks, dict = find_peaks(filtered[1], height=0)
            self.E_map_raw[i], self.A_map_raw[i], self.Si_map_raw[i] = np.sort(filtered[0][peaks[np.argpartition(dict['peak_heights'],-3)[-3:]]])
        self.correct()

    def correct(self):
        self.E_map = np.array(np.split(self.E_map_raw - (self.Si_map_raw - 520.0),self.height))
        self.A_map = np.array(np.split(self.A_map_raw - (self.Si_map_raw - 520.0),self.height))
            
        






