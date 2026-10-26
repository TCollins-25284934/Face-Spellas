# Unedited drafts of AI language-edited text

The module guidelines ask for the non-edited version of any text that was language-edited with an LLM. This file lists my original drafts of the markdown cells that Claude (Anthropic) edited. The edited versions are the ones in the notebooks. Cells not listed here were written without AI editing, or are listed under "No draft" below.

## hst-assignment.ipynb

### Section 11, discussion of the difference image

We can see from the third plot that the normalized differences between the two images range from -0.10 to 0.20 counts. These values are much lower in order of magnitude than the two separate images, which range from $$\approx$$ -10 to 10 counts. This indicates a very high correlation between our results and the reference image, which will be further visualised through a histogram.

### Section 11, discussion of the histograms

We can see that the two histograms are almost identical and the majority of pixels show a pixel-by-pixel difference between 0 and 0.1 DN

### No draft

These cells were drafted by Claude from the notebook output, without a draft of mine: Section 9 (sky estimate), the cell after the plot of the largest differences (Section 11), and Section 12 (final results).

Parts of the two Section 11 cells above also have no draft of mine, because Claude added them when it edited my text: the second paragraph of the difference-image discussion (the edge band and the bias-level offset), and in the histogram discussion the numbers (91.4%, median and standard deviation) and the sentences on the smaller groups of pixels near -0.15 and -0.08 DN and the tail up to 0.7 DN.

## sentinel-assignment.ipynb

### 1.2. Pixel size of every image

The results show that all bars are of the same length, indicating the images were taken in the same conditions from Google Earth, with the only thing changed being the date.

The measurement of the number of pixels in the bar is quite precise (see figure above) and even if the actual number of pixels in the bar were a slightly different amount, the area per pixel only varies by a few centimeters (eg: a bar of 309 pixels returns an area of 3.770 m^2 per pixel and one of 311 returns an area of 3.722 m^2). Considering the area per pixel is of the order of meters, this variation is not significant enough to affect our results.

### 2. Pixel-to-metre ratio of the Sentinel-2 images (discussion)

The calculated ground dimensions of the pixels are slightly below the nominal 10 m resolution. This difference arises from expressing pixel dimensions in angular units (EPSG:4326) and converting them to metres, with the horizontal dimension depending on latitude.

The variation in latitude across each image is small, so its effect on pixel dimensions is negligible for this analysis.

### 3.1. Explore the HSV values of one image

A hue range between 0 and 0.40 was chosen manually after plotting the imaging and observing the highest values of the pixels in the sea. This provided me with a first approximation which was later refined through trial and error, as I plotted the mask and checked if there were any significant portions of pixels that were mistakenly identified as land.

### 3.4. Excluding 2021Dec

Early on, I noticed that the 2021Dec image showed the entire island covered by a cloud of smoke (see figure below) that was due to the fact the volcano had become active during this time, culminating in the explosion of 15-01-2022 just a month later. As such, I chose to exclude this image from the analysis as it did not provide any useful data that could be used.

### 3.5. Land area over time

We can observe that the land area saw a massive increase between 2014 and 2016, due to the fact that material from the underwater volcano had risen above the sea level and "merged" the two separate islands into a larger one (this happened during the 2014-2015 eruptions). From 2016 to 2020 the total area remained stable and in the 2022 violent eruption, a lot of material was scattered during the explosion, resulting in a reduced land area. From 2022 to 2023 we can see a decrease in the land area, but this is due to the fact that the 2022 image mask counts a shadow from a cloud as land.

### 4.2. Choosing the NDVI threshold

I chose 0.5 manually, after comparing the NDVI image to the true colour and zooming in on the less vegetated areas to see what NDVI values they had.

### 4.4. Vegetated area over time

In this case, we only had Sentinel images ranging from 2017-2019, so we studied the evolution of the vegetated area during this time period. We can see a constant increase over time, starting at 0.389 km^2 and ending with 0.528 km^2 as during this time period, the volcano was inactive and the island remained "stable", allowing for plant life to grow and expand across the barren rocks and sands of the island.

This serves as an example of Dr. Ian Malcolm's famous saying "life finds a way", as we can see that even on a recently formed volcanic island, the total area covered by plants increased over time.

### 5.1. Our NDVI vs the pipeline NDVI (discussion)

We can see that our NDVI of 0.5 was a bit extreme as it left out many pixels (left figure, red) that could potentially be considered as vegetated area too. After lowering the threshold and comparing it to the pipeline's, we can see that the correlation is much higher, with fewer pixels left out.

However, as it was mentioned before, an NDVI of 0.5 is still reasonable as it is more unambiguous as to what is considered "vegetated area" (i.e, dense vegetation vs sparse one)

### 5.2. Sensitivity to the NDVI threshold

The relationship between the vegetated area and the threshold seems to behave hyperbolically. At lower thresholds, the vegetated area is extremely high, as several pixels meet the criteria and it decreases rapidly until the threshold reaches 0.2, from there, it stabilises but continues to decrease as the NDVI threshold is increased, as more pixels fail to meet the criteria.

### 5.3. Land area: Sentinel-2 vs Google Earth

The land area obtained with the Sentinel-2 images between 2017 and 2019 align well with the results from Google Earth, as they remain in the same range of values. They are not identical, but very similar, and some of the differences might be due to the lower resolution of Sentinel-2, resulting in either overestimating or underestimating the size of the island depending of what pixels pass the NDWI mask. There could also be other factors in play such as the tides when the sentinel images were taken, resulting in a higher or lower land area.

### No draft

These cells were drafted by Claude without a draft of mine: the introduction and the section introductions (Sections 0, 1, 2, 3, 4, 5.1 and 5.3), which came with the notebook skeleton.

### Section 6 (final results)

Claude suggested a summary of the results table. The text in the notebook is my own rewrite of it, without further AI editing.
