import data_containers.shard as shi

###########
# Globals #
###########

# Indices of calibrator lines in config file
ADDR_IND = 0
PX_IND = 1

def get_calibrators(config):

    '''
    Saves the calibrator pixels given in the config file in the form (order, px).
    '''

    cal_pxs = []
    for calibrator in config["reduction_calibrators"]:
        cal_pxs.append((calibrator[ADDR_IND][shi.ORD_IND],
                       calibrator[ADDR_IND][shi.LOPX_IND] + calibrator[PX_IND]))
    return cal_pxs
