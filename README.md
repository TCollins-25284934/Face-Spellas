# Face-Spella's
Space Fella's

Optical Detectors assignment: calibration of raw Hubble Space Telescope (HST) WFPC2 exposures, and analysis of Sentinel-2 images of the Hunga Tonga volcano. Each part has its own Jupyter notebook.

## Repository structure

```
Face-Spellas/
├── hst-data/
│   ├── calibration/          # raw exposures and their calibration files
│   │   ├── ubai2505m/        # *_raw, *_maskfile, *_blevfile, *_biasfile, *_darkfile, *_flatfile, *_atodfile
│   │   ├── ubai2507m/
│   │   └── ubai2508m/
│   ├── F336W/                # STScI pipeline images (*_c0m_aligned.fits) used for comparison
│   └── F555W/
├── hst-processed/            # FITS files written by hst-assignment.ipynb
├── sentinel-data/
│   ├── White_light/          # Google Earth images, named <year><month>.jpg (2014Feb ... 2023Oct)
│   ├── S2_2017-07-12/        # Sentinel-2 L2A bands (*_B01_Raw ... *_B12_Raw) and pipeline products (NDVI, NDWI, True_color, ...)
│   ├── S2_2018-07-12/
│   └── S2_2019-07-12/
├── sentinel-processed/       # masks and areas.csv written by sentinel-assignment.ipynb
├── hst-assignment.ipynb
├── sentinel-assignment.ipynb
├── ai-unedited-drafts.md     # my drafts of the AI language-edited markdown cells
└── README.md
```

## Requirements

Python 3 with `numpy`, `scipy`, `astropy`, `matplotlib`, `rasterio` and `ipympl` (for the interactive `%matplotlib widget` plots in the HST notebook).

```bash
pip install numpy scipy astropy matplotlib rasterio ipympl
```

All paths in the notebooks are relative to the repository root, so they run without changing any paths. Open them from the root folder and use **Restart & Run All**. Both notebooks recreate every file in `hst-processed/` and `sentinel-processed/`.

## Part 1: HST calibration

[`hst-assignment.ipynb`](hst-assignment.ipynb) turns raw WFPC2 exposures into calibrated images, following

```
stars + noise = (raw - bias - dark) / flat - sky
```

### Workflow

| Step | Calibration file | What the notebook does |
|---|---|---|
| 1. Mask | MASKFILE | Defective pixels (2) set to NaN; questionable pixels (256) kept and flagged |
| 2. A-to-D correction | ATODFILE | Skipped: the raw file is already ADC-corrected |
| 3. Bias level | BLEVFILE | Mean overscan level subtracted per chip, separately for even and odd columns |
| 4. Bias image | BIASFILE | Bias reference frame subtracted |
| 5. Dark | DARKFILE | Dark rate scaled by the exposure's DARKTIME and subtracted |
| 6. Flat field | FLATFILE | Multiplied by the inverse flat |
| 7. Shading | SHADFILE | Skipped: only needed for very short exposures |
| 8. Photometry | PHOTFLAM, PHOTZPT, ZP_CORR | Counts converted to flux density (erg s⁻¹ cm⁻² Å⁻¹) and magnitudes (STMAG) |
| 9. Sky | – | Per-chip sky estimated as the median after 3σ clipping and subtracted |

Each step is a separate function, and `calibrate_exposure()` runs the full workflow. The notebook first goes through the steps one by one for `ubai2507m` (with plots and checks), then calibrates every exposure in `hst-data/calibration/` in a loop.

### Outputs (`hst-processed/`)

| File | Contents |
|---|---|
| `<id>_calibrated.fits` | Calibrated image in counts (DN), all four chips, before sky subtraction |
| `<id>_skysub.fits` | Calibrated image after sky subtraction, in counts (DN) |
| `<id>_skysub_flux.fits` | Sky-subtracted chip 0 in flux density, with the photometry keywords in the header |
| `<id>_masked.fits`, `<id>_blev.fits`, `<id>_flux.fits` | Intermediate steps for the example exposure set by `calibration_image` (`ubai2507m` by default) |

Each file's header has a `HISTORY` entry describing the processing applied.

### Comparison with the STScI pipeline

The `*_c0m_aligned.fits` pipeline files contain only DETECTOR 1 (PC1), so the comparison uses chip 0. For all three F336W exposures, the difference between our image and the pipeline image has a median of 0.03–0.04 DN and a standard deviation of 0.22–0.28 DN. That is well below the sky noise of ≈ 1 DN. The largest differences lie in a band along the left and bottom edges of the chip.

## Part 2: Sentinel-2 analysis

[`sentinel-assignment.ipynb`](sentinel-assignment.ipynb) measures how the land area of Hunga Tonga–Hunga Ha'apai changed between 2014 and 2023 using the Google Earth images, and how the vegetated area changed between 2017 and 2019 using Sentinel-2. It then compares the results with the Sentinel-2 pipeline products and with each other.

### Workflow

| Section | Data | What the notebook does |
|---|---|---|
| 1. Google Earth pixel size | `White_light/*.jpg` | Measures the 600 m scale bar in pixels: 310 px in every image, so 1.935 m/px (3.746 m² per pixel) |
| 2. Sentinel-2 pixel size | `src.res`, `src.bounds` | Converts the pixel size from degrees (EPSG:4326) to metres with the latitude of the image centre: 9.36 m × 9.35 m (87.6 m²) |
| 3. Land area | Google Earth | HSV mask (hue 0–0.40) cleaned with a binary opening, removal of small regions and filling of small holes. `2021Dec` is excluded because the eruption plume covers the island |
| 4. Vegetated area | B04, B08 | NDVI = (B08 − B04) / (B08 + B04), vegetation where NDVI > 0.5 |
| 5.1 Pipeline comparison | `NDVI.tiff` | The pipeline NDVI is a colour image, so its vegetation mask (green as the strongest channel, about NDVI ≥ 0.125) is compared with ours pixel by pixel (agreement, IoU, area) |
| 5.2 Threshold sensitivity | B04, B08 | Vegetated area for NDVI thresholds from 0 to 0.8 |
| 5.3 Land area cross-check | B03, B08 | Independent land area from NDWI = (B03 − B08) / (B03 + B08) < 0.1, compared with the Google Earth series |
| 6. Final results | – | Writes every area to `areas.csv` |

Each step is a function defined at the top of the notebook (for example `land_mask_hsv`, `vegetation_mask`, `pixel_size_m`, `compare_masks`), and the cells below run them for one example image or date and then for all of them.

### Outputs (`sentinel-processed/`)

| File | Contents |
|---|---|
| `<image>_land_mask.png` | Land mask of each Google Earth image (1 = land) |
| `S2_<date>_land_mask.tif` | Sentinel-2 NDWI land mask, a GeoTIFF with the same georeferencing as the bands |
| `S2_<date>_vegetation_mask.tif` | Sentinel-2 NDVI vegetation mask (NDVI > 0.5), GeoTIFF |
| `areas.csv` | Every area in km², with columns `source`, `quantity` (land or vegetation), `date` and `area_km2` |

### Results

| Date | Source | Land area (km²) | Vegetated area (km²) |
|---|---|---|---|
| Feb 2014 | Google Earth | 0.739 | – |
| May 2016 | Google Earth | 2.882 | – |
| Jul 2017 | Sentinel-2 | 2.784 | 0.389 |
| Jul 2018 | Sentinel-2 | 2.928 | 0.481 |
| Jul 2019 | Sentinel-2 | 2.931 | 0.528 |
| Nov 2020 | Google Earth | 2.856 | – |
| Jan 2022 | Google Earth | 0.441 | – |
| Oct 2023 | Google Earth | 0.202 | – |

The 2014–2015 eruption joined the two islands and the land area grew almost fourfold. It stayed stable until 2020, with Google Earth and Sentinel-2 agreeing to within about 3%. The eruption of 15 January 2022 removed about 85% of it. Between 2017 and 2019 the vegetated area grew by about 36%. The pipeline NDVI gives about twice our vegetated area because it corresponds to a lower threshold (about 0.125); at that threshold the two agree to within 1–2%.

## AI usage

Both notebooks end with an "AI usage" section that states what Claude (Anthropic) was used for. As the module guidelines require, my unedited drafts of the markdown cells that Claude language-edited are in [`ai-unedited-drafts.md`](ai-unedited-drafts.md).

