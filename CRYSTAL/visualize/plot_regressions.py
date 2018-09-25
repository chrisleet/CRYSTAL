import sys

import matplotlib.pyplot as plt
import numpy as np

# Clusters are denoted by the 2-tuple (start_px, end_px). This set of globals
# notes that the index of the start pixel, given by ST_IND, is 0, and the
# index of the finish pixel, given by END_IND, is 1.
global ST_IND
ST_IND = 0
global END_IND
END_IND = 1

def plot_regressions(calibrators, shards, config):

    '''
    Plots each px selected in config's regression against its calibrator.

    Takes each pixel px in listed in config. Scatter plots the depth of 
    px for each spectrum against either (a) the average depth of the water 
    calibration lines if px is a water pixel or (b) airmass if px is a 
    non-water pixel, and then plots px's regression line over the scatter plot
    If px is neither a water pixel nor a non-water pixel, prints a message and
    does not produce a plot.
    '''
    
    if not config["plot_regression_models"]:
        return

    for shard_addr, px in config["regression_model_px"]:
        plot_px_regression(tuple(shard_addr), px, calibrators, shards)

def plot_px_regression(shard_addr, px, calibrators, shards):

    '''
    Plot the px in shard shard_addr's regression model with its calibrator.

    Worker function of plot regressions.
    '''

    w_calibrator, z_calibrator, f_order = calibrators
    
    if shard_addr not in shards:
        err_ms = "Err: shard {} not in shards, can't draw regression.".format(shard_addr)
        sys.stderr.write(err_ms)
        return
    shard = shards[shard_addr]
    
    px_depths = []
    for filename in f_order:
        px_depths.append(shard.spectra[filename].log_y[px])
    
    if px in shard.w_coeffs:
        r_model = np.poly1d(shard.w_coeffs[px])
        calibrator = w_calibrator
        cal_lbl = "Water calibrator"
    elif px in shard.z_coeffs:
        r_model = np.poly1d(shard.z_coeffs[px])
        calibrator = z_calibrator
        cal_lbl = "Airmass"
    else:
        err_ms = "Err: px {}, shard {} not telluric, can't draw regression".format(px, shard_addr)
        sys.stderr.write(err_ms)
        return

    fig = plt.figure(facecolor='white')
    plt.xlabel(cal_lbl)
    plt.ylabel("Px {} log signal strength".format(px, shard.order))
    plt.title("Px {}, shard (order {}, px {}-{}) regression w/ {}".format(px, 
                                                                          shard.order, shard.lo_px,
                                                                          shard.hi_px, cal_lbl))
    plt.scatter(calibrator, px_depths, marker="X", color="k")
    plt.plot(sorted(calibrator), r_model(sorted(calibrator)),"r--", zorder=0)
    plt.show()
        
