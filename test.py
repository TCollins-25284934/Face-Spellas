import MAD
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

calibrated = MAD.calibrate_exposure(2505)
MAD.show_chip(calibrated,0)
MAD.difference(calibrated,2505)
MAD.histogram_overlay(calibrated[0], 2505)
#
calibrated2 = MAD.calibrate_exposure(2507)
MAD.show_chip(calibrated2, 0)
MAD.difference(calibrated2,2507)
MAD.histogram_overlay(calibrated2[0], 2507)

calibrated3 = MAD.calibrate_exposure(2508)
MAD.show_chip(calibrated3, 0)
MAD.difference(calibrated3,2508)
MAD.histogram_overlay(calibrated3[0], 2508)

MAD.cosmic_ray_removal(calibrated,calibrated2,calibrated3,chip=0)

MAD.show_chip(calibrated,1)
MAD.show_chip(calibrated2,1)
MAD.show_chip(calibrated3,1)
MAD.cosmic_ray_removal(calibrated,calibrated2,calibrated3,chip = 1)



