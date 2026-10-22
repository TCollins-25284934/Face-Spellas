import pathlib
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

here = pathlib.Path(".")

def load_calibration_files(index, key):
    index = str(index)
    file_stem = "ubai" + index + "m_"
    subfolder = "*/ubai"+ index + "*/*.fits"
    cal_files = list(here.rglob(subfolder))
    stems = [file.stem.replace(file_stem, "").replace("file", "") for file in cal_files]
    new_dict = dict(zip(stems, cal_files))
    return new_dict[key]


def image_extract(filename, ext):

    with fits.open(filename) as hdul:
        data = hdul[ext].data.astype(float)

    return data


def apply_mask(raw, mask):
    corrected = raw.copy()

    corrected[mask != 0] = np.nan

    return corrected


def get_blev_values(blev_chip):

    overscan = blev_chip[9:790, 8:14]


    odd_bias = np.mean(overscan[:, ::2])
    even_bias = np.mean(overscan[:, 1::2])

    return odd_bias, even_bias


def apply_blev_correction(raw, blev_file):

    corrected = raw.copy()

    with fits.open(blev_file) as hdul:

        for chip in range(4):

            blev_chip = hdul[chip + 1].data.astype(float)

            odd_bias, even_bias = get_blev_values(blev_chip)

            corrected[chip, :, ::2] -= odd_bias
            corrected[chip, :, 1::2] -= even_bias

    return corrected


def subtract_bias(image, bias_cube):

    return image - bias_cube


def subtract_dark(image, dark_cube, raw_file):
    with fits.open(raw_file) as hdul:
        header = hdul[0].header
    return image - dark_cube*hdul[0].header.get("EXPTIME")



def apply_flat(image, flat_cube):
    return image * flat_cube


def subtract_sky(image, background):
    return image - background


def calibrate_exposure(index):
    raw_file = load_calibration_files(index, "raw")
    mask_file = load_calibration_files(index, "mask")
    blev_file = load_calibration_files(index, "blev")
    bias_file = load_calibration_files(index, "bias")
    dark_file = load_calibration_files(index, "dark")
    flat_file = load_calibration_files(index, "flat")

    raw = image_extract(raw_file, 1)
    mask = image_extract(mask_file, 0)
    bias = image_extract(bias_file, 0)
    dark = image_extract(dark_file, 0)
    flat = image_extract(flat_file, 0)

    image = apply_mask(raw, mask)

    image = apply_blev_correction(
        image,
        blev_file
    )

    image = subtract_bias(
        image,
        bias
    )

    image = subtract_dark(
        image,
        dark, raw_file
    )

    image = apply_flat(
        image,
        flat
    )

    sky = get_sky(raw[0])
    image = subtract_sky(image, sky)
    image = transform_by('sqrt', image, pmin=1, pmax=99)
    # image = transform_by('log', image, pmin=15, pmax=85)


    return image


def show_chip(image_cube, chip=0):

    fig, ax = plt.subplots(figsize=(8, 8))

    image = image_cube[chip,:, :]

    ax.imshow(
        image,
        origin="lower",
        vmin=np.nanpercentile(image, 1),
        vmax=np.nanpercentile(image, 99)
    )
    # ax.imshow(
    #     image,
    #     origin="lower"
    # )

    ax.set_title(f"Chip {chip}")

    plt.tight_layout()
    plt.show()


def normalize_data(x, pmin=None, pmax=None):
    """
    normalize data between 0 and 1, optionally clipping the original data
    between user-specified min/max values, or percentiles

    Parameters:
    -----------
    x: np.ndarray
        The data to normalize
    dmin: float or None
        The minimum data value to use for normalization
    dmax: float or None)
        The maximum data value to use for normalization
    percentiles: list, tuple, int, or None
        Instead of using manual dmin/dmax values, use percentiles instead

    Returns:
    -----------
    norm: np.ndarray
        data normalized to [0, 1]
    dmin, dmax: float, float
        min/max values used for normalization
    """
    res = np.asarray(x, dtype=np.float64)
    # quick fix: np.percentile will complain if pmin, pmax are None!
    # if no pmin/pmax values are passed, we'll just assume they want
    # the global min and max values
    if not pmin:
        pmin = 0
    if not pmax:
        pmax = 100

    # vmin, vmax = np.percentile(res, [pmin, pmax])
    vmin, vmax = np.nanpercentile(res, [pmin, pmax])
    # basic min-max normalization here
    norm = (res - vmin) / (vmax - vmin)
    norm = np.clip(norm, 0, 1)

    # make sure it's definitely between 0 and 1
    return np.clip(norm, 0, 1)


def transform_by(func, x, pmin=None, pmax=None):
    """
    transform/stretch the data by a named function,
    normalizing the data if necessary

    Parameters:
    -----------
    func: str
        one of 'linear', 'sqrt' or 'log'
    x: np.ndarray
        data to transform
    pmin: int, float, or None
        lower percentile to use for min/max normalization
    pmax: int, float, or None
        upper percentile to use for min/max normalization
    Returns:
    ----------
    out : np.array
        the transformed data
    """

    x_norm = normalize_data(x, pmin=pmin, pmax=pmax)
    if func.lower() == 'sqrt':
        return np.sqrt(x_norm)
    elif func.lower() == 'log':
        scale = 1000
        log_scaled = np.log10(1 + scale * x_norm) / np.log10(1 + scale)
        return log_scaled
    elif func.lower() == 'linear':
        return x_norm
    else:
        raise ValueError("Unsupported function: ", func)

def filter_mad(sample, threshold=3):
    """
    compute the simple MAD and clip the data

    Parameters:
    -----------
    sample : np.array
        the sample data to clip
    threshold : int, float
        the number of MADs to apply for clipping
    Returns:
    -----------
    flag : np.ndarray
        a mask of flagged values
    """
    median = np.nanmedian(sample)
    mad = np.nanmedian(np.abs(sample - median))
    stddev = 1.4826 * mad

    # flag = (sample - median) > (threshold * stddev)
    flag = (sample - median) / stddev > threshold
    print(f"MAD thresholding produced {flag.sum()} values above the threshold")
    return flag

def filter_stddev(sample, threshold=3):
    """
    compute the simple stddev and clip the data

    Parameters:
    -----------
    sample : np.array
        the sample data to clip
    threshold : int, float
        the number of MADs to apply for clipping
    Returns:
    -----------
    flag : np.ndarray
        a mask of flagged values
    """
    mean = np.nanmean(sample)
    stddev = np.nanstd(sample)
    flag = (sample - mean) / stddev > threshold
    print(f"STDDEV thresholding produced {flag.sum()} values above threshold")
    return flag


def filter_by(data, kind='mad', thresh=3):
    """ a wrapper to call either of the above functions """
    if kind.lower() == 'mad':
        filtered = filter_mad(data, thresh)
    elif kind.lower() in ['std', 'stddev']:
        filtered = filter_stddev(data, thresh)
    return filtered

# madmask = filter_by('mad', pc_data, 3)
# stdmask = filter_by('std', pc_data, 3)

def get_sky(image):
    flag = filter_by(image, 'mad', 3)
    pc_data_masked = np.ma.masked_array(image, mask=flag)
    # fig, ax = plt.subplots(figsize=(7, 7))
    # ax.imshow(pc_data_masked, origin='lower')
    # plt.show()
    return pc_data_masked

def main():
    raw_file = load_calibration_files(2505, "raw")
    # mask_file = load_calibration_files(2505, "mask")
    # blev_file =load_calibration_files(2505, "blev")
    # bias_file = load_calibration_files(2505, "bias")
    # dark_file = load_calibration_files(2505, "dark")
    # flat_file = load_calibration_files(2505, "flat")
    #
    # mask = image_extract(mask_file, 0)
    raw = image_extract(raw_file, 1)
    # dark = image_extract(dark_file, 0)
    # flat = image_extract(flat_file,0)
    # bias = image_extract(bias_file, 0)
    #
    # corrected1 = apply_mask(raw, mask)
    # corrected2 = apply_blev_correction(corrected1, blev_file)
    # corrected3 = subtract_dark(corrected2, dark, raw_file)
    # corrected4= apply_flat(corrected3, flat)
    # corrected5 = subtract_bias(corrected4, bias)


    calibrated = calibrate_exposure(2505)
    # pc_norm = normalize_data(corrected, pmin=1, pmax=99)
    # pc_norm.min(), pc_norm.max(), np.median(pc_norm)
    # print(calibrated.shape)
    show_chip(calibrated, chip=1)

    # plt.figure(figsize=(8, 8))
    # plt.imshow(pc_norm[1],
    #            origin="lower")
    # plt.show()
    # raw_sqrt = transform_by(
    #     'sqrt',
    #     raw,
    #     pmin=1,
    #     pmax=99
    # )

    # pc_sqrt1 = transform_by(
    #     'sqrt',
    #     corrected1,
    #     pmin=1,
    #     pmax=99
    # )
    # pc_sqrt2 = transform_by(
    #     'sqrt',
    #     corrected2,
    #     pmin=1,
    #     pmax=99
    # )
    # pc_sqrt3 = transform_by(
    #     'sqrt',
    #     corrected3,
    #     pmin=1,
    #     pmax=99
    # )
    # pc_sqrt4 = transform_by(
    #     'sqrt',
    #     corrected4,
    #     pmin=5,
    #     pmax=95
    # )
    # pc_sqrt5 = transform_by('sqrt', corrected5, pmin=5, pmax=95)
    #
    # fig, ax = plt.subplots(figsize=(8, 8))
    # ax.imshow(pc_sqrt1[1], origin='lower')
    # plt.title("1")
    # plt.show()
    # plt.imshow(pc_sqrt2[1],
    #            origin='lower')
    # plt.title("2")
    # plt.show()
    # plt.imshow(pc_sqrt3[1],
    #            origin='lower')
    # plt.title("3")
    # plt.show()
    # plt.imshow(pc_sqrt4[1],
    #            origin='lower')
    # plt.title("4")
    # plt.show()
    # plt.imshow(pc_sqrt5[1],
    #            origin='lower')
    # plt.title("5")
    # plt.show()
    data_file = 'hst-data/F336W/ubai2505m_c0m_aligned.fits'
    # we will use context management here
    # with fits.open(data_file) as hdul:
    #     # header = hdul[0].header
    #     data = hdul[1].data
    # pc_data = data[0].copy()
    # pc_sqrt = transform_by('sqrt', pc_data, pmin=1, pmax=99)
    # pc_log = transform_by('log', pc_data, pmin=1, pmax=95)
    # fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 7))
    # ax1.imshow(pc_sqrt, origin='lower')
    # ax2.imshow(pc_log, origin='lower')
    # ax1.set_title('sqrt normalizatin')
    # ax2.set_title('log10 normalizatin')

    with fits.open(data_file) as hdul:
        reference = hdul[1].data.astype(float)

    mine = calibrated[0]

    ref_display = transform_by('sqrt', reference, pmin=1, pmax=99)
    # my_display = transform_by('sqrt', mine, pmin=1, pmax=99)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.imshow(mine, origin='lower')
    ax1.set_title("My calibration")

    ax2.imshow(ref_display, origin='lower')
    ax2.set_title("HST reference product")

    plt.show()

    difference = mine - reference
    plt.imshow(
        difference,
        origin="lower",
        vmin=np.nanpercentile(difference, 5),
        vmax=np.nanpercentile(difference, 95)
    )
    plt.colorbar()
    plt.title("Difference")
    plt.show()
    # get_sky(raw[0])


if __name__ == "__main__":
    main()