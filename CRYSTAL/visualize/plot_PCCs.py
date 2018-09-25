import matplotlib.pyplot as plt
import numpy as np

import utility.utility as utility

def plot_PCCs(shards, PCC_type, show=False):

    '''
    Plot each shard's pixels colored by PCC.
    '''

    if not show:
        return 

    for shard in shards.itervalues():
        plot_shard_PCCs(shard, PCC_type)

def plot_shard_PCCs(shard, PCC_type):

    '''
    Plot a shard's pixels colored by PCC.
    '''

    cmap = plt.get_cmap('Spectral_r')

    fig = plt.figure(facecolor = 'white')
    for spectrum in shard.spectra.itervalues():
        if PCC_type == "water":
            plt.scatter(spectrum.lin_x, spectrum.log_y, c=shard.w_PCCs, 
                        vmin=0.0, vmax=1.0, cmap=cmap)
        elif PCC_type == "airmass":
            plt.scatter(spectrum.lin_x, spectrum.log_y, c=shard.z_PCCs, 
                        vmin=0.0, vmax=1.0, cmap=cmap)
        else:
            raise Exception("Could not plot unrecognized PCC type")

    plt.title("Order {}, px {}-{} PCC with {} calibrator".format(shard.order, shard.lo_px, 
                                                                 shard.hi_px, PCC_type))
    plt.xlabel("Wavelength (Angstroms)")
    plt.ylabel("Log Space Signal Intensity")
    cb = plt.colorbar()
    cb.set_label("PCC with {} calibrator".format(PCC_type))
    plt.tight_layout()
    plt.show()
    

def plot_PCCs_flag_sig(shards, PCC_type, show=False, title=""):

    '''
    Plots each shard colored by px PCC, w/ cluster px highlighted.

    The spectrum in the shard are coadded to create a single 'average' 
    spectrum to make data easier to see. Each pixel in the coadded spectrum is
    then colored by its PCC, and finally pixels in the telluric clusters of 
    type PCC_type are highlighted by coloring them black.
    '''

    if not show:
        return

    for shard in shards.itervalues():
        plot_shard_PCCs_flag_sig(shard, PCC_type, title)


def plot_shard_PCCs_flag_sig(shard, PCC_type, title):

    '''
    Plots each shard colored by px PCC, w/ cluster px highlighted.

    (Worker function of plot_PCCs_flag_sig)
    '''

    # 1) Coadd spectrum
    coadded_x, coadded_y = utility.coadd_spectrum(shard)

    # 2) Plot coadded spectrum's PCCs with cluster PCCs in black
    cmap = plt.get_cmap('Spectral_r')
    fig = plt.figure(facecolor='white')
    plt.xlabel("Wavelength (Angstroms)")
    plt.ylabel("Signal strength")
    plt.title("Order {} px{}-{} (coadded), sig PCCs flagged {} {}".format(shard.order, shard.lo_px,
                                                                          shard.hi_px, PCC_type, 
                                                                          title))
    if PCC_type == "water":
        for cluster in shard.w_clusters:
            cluster_px = range(cluster[0], cluster[1]+1)
            plt.scatter(coadded_x[cluster_px], coadded_y[cluster_px], color="k", zorder=2)
        plt.scatter(coadded_x, coadded_y, c=shard.w_PCCs, 
                    vmin=0.0, vmax=1.0, cmap=cmap, zorder=1)
    else:
        for cluster in shard.z_clusters:
            cluster_px = range(cluster[0], cluster[1]+1)
            plt.scatter(coadded_x[cluster_px], coadded_y[cluster_px], color="k", zorder=2)
        plt.scatter(coadded_x, coadded_y, c=shard.z_PCCs, 
                    vmin=0.0, vmax=1.0, cmap=cmap, zorder=1)

    cb = plt.colorbar()
    cb.set_label("Pixel PCC with {}".format(PCC_type))
    plt.plot(coadded_x, coadded_y, color="orange", zorder=3)    
    plt.show()



def plot_px_classification(shards, show=False):
    
    if not show:
        return

    for shard in shards.itervalues():
        plot_shard_px_classification(shard)

def plot_shard_px_classification(shard):

    '''
    Plots each shard colored by classifaction type.

    The spectrum in the shard are coadded to create a single 'average'
    spectrum to make data easier to see. Pixels in airmass clusters are colored
    red, pixels in water clusters are colored blue,  pixels in composite 
    clusters are colored purple.
    '''

    coadded_x, coadded_y = utility.coadd_spectrum(shard)

    fig = plt.figure(facecolor='white')
    plt.xlabel("Wavelength (Angstroms)")
    plt.ylabel("Signal strength")
    plt.title("Order {} px{}-{} (coadded) pixel classification".format(shard.order, shard.lo_px,
                                                                       shard.hi_px))
    plt.scatter(coadded_x, coadded_y, color="k", zorder=1)
    plt.plot(coadded_x, coadded_y, color="orange", zorder=3)

    for cluster in shard.w_clusters:
        cluster_px = range(cluster[0], cluster[1]+1)
        plt.scatter(coadded_x[cluster_px], coadded_y[cluster_px], color="b", zorder=2)

    for cluster in shard.z_clusters:
        cluster_px = range(cluster[0], cluster[1]+1)
        plt.scatter(coadded_x[cluster_px], coadded_y[cluster_px], color="r", zorder=2)

    for cluster in shard.c_clusters:
        cluster_px = range(cluster[0], cluster[1]+1)
        plt.scatter(coadded_x[cluster_px], coadded_y[cluster_px], color="purple", zorder=2)

    plt.show()

    
