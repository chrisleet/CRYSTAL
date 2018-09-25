def view_tellurics_read_argv(argv):

    '''
    Reads the argv for the view_tellurics function.

    The view_tellurics function has two args in argv: argv[1] and argv[2],
    which are the start and end wavelengths to display tellurics and should
    be floats.
    '''

    if len(argv) < 3 or len(argv) > 3:
        raise Exception("python view_tellurics.py <start wavelength> <end wavelength>")

    try:
        st_wv = float(argv[1])
    except ValueError:
        raise Exception("Start wavelength {} not a float".format(argv[1]))

    try:
        end_wv = float(argv[2])
    except ValueError:
        raise Exception("End wavelength {} not a float".format(argv[2]))

    if st_wv >= end_wv:
        raise Exception("Start wavelength not less than end wavelength")
        
    return (st_wv, end_wv)
