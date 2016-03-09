'''
    Calculate virtual potential temperature from
    RASS virtual temperature observations

    RASS retrieves virtual temperature observations
    using variations in speed of sound:
    Cs ~= 20Tv^(1/2)

    Raul Valenzuela
    raul.valenzuela@colorado.edu

'''
import Meteoframes as mf
import pandas as pd
import numpy as np


def get_thetav(case=None, Tv_array=None, hgt_array=None, homedir=None):
    '''
        Equations derived using hypsometric eq (3.29 W&H)
        and theta defintion (3.54 W&H). Method is equivalent
        to Neiman et al (1992)
    '''
    g = 9.8  # [m/s2]
    Rd = 287  # [J K-1 kg-1]
    press = get_pressure(case=case, homedir=homedir).values
    press2 = np.expand_dims(press, axis=1)
    a, _ = hgt_array.shape
    press2 = np.repeat(press2, a, axis=1).T

    Tv = Tv_array + 273.15  # [K]

    Z_1000 = 8*(press2 - 1000)
    Z = hgt_array*1000.  # [m]
    f1 = (Z - Z_1000) * g
    f2 = Rd * Tv
    thetav = Tv * np.power(np.exp(f1/f2), (2/7.))
    return thetav


def get_pressure(case=None, homedir=None):
    from glob import glob

    fpath = '/home/rvalenzuela/SURFACE/case{}/bby*'
    surf_files = glob(fpath.format(str(case).zfill(2)))
    surf_files.sort()
    df_list = []
    for f in surf_files:
        df_list.append(mf.parse_surface(f))

    if len(df_list) > 1:
        df = pd.concat(df_list)
    else:
        df = df_list[0]

    g = pd.TimeGrouper('60T')
    dfg = df['press'].groupby(g).mean()
    return dfg
