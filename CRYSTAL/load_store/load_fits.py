import os

from astropy.io import fits
import numpy as np

import data_containers.shard as shard

def get_fits_filename_from_argv(argv):

    '''
    Returns the fits file name given in the program's argv
    '''

    FILE_IND = 1 #Fits file is given as the first arg in program calling sequence

    if len(argv) < 2:
        raise Exception("No fits file given to reduce.")
    elif not argv[FILE_IND].endswith('.fits'):
        raise Exception("File given to reduce is not a fits file.")
    return [argv[FILE_IND]]

def get_fits_filenames_at_path(config):    

    '''
    Returns the file name of each fits file at path.
    '''

    filenames = []
    for filename in os.listdir(config["cal_spectra_path"]):
        if filename.endswith('.fits'):
            filenames.append(filename)
    return filenames


def load_fits_orders(filenames, config, add_path=True):

    '''
    Loads spectra from the given fits files into a shard for each order.
    
    For details of the shard data container, see data_container/shard

    Parameters
    ----------
    filenames: list (string)
        A list of the files to load

    config: config
       The config file

    add_path: bool
        If true, adds path to filenames before opening their file
    '''

    # 1) Open each file in filenames
    file_dict = {}
    for filename in filenames:
        if add_path:
            filename = os.path.join(config["cal_spectra_path"], filename)
        f = fits.open(filename, do_not_scale_image_data=True)
        file_dict[filename] = f

    # 2) Resolve orders to read if the orders setting in config is a special
    # keyword.
    FIRST_CHIRON_ORDER = 0
    LAST_BLUE_ORDER = 44
    FIRST_RED_ORDER = 45
    LAST_CHIRON_ORDER = 61
        
    if config["orders"] == "blue":
        # Select the 44 bluest orders of CHIRON
        orders = np.arange(FIRST_CHIRON_ORDER, LAST_BLUE_ORDER+1) 
    elif config["orders"] == "red":
        # Select the 16 redest orders of CHIRON
        orders = np.arange(FIRST_RED_ORDER, LAST_CHIRON_ORDER) 
    elif config["orders"] == "all":
        orders = np.arange(0, 61) # Select all CHIRON orders
    else:
        orders = config["orders"] # Otherwise config[orders] is a list of orders

    # 3) Add each file's data for each selected order to that order's shard.
    order_shards = {}
    for order in orders:
        order_shards[order] = shard.Shard(order, 0, config["pixels_per_order"])

        for filename, f in file_dict.iteritems():
            
            order_data = f[0].data[order]
            lin_x = np.array(order_data[:,0])
            lin_y = np.array(order_data[:,1])
            log_y = np.log(lin_y)
            z = float(f[0].header["AIRMASS"])
            f_data = shard.Spectrum_Data(lin_x, lin_y, log_y, z)
            order_shards[order].spectra[filename] = f_data

    # 3) Close spectrum files
    for filename, f in file_dict.iteritems():
        f.close(output_verify = "warn")

    return order_shards
