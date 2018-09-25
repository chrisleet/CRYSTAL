import csv
import os

import load_store.db_indicies as dbi

def read_db(config, read_calibrator_info=False):

    csv_file = open(os.path.join(config["cal_db_path"], config["cal_db_filename"]), 'rb')
    csv_reader = csv.reader(csv_file, delimiter=" ", quotechar="'")
    db = []
    current_record = csv_reader.next()
    for record in csv_reader:
        record[dbi.ORD_IND] = int(record[dbi.ORD_IND])
        record[dbi.PX_IND] = int(record[dbi.PX_IND])
        record[dbi.WV_IND] = float(record[dbi.WV_IND])
        record[dbi.PCC_IND] = float(record[dbi.PCC_IND])
        record[dbi.RM_IND] = float(record[dbi.RM_IND])
        record[dbi.RC_IND] = float(record[dbi.RC_IND])
        record[dbi.INT_IND] = float(record[dbi.INT_IND])
        db.append(record)
    return db
    
