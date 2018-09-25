import numpy as np

###########
# Globals #
###########

# NULL PCC value
NULL_INT = -10

# Indicies of shard address tuple
ORD_IND = 0
LOPX_IND = 1
HIPX_IND = 2

class Shard():

    '''
    A shard is the primary data container for the telluric calibration code.

    A shard holds all data for a given range of wavelengths (e.g. spectra,
    PCCs of pixels, linear regression coefficients, etc.)

    Parameters
    ----------
    order: int
        The Echelle order the shard's data comes from.

    lo_px: int
        The low pixel number in the shard's range of pixels.

    hi_px: int
        The high pixel number in the shard's range of pixels.

    Attributes
    ---------
    order: int
        (see parameters)

    lo_pixel: int
        (see parameters)

    hi_pixel: int
        (see parameters)

    spectra: dict
        A dictionary mapping each calibration filename to a Spectrum_Data 
        object which contains its data.

    w_PCCs: list (floats)
        The PCC of each pixel in the shard with the water calibrator.

    w_tel: list (booleans)
        Flags denoting whether each pixel has a water telluric component.

    w_clusters: list (tuples)
        Tuples giving the range of each cluster of water pixels in a spectrum.
        Note that w, z, and composite clusters are non-overlapping after 
        processing.

    z_PCCs: list (floats)
        The PCC of each pixel in the shard with airmass.

    z_tel: list (booleans)
        Flags denoting whether each pixel has an air telluric component.

    z_clusters: list (tuples)
        Tuples giving the range of each cluster of z pixels in a spectrum.
        Note that w, z, and composite clusters are non-overlapping after
        processing.

    c_clusters: list (tuples)
        Tuples giving the range of each cluster of composite w-z pixels in a 
        spectrum. Note that w, z, and composite clusters are non-overlapping
        after processing.

    w_coeffs: dict (int -> tuple)
        Maps each water telluric pixel to a tuple containg the coeffcients
        in its linear regression model against the selected calibration 
        pixel. The tuple, t, represents the coefficients in the regression
        as y = t[0]*x + t[1].

    z_coeffs: dict (int -> tuple)
        Maps each water telluric pixel to a tuple containg the coeffcients
        in its linear regression model against airmass (see w_coeffs).
    '''

    def __init__(self, order, lo_px, hi_px):
        self.order = order
        self.lo_px = lo_px
        self.hi_px = hi_px

        self.spectra = {}
        self.w_PCCs = np.zeros(hi_px - lo_px) + NULL_INT
        self.w_tel = np.zeros(hi_px - lo_px, dtype=bool)
        self.w_clusters = []
        self.z_PCCs = np.zeros(hi_px - lo_px) + NULL_INT
        self.z_tel = np.zeros(hi_px - lo_px, dtype=bool)
        self.z_clusters = []
        self.c_clusters = []
        self.w_coeffs = {}
        self.z_coeffs = {}

class Spectrum_Data():

    '''
    Stores the data associated with a file in a shard's wavelength range.

    Parameters
    ----------

    lin_x: array (float)
        Spectrum wavelength data
    
    lin_y: array (float)
        Spectrum intensity data in linear space

    log_y: array (float)
        Spectrum intensity data in log space

    z: float
        Spectrum airmass

    Attributes
    ----------
    lin_x: array (float)
        (see parameters)

    lin_y: array (float)
        (see parameters)

    log_y: array (float)
        (see parameters)

    z: float
        (see parameters)
    '''
    
    def __init__(self, lin_x, lin_y, log_y, z):
        self.lin_x = lin_x
        self.lin_y = lin_y
        self.log_y = log_y
        self.z = z
