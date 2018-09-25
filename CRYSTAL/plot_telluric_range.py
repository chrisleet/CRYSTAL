import sys
import yaml

import load_store.read_argv as read_argv
import load_store.read_db as read_db
import visualize.plot_telluric_range

def plot_telluric_range():

    '''
    Plots the tellurics in the database from argv[1]-argv[2] nm.

    Plot the database's telluric spectrum for an average airmass and PWV.
    Water telluric pixels are colored blue, non-water pixels are colored 
    red, and composite pixels are colored purple. 
    '''

    # 1) LOAD DATA
    config = yaml.safe_load(file("config/config.yml", "r"))
    db = read_db.read_db(config)
    wv_lo, wv_hi = read_argv.view_tellurics_read_argv(sys.argv)
    visualize.plot_telluric_range.plot_telluric_range(db, wv_lo, wv_hi)

if __name__ == "__main__":
    plot_telluric_range()
    
