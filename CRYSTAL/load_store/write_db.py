import csv
import os

import numpy as np

import utility.utility as utility

# Clusters are denoted by the 2-tuple (start_px, end_px). This set of globals
# notes that the index of the start pixel, given by ST_IND, is 0, and the
# index of the finish pixel, given by END_IND, is 1.
global ST_IND
ST_IND = 0
global END_IND
END_IND = 1

def gen_record(shard, px, coadd_x, coadd_y, PCCs, coeffs, clss):

    '''
    Generates a formatted record for a set of record values.
    '''

    order_fmt = "{:0=2d}".format(shard.order)
    px_fmt = "{:0=4d}".format(px + shard.lo_px)
    wv_fmt = "{:.2f}".format(coadd_x[px])
    intensity_fmt = "{:.4f}".format(coadd_y[px])

    if clss == "w" or clss == "z":
        r_m, r_c = coeffs[px]
        PCC_fmt = "{:.3f}".format(PCCs[px])
        r_m_fmt = "{:.5f}".format(r_m)
        r_c_fmt = "{:.5f}".format(r_c)
    elif clss == "c":
        PCC_fmt = "-1"
        r_m_fmt = "-1"
        r_c_fmt = "-1"

    return [order_fmt, px_fmt, wv_fmt, clss, PCC_fmt, r_m_fmt, r_c_fmt, intensity_fmt]

def write_db(shards, calibrators, config):
    '''
    Writes the telluric model developed out to a database.

    This database contains a single relation which contains a record for each
    telluric pixel detected. This relation's attributes are, in order:

    order ordpx wavelength class PCC r_m r_c med_intensity

    where:
        ordpx is the telluric pixel's pixel number in its order
        wavelength is the average wavelength of the pixel in the training data
        class flags whether the pixel is water, non-water or composite
        PCC is the pixel's PCC with the relevant calibrator (0 for composite)
        r_m and r_c are its coefficients in in the linear regression model

        log(depth) = r_m * calibrator_value + r_c

        and med_intensity is pixel's median intensity in the training data
    '''
    
    # 1) Sort shard addr in order of order, with shard_addr of the same order sorted by order of 
    # start pixel. We accomplish this by first sorting by order of start pixel, and then using
    # a stable sort (mergesot) - a sort which is guarenteed to preserve the relative ordering of
    # elements with the same initial positioning, to sort by order.
    sorted_shard_addr = np.array(shards.keys())
    sorted_shard_addr = sorted_shard_addr[sorted_shard_addr[:,1].argsort()]
    sorted_shard_addr = sorted_shard_addr[sorted_shard_addr[:,0].argsort(kind='mergesort')]

    # 2) Create a record for each telluric pixel in database in increasing order of wavelength
    
    csv_file = open(os.path.join(config["cal_db_path"], config["cal_db_filename"]), "wb")
    csv_writer = csv.writer(csv_file, delimiter=" ", quotechar="'", quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["order", "px", "wavelength", "class", "PCC", "r_m", "r_c", "med_intensity"])

    for shard_addr in sorted_shard_addr:
        shard = shards[tuple(shard_addr)]
        w_clusters = shard.w_clusters[:] + [[float("inf"), float("inf")]] #sentinel
        z_clusters = shard.z_clusters[:] + [[float("inf"), float("inf")]]
        c_clusters = shard.c_clusters[:] + [[float("inf"), float("inf")]]
        w_i, z_i, c_i = 0, 0, 0

        coadd_x, coadd_y = utility.coadd_spectrum(shard)
        while w_i < len(w_clusters) - 1 or z_i < len(z_clusters) - 1 or c_i < len(c_clusters) - 1:

            # 2a) Write water telluric to db
            if w_clusters[w_i] < z_clusters[z_i] and w_clusters[w_i] < c_clusters[c_i]:
                for px in range(w_clusters[w_i][ST_IND], w_clusters[w_i][END_IND] + 1):
                    rc = gen_record(shard, px, coadd_x, coadd_y, shard.w_PCCs, shard.w_coeffs, "w")
                    csv_writer.writerow(rc)
                w_i += 1
            # 2b) Write non-water telluric to db
            elif z_clusters[z_i] < w_clusters[w_i] and z_clusters[z_i] < c_clusters[c_i]:
                for px in range(z_clusters[z_i][ST_IND], z_clusters[z_i][END_IND] + 1):
                    rc = gen_record(shard, px, coadd_x, coadd_y, shard.z_PCCs, shard.z_coeffs, "z")
                    csv_writer.writerow(rc)
                z_i += 1
            # 2c) Write composite telluric to db
            else:
                for px in range(c_clusters[c_i][ST_IND], c_clusters[c_i][END_IND] + 1):
                    rc = gen_record(shard, px, coadd_x, coadd_y, None, None, "c")
                    csv_writer.writerow(record)
                c_i += 1

    csv_file.close()
            
        
