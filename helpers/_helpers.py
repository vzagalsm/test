import os
import subprocess

__all__ = ['hide_deprecationWarnings','hide_nonfunctionalWarnings','hide_FITSwarnings','hide_ComparisonWarnings','correct_velo_info']


###################################################################################################

# switch of deprecation warnings
################################

def hide_deprecationWarnings():
    try:
        from matplotlib.cbook import MatplotlibDeprecationWarning
        import warnings
        warnings.simplefilter('ignore', MatplotlibDeprecationWarning)
    except:
        raise Warning("easy_aplpy: Could not switch off MatplotlibDeprecationWarnings.These are raised because of aplpy but cause no harm.")


def hide_nonfunctionalWarnings():
    try:
        import warnings
        warnings.filterwarnings("ignore", message="This method is not functional at this time")
        warnings.filterwarnings("ignore", message="WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
        warnings.filterwarnings("ignore", message="No labelled objects found.")
    except:
        raise Warning("easy_aplpy: Could not switch off aplpy warnings about non-functional methods. They do NOT affect easy_aplpy.")


def hide_FITSwarnings():
    try:
        import warnings
        warnings.filterwarnings("ignore", message="PC01_01 = 1.000000000000E+00 indices in parameterized keywords must not have leading zeroes.")
    except:
        raise Warning("easy_aplpy: Could not switch off aplpy warnings about leading zeros in FITS header. They do NOT affect plotting at all.")


def hide_ComparisonWarnings():
    try:
        import warnings
        warnings.filterwarnings("ignore", message="invalid value encountered in less")
        warnings.filterwarnings("ignore", message="Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal")
    except:
        raise Warning("easy_aplpy: Could not switch off aplpy comparison warnings. These are raised within aplpy and do NOT affect plotting at all.")


###################################################################################################

# correct velocity header
#########################

def correct_velo_info(pv, overwrite=True):

    """
    convert_velo_info: scale the velocity axis in pV diagrams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    CASA position-velocity diagrams are exported in m/s which is inconvenient
    because the tick labels get very long. This function converts the velocity
    axis to km/s by changing the header.
    !!! Note that aplpy in order to display the velocity correctly requires
    !!! overcorrecting. This seems to be a bug somewhere in aplpy or the FITS
    !!! images. The resulting images are off by a factor of 1000, 100km/s are
    !!! given as 0.1km/s in the FITS header but aplpy shows it as 100km/s.
    It is recommended to use the "corrected" images for plotting only.

    Mandatory arguments:
        pv          Path and file name of a single pV diagram as FITS file or a list
                    of multiple FITS images.

    Optional arguments:
        overwrite   True or False. Default: True

    example:

    correct_velo_info(['file1.fits', 'file2.fits', file3.fits'],
        overwrite = False
        )
    """

    if isinstance(pv, str):
        pv_list = [pv]
    elif isinstance(pv, (list,tuple)):
        pv_list = pv
    else:
        raise TypeError('Input needs to be a single FITS file or list of FITS files.')

    for this_pv in pv_list:

        # get current velocity unit
        velounit = subprocess.check_output('gethead cunit2 '+this_pv, shell=True)

        # convert to km/s if necessary
        if (velounit == 'm/s\n'):
            if (overwrite == False):
                os.system('cp -r '+this_pv+' '+this_pv+'.corrected')
                this_pv = this_pv+'.corrected'

            crval_old = float(subprocess.check_output('gethead crval2 '+this_pv, shell=True))
            cdelt_old = float(subprocess.check_output('gethead cdelt2 '+this_pv, shell=True))
            crval_new = crval_old/1e6
            cdelt_new = cdelt_old/1e6
            cunit_new = 'km/s'
            os.system('sethead -kv CTYPE1=OFFSET CRVAL2='+'{:18.12E}'.format(crval_new)+' CDELT2='+'{:18.12E}'.format(cdelt_new)+' CUNIT2='+cunit_new+' '+this_pv)
            print('Unit is m/s. Corrrecting to km/s: '+this_pv)
            print('\tNote that the header is now wrong by a factor of 1e3!')
        elif (velounit == 'km/s\n'):
            print('Unit is km/s already: '+this_pv)
        else:
            raise TypeError('Unrecognized velocity unit: '+this_pv)


###################################################################################################
