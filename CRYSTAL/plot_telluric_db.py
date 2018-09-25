import sys
import yaml

import load_store.read_argv as read_argv
import load_store.read_db as read_db
import visualize.plot_telluric_db

def plot_telluric_db():

    '''
    Plots the telluric database as a block plot.

    Plots each telluric pixel in the database as a block plot.
    Water telluric pixels are colored blue, non-water pixels are colored 
    red, and composite pixels are colored purple. 
    '''

    # 1) LOAD DATA
    config = yaml.safe_load(file("config/config.yml", "r"))
    db = read_db.read_db(config)
    visualize.plot_telluric_db.plot_telluric_db(db, config)
    

if __name__ == "__main__":
    plot_telluric_db()
    
