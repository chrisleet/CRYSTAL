import data_containers.shard

def divide_orders(order_shards, config):

    '''
    Breaks each order shard up into smaller shards.

    Takes the orders fed into CRYSTAL, and divides them into smaller shards. This helps the 
    performance of certain modules such as baseline normalization.

    Parameters
    ----------
    order_shards: dict
        Dictionary containing the shards for each order.

    config: dict
        Configuration.

    Returns
    -------
    shards: dict
        Dictionary mapping from a tuple (order, lo_px, hi_px) to a shard with the section
        of wavelength in order order between lo_px and hi_px.
    '''

    #If user has set special sharding pixel ranges for a particular order (e.g. to avoid the NA-D
    #line) those sharding pixel ranges are used. Otherwise, the default sharding pixel ranges in
    #the config file are used.

    shards = {}
    for order, shard in order_shards.iteritems():
        if config["special_shard_ranges"] is not None and order in config["special_shard_ranges"]:
            for rng_start, rng_end in config["special_shard_ranges"][order]:
                shards[(order, rng_start, rng_end)] = take_shard_subsec(rng_start, rng_end, shard)
        else:
            for rng_start, rng_end in config["default_shard_ranges"]:
                shards[(order, rng_start, rng_end)] = take_shard_subsec(rng_start, rng_end, shard)
    return shards


def take_shard_subsec(rng_start, rng_end, shard):

    '''
    Creates a shard from the pixel range [rng_start, rng_end).
    '''
    
    subsec_shard = data_containers.shard.Shard(shard.order, rng_start, rng_end)
    for filename, spectrum in shard.spectra.iteritems():
        lin_x = spectrum.lin_x[rng_start:rng_end]
        lin_y = spectrum.lin_y[rng_start:rng_end]
        log_y = spectrum.log_y[rng_start:rng_end]
        z = spectrum.z
        subsec_spectrum = data_containers.shard.Spectrum_Data(lin_x, lin_y, log_y, z)
        subsec_shard.spectra[filename] = subsec_spectrum
    return subsec_shard
