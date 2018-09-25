import csv
import os

import model.generate_model as mi

def format_record(r):

    '''
    Generates a formatted record for a set of record values.
    '''

    order_fmt = "{:0=2d}".format(r[mi.ORD_IND])
    px_fmt = "{:0=4d}".format(r[mi.PX_IND])
    wv_fmt = "{:.2f}".format(r[mi.WV_IND])
    intensity_fmt = "{:.4f}".format(r[mi.INT_IND])

    return [order_fmt, px_fmt, wv_fmt, r[mi.CLS_IND], intensity_fmt]

def write_spectrum(filenames, model):

    '''
    Writes the telluric spectrum for a single stellar line as filename_tel.csv

    This database contains a single relation which contains a record for each
    telluric pixel detected. This relation's attributes are, in order:

    order ordpx wavelength class intensity

    where:
        ordpx is the telluric pixel's pixel number in its order
        wavelength is the average wavelength of the pixel in the training data
        class flags whether the pixel is water, non-water or composite
        and intensity is the telluric pixel's intensity
    '''
    
    filename = filenames[0] #  Only one file in filenames
    csv_file = open("./" + os.path.basename(os.path.splitext(filename)[0]) + "_tel.csv", "wb")
    csv_writer = csv.writer(csv_file, delimiter=" ", quotechar="'", quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["order", "px", "wavelength", "class", "intensity"])

    for r in model:
        csv_writer.writerow(format_record(r))

    csv_file.close()
            
        
