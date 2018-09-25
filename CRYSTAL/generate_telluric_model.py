import sys
import yaml

import load_store.load_fits as load_fits
import load_store.read_db as read_db
import load_store.write_spectrum as write_spectrum
import model.fit_model as fit_model
import model.get_calibrators as get_calibrators
import model.generate_model as generate_model
import model.telluric_identification as telluric_id
import preprocessing.divide_orders as divide_orders
import preprocessing.normalize as normalize
import preprocessing.x_correlate as x_correlate
import visualize.plot_shards as plot_shards
import visualize.plot_model as plot_model

def generate_telluric_model():

    # 0) DEFINE CONSTANTS
    FILE_ARGIND = 1  #File to reduce is the first argument of the terminal call

    # 1) LOAD DATA
    # Load external data for calibration. External data is: i) configuration
    # file, ii) filename of spectrum to reduce, iii) content of calibration
    # spectra. Loads calibration spectra contents into a data container for 
    # each order. These data containers are called shards. Produces a 
    # dictionary linking each processed order to its shard.
    config = yaml.safe_load(file("config/config.yml", "r"))
    db = read_db.read_db(config)
    filenames = load_fits.get_fits_filename_from_argv(sys.argv)
    order_shards = load_fits.load_fits_orders(filenames, config, add_path=False)
    plot_shards.plot_shards(order_shards, "wavelength", "log", config["plot_fspectrum_by_order"])

    # 2) PREPROCESS DATA
    # i)   Subdivide each order shard into smaller shards based on sharding configuration given in
    #      the config file.
    # ii)  Normalize each smaller shard.
    # iii) Get the calibration pixels from the config file.
    # iv)  Cross correlate the telluric model with the science spectrum on the calibration pixels.
    shards = divide_orders.divide_orders(order_shards, config)
    plot_shards.plot_shards(shards, "wavelength", "log", config["plot_fspectrum_by_shard"])
    normalize.normalize(shards)
    plot_shards.plot_shards(shards, "wavelength", "log", config["plot_normalized_fshards"], 
                            "after normalization")
    cal_pxs = get_calibrators.get_calibrators(config)
    shift = x_correlate.x_correlate(cal_pxs, shards, db, config)
    plot_shards.plot_shards_vs_xcorr_tel(db, shift, shards, config["plot_fspectrum_model_xcorr"])

    # 3) GENERATE TELLURIC SPECTRUM
    # i) Find spectrum mu by fitting the water calibrators' intensity to the science spectrum
    # ii) Retrieve z from science spectrum.
    # iii) Generate telluric spectrum for choice of mu and z
    mu = fit_model.get_mu(cal_pxs, shift, shards, db, config)
    z = fit_model.get_z(shards)
    model = generate_model.generate_model(mu, z, db, config)
    plot_model.plot_model(shift, shards, model, show=config["plot_fspectrum_model_fitted"])
    
    # 4) Write out model
    # i) Writes model out as csv file
    write_spectrum.write_spectrum(filenames, model)

if __name__ == "__main__":
    generate_telluric_model()
