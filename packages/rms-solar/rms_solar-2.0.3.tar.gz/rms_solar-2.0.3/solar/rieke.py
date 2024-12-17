################################################################################
# solar/rieke.py: Solar model of Rieke et al. 2008, AJ 135, 2245
################################################################################

import os

import astropy.io.fits as pyfits
import solar
import tabulation as tab

# Read the file
filepath = os.path.join(os.path.split(solar.__file__)[0],
                        'data_files', 'rieke-solar_spec.fits')
hdulist = pyfits.open(filepath)
try:
    table = hdulist[1].data
    wavelength = table['WAVELENGTH']    # Angstroms
    flux = table['FLUX']                # erg/s/cm^2/A
finally:
    hdulist.close()

FLUX_DENSITY = tab.Tabulation(wavelength, flux)
UNITS = 'erg/s/cm^2/A'
XUNITS = 'A'

################################################################################
