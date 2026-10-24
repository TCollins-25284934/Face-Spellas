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
├── sentinel-data/            # Sentinel-2 and white-light images
├── hst-assignment.ipynb
└── README.md
```

## Requirements

Python 3 with `numpy`, `scipy`, `astropy`, `matplotlib` and `ipympl` (for the interactive `%matplotlib widget` plots).

```bash
pip install numpy scipy astropy matplotlib ipympl
```

All paths in the notebooks are relative to the repository root, so they run without changing any paths. Open them from the root folder and use **Restart & Run All**.

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
| `ubai2507m_masked.fits`, `ubai2507m_blev.fits`, `ubai2507m_flux.fits` | Intermediate steps for the example exposure |

Each file's header has a `HISTORY` entry describing the processing applied.

### Comparison with the STScI pipeline

The `*_c0m_aligned.fits` pipeline files contain only DETECTOR 1 (PC1), so the comparison uses chip 0. For all three F336W exposures, the difference between our image and the pipeline image has a median of 0.03–0.04 DN and a standard deviation of 0.22–0.28 DN. That is well below the sky noise of ≈ 1 DN. The largest differences lie in a band along the left and bottom edges of the chip.

## Part 2: Sentinel-2 analysis

