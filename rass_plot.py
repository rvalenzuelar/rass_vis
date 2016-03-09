import Meteoframes as mf
import os
import matplotlib.pyplot as plt
import numpy as np
from rass_thetav import get_thetav
from glob import glob
from rv_utilities import add_colorbar, format_xaxis, format_yaxis

homedir = os.path.expanduser('~')


for r in range(8, 14):
    ''' case 14 does not have RASS obs '''
    print 'case '+str(r)
    print '-----------------'
    fs = glob(homedir+'/RASS/c'+str(r).zfill(2)+'/*.cns')
    fs.sort()

    for n, f in enumerate(fs):
        T, Tc, Hgt, timestamp = mf.parse_rass(f)
        if n == 0:
            Tstack = T
            Hgtstack = Hgt
            ts = np.array(timestamp)
        else:
            Tstack = np.hstack((Tstack, T))
            Hgtstack = np.hstack((Hgtstack, Hgt))
            ts = np.hstack((ts, np.array(timestamp)))

    thetav = get_thetav(case=r, Tv_array=Tstack,
                        hgt_array=Hgtstack, homedir=homedir)
    titletxt = 'Case{} ({})'
    fig, ax = plt.subplots(2, 1, sharex=True)
    im = ax[0].imshow(Tstack, interpolation='none', origin='lower')
    ax[0].set_title(titletxt.format(str(r), ts[0].strftime('%Y-%b')))
    ax[0].text(0.05, 0.9, 'Virtual temperature', transform=ax[0].transAxes)
    add_colorbar(ax[0], im)
    format_xaxis(ax[0], ts)
    format_yaxis(ax[0], Hgt[:, 0])
    im = ax[1].imshow(thetav, vmin=282, vmax=294,
                      interpolation='none', origin='lower')
    add_colorbar(ax[1], im)
    format_yaxis(ax[1], Hgt[:, 0])
    ax[1].text(0.05, 0.9, 'Thetav', transform=ax[1].transAxes)
    ax[1].invert_xaxis()
    plt.tight_layout()
    plt.show(block=False)
