import numpy as np

import load_store.db_indicies as dbi

###########
# Globals #
###########

#Indices of fields in spectrum model
ORD_IND = 0
PX_IND = 1
WV_IND = 2
CLS_IND = 3
INT_IND = 4

def generate_model(mu, z, db, config):

    '''
    Combine mu and z values with telluric db to generate telluric model
    '''

    model = []

    for record in db:
        if record[dbi.CLS_IND] == "w":
            f_w  = np.poly1d([record[dbi.RM_IND], record[dbi.RC_IND]])
            lin_intensity = np.exp(f_w(mu))
        elif record[dbi.CLS_IND] == "z":
            f_z  = np.poly1d([record[dbi.RM_IND], record[dbi.RC_IND]])
            lin_intensity = np.exp(f_z(z))
        elif record[dbi.CLS_IND] == "c":
            intensity = -1
        if record[dbi.CLS_IND] == "c" or lin_intensity < 1.0 - config["min_model_depth"]:
            model.append(record[dbi.ORD_IND:dbi.CLS_IND+1] + [lin_intensity])
    return model
            
        
        
