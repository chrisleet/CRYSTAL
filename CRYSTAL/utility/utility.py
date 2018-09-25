import numpy as np

def coadd_spectrum(shard):

    '''
    Coadds each spectrum in shard.
    '''

    shard_px = shard.hi_px - shard.lo_px
    coadd_x = np.zeros(shard_px)
    coadd_y = np.zeros(shard_px)
    cnt = 0
    for spectrum in shard.spectra.itervalues():
        coadd_x += spectrum.lin_x
        coadd_y += spectrum.log_y
        cnt += 1
    coadd_x /= cnt
    coadd_y /= cnt
    return (coadd_x, coadd_y)
