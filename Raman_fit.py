
import numpy as np
import pandas as pd
# import time
# from scipy.signal import find_peaks
# from statsmodels.nonparametric.smoothers_lowess import lowess
# from tqdm import tqdm
import multiprocessing
from functools import partial
from fit_func import fit

class Raman_raw():
    def __init__(self, filename, width,  peak_nums, smooth_factor):
        
        self.data = pd.read_csv(filename, 
                                sep='\t', 
                                header=None, 
                                index_col=0,
                                comment='#').T.iloc[:-1]
        self.width = width
        self.height = int(self.data.index.size/self.width)
        self.peak_nums = peak_nums
        self.smooth_factor = smooth_factor
        # self.E_map_raw = np.zeros(self.width * self.height)
        # self.A_map_raw = np.zeros(self.width * self.height)
        # self.Si_map_raw = np.zeros(self.width * self.height)
        
    def fit(self):
        fit_partial = partial(fit, peak_num=self.peak_nums, sm_frac=self.smooth_factor)
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        self.fit_result = pool.map(fit_partial,self.data.iterrows())
        self.fit_result = np.array(self.fit_result).T
        # self.fit_result is a np array of shape (self.peak_nums, self.height*self.width)
        self.result= []
        for data in self.fit_result:
            self.result.append(np.array(np.split(data,self.height)))
        pool.close()
        pool.join()

class MoS2_Raman():
    
    def __init__(self, filename, width=400, smooth_factor=0.015):
        
        self.width = width
        self.smooth_factor = smooth_factor
        
        self.raw = Raman_raw(filename=filename, 
                             width=self.width, 
                             peak_nums=3, 
                             smooth_factor=self.smooth_factor)
        self.height = self.raw.height
        
        # self.E_map_raw = np.zeros(self.width * self.height)
        # self.A_map_raw = np.zeros(self.width * self.height)
        # self.Si_map_raw = np.zeros(self.width * self.height)
        # self.E_map = np.zeros(self.width * self.height)
        # self.A_map = np.zeros(self.width * self.height)
        
    def fit(self):
        self.raw.fit()
        self.E_map_raw = self.raw.result[0]
        self.A_map_raw = self.raw.result[1]
        self.Si_map_raw = self.raw.result[2]
        self.E_map = self.E_map_raw - (self.Si_map_raw - 520.0)
        self.A_map = self.A_map_raw - (self.A_map_raw - 520.0)
        self.result = np.zeros((2,self.height, self.width))
        
        self.result[0] = self.E_map
        self.result[1] = self.A_map
        
        return self.result
   