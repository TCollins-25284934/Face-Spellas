import pathlib
import matplotlib.pyplot as plt
from astropy.io import fits
here = pathlib.Path('.')
my_list = list(here.iterdir())

def load_calibration_files(index, key):
    index = str(index)
    file_stem = "ubai" + index + "m_"
    subfolder = "*/ubai"+ index + "*/*.fits"
    cal_files = list(here.rglob(subfolder))
    stems = [file.stem.replace(file_stem, "").replace("file", "") for file in cal_files]
    new_dict = dict(zip(stems, cal_files))
    return new_dict[key]

mask = fits.open(load_calibration_files(2505, "mask"))
raw = fits.open(load_calibration_files(2505, "raw"))
print(mask)

fig, ax = plt.subplots(figsize=(12, 5))
#
ax.imshow(raw, origin='lower', cmap='gray')
ax.set_title('Raw Image')
#
# ax[1].imshow(mask, origin='lower')
# ax[1].set_title('Mask')
#
# plt.show()

def main():
    # load_calibration_files(2507)
    pass
if __name__ == '__main__':
    main()

