import yaml

import load_store.load_fits as load_fits
import load_store.write_db as write_db
import model.cluster_analysis as cluster_analysis
import model.regression_model as regression_model
import model.telluric_identification as telluric_id
import preprocessing.divide_orders as divide_orders
import preprocessing.normalize as normalize
import visualize.plot_PCCs as plot_PCCs
import visualize.plot_regressions as plot_regressions
import visualize.plot_shards as plot_shards

def calibration():

    # 1) LOAD DATA
    # Load external data for calibration. External data is: i) configuration
    # file, ii) filenames of calibration spectra, iii) contents of calibration
    # spectra. Loads calibration spectra contents into a data container for 
    # each order. These data containers are called shards. Produces a 
    # dictionary linking each processed order to its shard.
    config = yaml.safe_load(file("config/config.yml", "r"))
    filenames = load_fits.get_fits_filenames_at_path(config)
    order_shards = load_fits.load_fits_orders(filenames, config)
    plot_shards.plot_shards(order_shards, "wavelength", "log", config["plot_spectra_by_order"])

    # 2) PREPROCESS DATA
    # i)  Subdivide each order shard into smaller shards based on sharding configuration given in
    #     the config file.
    # ii) Normalize each smaller shard.
    shards = divide_orders.divide_orders(order_shards, config)
    plot_shards.plot_shards(shards, "wavelength", "log", config["plot_spectra_by_shard"])
    normalize.normalize(shards)
    plot_shards.plot_shards(shards, "wavelength", "log", config["plot_normalized_shards"], 
                            "after normalization")

    # 3) IDENTIFY TELLURIC PIXELS
    # i)   Get calibration line/calibration line suite data.
    # ii)  Identify pixels with significant PCC with either a) a H20 calibration line or b) z.
    # iii) Remove all 1 and 2 telluric pixel clusters.
    # iv)  Remove all telluric clusters not in the shape of a Gaussian trough.
    # v)   Remove all telluric clusters more than 1nm from another cluster.
    # vi)  Mark each cluster as non-water, water, or both.
    calibrators = telluric_id.generate_calibrators(shards, config)
    k = telluric_id.compute_PCC_threshold(config["p_value"], config["threshold_k_db_path"])
    telluric_id.flag_high_PCC_pixels(calibrators, k, shards, config)
    cluster_analysis.identify_clusters(shards)
    plot_PCCs.plot_PCCs(shards, "water", config["plot_water_PCCs"])
    plot_PCCs.plot_PCCs(shards, "airmass", config["plot_z_PCCs"])
    plot_PCCs.plot_PCCs_flag_sig(shards, "water", config["plot_water_PCCs_flag_sig"])
    plot_PCCs.plot_PCCs_flag_sig(shards, "airmass", config["plot_z_PCCs_flag_sig"])
    cluster_analysis.remove_1_and_2_pixel_clusters(shards)
    cluster_analysis.remove_non_trough_clusters(shards, config)
    cluster_analysis.remove_isolated_clusters(shards)
    
    # 4) EXPAND CLUSTERS
    # Expand each cluster by one pixel on either side to pick up pixels in its line's tail.
    cluster_analysis.expand_clusters(shards)
    fp_ttl = "w/ fp removal (& expansion)"
    plot_PCCs.plot_PCCs_flag_sig(shards, "water", config["plot_water_PCCs_flag_sig_no_fp"], fp_ttl)
    plot_PCCs.plot_PCCs_flag_sig(shards, "airmass", config["plot_z_PCCs_flag_sig_no_fp"], fp_ttl)

    # 5) RESOLVE OVERLAPPING CLUSTERS
    # Resolve overlapping water and non-water clusters.
    cluster_analysis.resolve_same_class_overlapping_clusters(shards)
    cluster_analysis.resolve_diff_class_overlapping_clusters(shards)
    plot_PCCs.plot_px_classification(shards, config["plot_px_classification"])

    # 6) GENERATE REGRESSION MODEL
    # Generate a regression model for each telluric pixel.
    regression_model.find_regression_coeffs(shards, calibrators)
    plot_regressions.plot_regressions(calibrators, shards, config)
    
    # 7) WRITE MODEL TO DATABASE
    # Write out model to database.
    write_db.write_db(shards, calibrators, config)
    
if __name__ == "__main__":
    calibration()
