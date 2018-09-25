import matplotlib.pyplot as plt
import numpy as np

import data_containers.shard as shi
import load_store.db_indicies as dbi


def x_correlate(cal_pxs, shards, db, config):

    '''
    XCorrelate the telluric model with the spectrum on the calibration pxs.
    '''
        
    best_shift = -20
    best_SSE = float('inf')
    for shift in range(-config["x_corr_shift"], config["x_corr_shift"]+1):
        SSE = 0
        SSEs = {}

        for r in db:
            r_order = r[dbi.ORD_IND]
            r_x = r[dbi.PX_IND] + shift
            r_y = r[dbi.INT_IND]
            if (r_order, r[dbi.PX_IND]) in cal_pxs and r[dbi.CLS_IND] == "w":
                for shard in shards.itervalues():
                    if shard.order == r_order and shard.lo_px <= r_x and r_x < shard.hi_px:
                        s_y = shard.spectra.itervalues().next().log_y[r_x - shard.lo_px]
                        DIFF_LIM = 0.1
                        if r_y - s_y > DIFF_LIM:
                            SSE += abs(DIFF_LIM)
                        else:
                            SSE += abs(r_y - s_y)
                        SSEs[(r_order, r[dbi.PX_IND])] = abs(r_y - s_y)

        #print "SSEs:{}".format(SSEs)
        #print "shift:{} SSE:{}, best_shift:{}, best_SSE:{}".format(shift, SSE, best_shift, best_SSE)

        if SSE < best_SSE:
            best_shift = shift
            best_SSE = SSE
    
    return best_shift   
    
