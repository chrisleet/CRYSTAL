import matplotlib.pyplot as plt
import numpy as np

import load_store.db_indicies as dbi

def plot_shard(shard, y_scale, x_units, append_to_title):

    '''
    Plot the given shard

    Parameters
    ----------
    shards: dict
        Dictionary containing shards

    y_scale: str
       Specifies whether to plot y-axis in lin space or log space

    x_units: str
       Specifies whether to plot x-axis in pixels or angstroms

    append_to_title: str
       String to append to plot title.
    '''

    fig = plt.figure(facecolor='white')
    title = "Order:{}, px {}-{} spectra in {} space {}".format(shard.order, shard.lo_px, 
                                                               shard.hi_px, y_scale,
                                                               append_to_title)
    plt.title(title)
        
    for spectrum_name, spectrum in shard.spectra.iteritems():
        if x_units == "pixels":
            plt.xlabel("Pixels (Arbitrary 0)")
            if y_scale == "linear":
                plt.plot(spectrum.lin_y)
                plt.ylabel("Signal Intensity (linear space)")
            else:
                plt.plot(spectrum.log_y)
                plt.ylabel("Signal Intensity (log space)")

        elif x_units == "wavelength":
            plt.xlabel("Wavelength (Angstroms)")
            if y_scale == "linear":
                plt.plot(spectrum.lin_x, spectrum.lin_y)
                plt.ylabel("Signal Intensity (linear space)")
            else:
                plt.plot(spectrum.lin_x, spectrum.log_y)
                plt.ylabel("Signal Intensity (log space)")

        else:
            print "xUnits unrecognized"

    plt.show()


def plot_shards(shards, x_units, y_scale, show=False, append_to_title=""):
    
    '''
    Plot each shard in the shard dict.

    Parameters
    ----------
    shards: dict
        Dictionary containing shards

    x_units: str
       Specifies whether to plot x-axis in pixels or angstroms

    y_scale: str
       Specifies whether to plot y-axis in lin space or log space

    show: bool
       Flag specifying whether to suppress the plot.

    append_to_title: str
       String to append to plot title.
    '''

    if not show:
        return

    for shard in shards.itervalues():
        plot_shard(shard, y_scale, x_units, append_to_title)
        

def plot_shards_vs_xcorr_tel(db, shift, shards, show=False):

    '''
    Plots each shard against the xcorrelated, unfitted telluric model.
    '''

    if not show:
        return

    for shard in shards.itervalues():
        plot_shard_vs_xcorr_tel(db, shift, shard)

def plot_shard_vs_xcorr_tel(db, shift, shard):
    
    '''
    Plots a shard against the xcorrelated, unfitted telluric model.

    Worker function of plot_shards_vs_xcorr_tel.
    '''

    spectrum = shard.spectra.itervalues().next() #only one spectrum in shard

    db_spectrum = np.ones(len(spectrum.log_y))
    for record in db:
        px = record[dbi.PX_IND] + shift
        if record[dbi.ORD_IND] == shard.order and shard.lo_px <= px and px < shard.hi_px:
            db_spectrum[px - shard.lo_px] = np.exp(record[dbi.INT_IND])

    fig = plt.figure(facecolor = 'white')
    plt.plot(spectrum.lin_x, np.exp(spectrum.log_y), color='purple', label='CHIRON Spectrum')
    plt.plot(spectrum.lin_x, db_spectrum, label='Telluric Spectrum')
    plt.title("Order {} px {}-{}, spectrum and xcorr, unscaled telluric model".format(shard.order, 
                                                                                     shard.lo_px,
                                                                                     shard.hi_px))
    plt.xlabel("Wavelength (Angstroms)")
    plt.ylabel("Signal strength")
    plt.tight_layout()
    plt.legend()
    plt.show()
    
