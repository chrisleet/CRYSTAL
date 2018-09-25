# CRYSTAL v0.12
CRYSTAL: CRYSTAL Removes Your Spectrum's Terrestrial Atmospheric Lines

CRYSTAL is an open source, empirical program for identifying and removing telluric lines in stellar spectra.

## Repository structure
CRYSTAL: Contains the CRYSTAL program.<br>
config: Contains configuration files for CRYSTAL.<br>
example_telluric_db.csv: A premade telluric db for reference and learning.<br>
LICENSE: License of use.<br>

## Available functions
(Note: All function calls are made from the base directory)
```
CRYSTAL/calibration
```
Takes the set of B-star spectra and learns outputs a model of the telluric spectrum. This model is a table where each record represents a telluric pixel and contains its location, wavelength, whether it is a water or airmass pixel, and its PCC and regression model with either the water calibration line or airmass.

```
CRYSTAL/plot_telluric_db
```
Plots each telluric pixel in the model’s database as a block plot. Water telluric pixels are colored blue, non-water pixels are colored red, and composite pixels are colored purple. 

```
CRYSTAL/plot_telluric_range <lo_wavelength> <hi_wavelength>
```
Takes the wavelength range (```<lo_wavelength>```, ```<hi_wavelength>```) and plots the model’s database's telluric spectrum for an average airmass and PWV within that range. Water telluric pixels are colored blue, non-water pixels are colored red, and composite pixels are colored purple.

```
CRYSTAL/generate_telluric_model <science spectrum>
```
Takes the science spectrum ```<science spectrum>``` and the model database given in the config file and fits the model’s telluric spectrum to the science spectrum. Returns the fitted model as the csv file: ```<science spectrum>_tel.fits```
  
For more information, check out the wiki!
