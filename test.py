import HST_V2
import matplotlib.pyplot as plt
raw_file = MAD_easy.load_calibration_files(2505, "raw")
raw = MAD_easy.image_extract(raw_file, 1)
# print(raw.shape[0])
skies = HST_V2.get_sky(raw)
# print(skies)

calibrated = HST_V2.calibrate_exposure(2505)
image = calibrated[0]
image2 = calibrated[1]
image3 = calibrated[2]
image4 = calibrated[3]
calibrated = HST_V2.transform_by('sqrt', calibrated, pmin=1, pmax=99)
# HST_V2.show_chip(calibrated, 0)
# HST_V2.show_chip(calibrated, 1)
# HST_V2.show_chip(calibrated, 2)
# HST_V2.show_chip(calibrated, 3)




image = HST_V2.transform_by('sqrt', image, pmin=1, pmax=99)
image2 = HST_V2.transform_by('sqrt', image2, pmin=1, pmax=99)
image3 = HST_V2.transform_by('sqrt', image3, pmin=1, pmax=99)
image4 = HST_V2.transform_by('sqrt', image4, pmin=1, pmax=99)
fig, (ax1, ax2, ax3, ax4) = plt.subplots(ncols = 4,figsize=(8, 8))
ax1.imshow(calibrated[0], origin="lower")
ax2.imshow(calibrated[1], origin="lower")
ax3.imshow(calibrated[2], origin="lower")
ax4.imshow(calibrated[3], origin="lower")
fig, (ax5, ax6, ax7, ax8) = plt.subplots(ncols = 4,figsize=(8, 8))
ax5.imshow(image, origin="lower")
ax6.imshow(image2, origin="lower")
ax7.imshow(image3, origin="lower")
ax8.imshow(image4, origin="lower")
plt.show()