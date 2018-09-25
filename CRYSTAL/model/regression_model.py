import numpy as np

global ST_IND
ST_IND = 0
global END_IND
END_IND = 1

def find_regression_coeffs(shards, calibrators):

    '''
    Build a regression model for each telluric pixel & save regression coeffs.

    The regression model for water pixels is built by regression against the
    water calibrator, the regression model for non-water builds is built by
    regression against airmass.

    Notes
    -----
    The order in which spectrum appear in each calibrator is saved, and 
    spectra's depths' at the current telluric pixel are appended in that order
    to make sure that the regression's x and y values are in the right order.
    '''

    w_calibrator, z_calibrator, f_order = calibrators

    for shard in shards.itervalues():

        for clusters, coeffs, calibrator in zip([shard.w_clusters, shard.z_clusters],
                                                [shard.w_coeffs, shard.z_coeffs],
                                                [w_calibrator, z_calibrator]):
            for cluster in clusters:
                for px in range(cluster[ST_IND], cluster[END_IND]+1):
                    px_depth = []
                    for filename in f_order:
                        px_depth.append(shard.spectra[filename].log_y[px])
                    m, c = np.polyfit(calibrator, px_depth, 1)
                    coeffs[px] = (m, c)

                
