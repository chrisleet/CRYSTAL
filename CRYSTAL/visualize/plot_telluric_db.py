from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np

import load_store.db_indicies as dbi

def plot_telluric_db(db, config):

    '''
    Plots the telluric database as a block plot.

    Plots each telluric pixel in the database as a block plot.
    Water telluric pixels are colored blue, non-water pixels are colored
    red, and composite pixels are colored purple.
    '''
    
    Y_MAX = 44 #Reddest order to display
    CLASS_TO_FLOAT = {"w":0.3, "z":0.6, "c":1.0} #Convert classes to integers
    
    img = np.zeros((Y_MAX+1, config["pixels_per_order"]))
    
    for record in db:
        img[record[dbi.ORD_IND], record[dbi.PX_IND]] = CLASS_TO_FLOAT[record[dbi.CLS_IND]]

    cm_list = ((0.0, "white"), (0.3, "blue"), (0.6, "red"), (1.0, "purple"))
    cm = LinearSegmentedColormap.from_list("telluric_classes", cm_list, N=4)

    fig, ax = plt.subplots()
    i_ax = ax.imshow(img, cmap=cm, aspect='auto', origin='lower', vmin=0.0, vmax=1.0)
    #cb = fig.colorbar(i_ax)  #Uncomment to show colorbar
    plt.xlabel("Pixels in order")
    plt.ylabel(r'Wavelength, ($\AA$)')
    plt.title("Pixels in telluric database")
    ax.set_yticklabels(["alpha", 4505, 4692, 4896, 5119, 5362, 5631, 5927, 6256, 6624])
    plt.show()
