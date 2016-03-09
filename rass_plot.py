import Meteoframes as mf
import os
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from rv_utilities import add_colorbar

homedir = os.path.expanduser('~')

for r in range(8, 15):
    print 'case '+str(r)
    print '-----------------'
    fs = glob(homedir+'/RASS/c'+str(r).zfill(2)+'/*.cns')
    fs.sort()

    for n, f in enumerate(fs):
        T, Tc, Hgt, timestamp = mf.parse_rass(f)
        print T.shape
        if n == 0:
            Tstack = T
            ts = np.array(timestamp)
        else:
            Tstack = np.hstack((Tstack, T))
            ts = np.hstack((ts, np.array(timestamp)))

    ' QC'
    mu = np.nanmean(Tstack)
    sigma = np.nanstd(Tstack)
    bot = mu-3*sigma
    top = mu+3*sigma
    Tstack[Tstack <= bot] = np.nan
    Tstack[Tstack >= top] = np.nan

    plt.figure()
    im = plt.imshow(Tstack, interpolation='none', origin='lower')
    plt.gca().invert_xaxis()
    add_colorbar(plt.gca(), im)
    plt.tight_layout()
    plt.title('case '+str(r))
    plt.show(block=False)
