import matplotlib.pyplot as plt
import numpy as np

import model.generate_model as mi

def plot_model(shift, shards, model, show=False):

    '''
    Plot telluric model against spectrum to be reduced.
    '''

    if not show:
        return

    for shard in shards.itervalues():
        plot_shard_model(shift, shard, model)

def plot_shard_model(shift, shard, model):

    '''
    Plot telluric model against spectrum to be reduced for shard.
    '''

    spectrum = shard.spectra.itervalues().next() #only one spectrum in shard

    shard_model = np.ones(len(spectrum.log_y))
    for row in model:
        px = row[mi.PX_IND]
        if row[mi.ORD_IND] == shard.order and shard.lo_px <= px and px < shard.hi_px:
            shard_model[px - shard.lo_px + shift] = row[mi.INT_IND]
            
    fig = plt.figure(facecolor = 'white')
    plt.plot(spectrum.lin_x, np.exp(spectrum.log_y), color='purple', label='CHIRON Spectrum')
    plt.plot(spectrum.lin_x, shard_model, label='Model')
    plt.title("Order {} px {}-{}, spectrum and telluric model".format(shard.order, shard.lo_px,
                                                                      shard.hi_px))
    plt.xlabel("Wavelength (Angstroms)")
    plt.ylabel("Signal strength")
    plt.tight_layout()
    plt.legend()
    plt.show()
