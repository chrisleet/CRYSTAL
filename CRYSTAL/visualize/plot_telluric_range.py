import matplotlib.pyplot as plt
import numpy as np

import load_store.db_indicies as dbi

def plot_telluric_range(db, wv_lo, wv_hi):

    '''
    Plots the tellurics in the database from argv[1]-argv[2] nm.

    Plot the database's telluric spectrum for an average airmass and PWV.
    Water telluric pixels are colored blue, non-water pixels are colored
    red, and composite pixels are colored purple.
    '''

    PTS_WV_DIFF = 0.035 #Max wavelength distance between any two points
    
    pts_x, pts_y = [], []
    w_pts, z_pts, c_pts = [], [], []

    for record in db:
        if wv_lo <= record[dbi.WV_IND] and record[dbi.WV_IND] <= wv_hi:
            pts_x.append(record[dbi.WV_IND])
            pts_y.append(np.exp(record[dbi.INT_IND]))
            if record[dbi.CLS_IND] == "w":
                w_pts.append(len(pts_x)-1)
            elif record[dbi.CLS_IND] == "z":
                z_pts.append(len(pts_x)-1)
            elif record[dbi.CLS_IND] == "c":
                c_pts.append(len(pts_x)-1)


    plot_pts_x, plot_pts_y = [], []
    for i in xrange(len(pts_x)):
        if i == 0 or pts_x[i] - pts_x[i-1] > 2*PTS_WV_DIFF:
            plot_pts_x.append(pts_x[i] - PTS_WV_DIFF)
            plot_pts_y.append(1.0)
        plot_pts_x.append(pts_x[i])
        plot_pts_y.append(pts_y[i])
        if i == len(pts_x) - 1 or pts_x[i+1] - pts_x[i] > 2*PTS_WV_DIFF:
            plot_pts_x.append(pts_x[i] + PTS_WV_DIFF)
            plot_pts_y.append(1.0)
        elif pts_x[i+1] - pts_x[i] > PTS_WV_DIFF:
            plot_pts_x.append((pts_x[i+1] + pts_x[i])/2.0)
            plot_pts_y.append(1.0)

    if plot_pts_x[0] - wv_lo > PTS_WV_DIFF:
        plot_pts_x = [wv_lo] + plot_pts_x
        plot_pts_y = [1.0] + plot_pts_y

    if wv_hi - plot_pts_x[-1] > PTS_WV_DIFF:
        plot_pts_x.append(wv_hi)
        plot_pts_y.append(1.0)

    fig = plt.figure(facecolor="white")
    plt.scatter(np.array(pts_x)[w_pts], np.array(pts_y)[w_pts], 
                color="b", marker="X", label="Water px", zorder=1)
    plt.scatter(np.array(pts_x)[z_pts], np.array(pts_y)[z_pts], 
                color="r", marker="X", label="Non-water px", zorder=1)
    plt.scatter(np.array(pts_x)[c_pts], np.array(pts_y)[c_pts], 
                color="purple", marker="X", label="Composite px", zorder=1)
    plt.plot(plot_pts_x, plot_pts_y, color="k", zorder=2)
    plt.title(r'Telluric spectrum {}-{}$\AA$'.format(wv_lo, wv_hi))
    plt.xlabel(r'Wavelength ($\AA$)')
    plt.ylabel("Signal Strength")
    plt.legend()
    plt.show()
        
