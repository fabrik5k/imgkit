# pictokit

## Introduction

`pictokit` is a Python library designed to perform **image processing and transformations**.  
It serves as a foundation for applying different methods commonly studied in **Image Processing courses**, while also being flexible enough to be extended for research and development.

---

## Installation

`pictokit` requires **Python >= 3.10**.

You can install it directly from PyPI:

```bash
pip install pictokit
```

---

## Features

- Basic image loading and visualization  
- Histogram analysis and equalization  
- Contrast expansion  
- [More features will be added and documented here in future versions]  

---

## How it Works

The library provides modular functions that can be combined to build **image transformation pipelines**.  
It is meant to be lightweight and educational, focusing on clarity and usability.  
Detailed usage examples will be provided in the official documentation.  

### Basic image loading and visualization  
  Images can be loaded directly from disk or from memory arrays and displayed using standard Python visualization tools. This provides a straightforward way to inspect input data before applying transformations.  

  ```python
  from pictokit import Image

  # Load image from file
  img = Image(path="examples/image.png")

  # Display the original image
  print(img)
```

![Image Display Example](.github/readme/img.png)

### Histogram analysis and equalization
Functions are available to compute and plot image histograms, giving insights into the distribution of pixel intensities.  

```python
from pictokit import Image

img = Image(path="examples/image.png")

# Plot histogram of the original image
img.histogram()
```

![Plot Histogram Example](.github/readme/img_histogram.png)

### Contrast Expansion
Contrast enhancement can be achieved through **expansion techniques**, where pixel intensity values are stretched to span a wider range (0–255).  
This adjustment improves the visibility of details that might otherwise be hidden in very dark or very bright regions of the image.  

The transformation is defined by the following formula:

$$
f(D) = \frac{255}{H - L}(D - L)
$$

Where:
- **D** → the original pixel value  
- **L** → the lowest pixel intensity in the image (minimum gray level)  
- **H** → the highest pixel intensity in the image (maximum gray level)  
- **f(D)** → the new pixel value, rescaled to the 0–255 range  


```python
from pictokit import Image

img = Image(path="examples/image.png")

# Apply contrast expansion with low and high limits and show histogram
img.contrast_expansion(low_limit=50, high_limit=250, hist=True)

# Show original and transformed images side by side
img.compare_images()
```

Example result of contrast expansion:  

![Contrast Expansion Example](.github/readme/compare_images.png)

### Thresholding
Thresholding is a **point operation** used to segment an image into regions based on intensity.  
Pixels with values below a given threshold are set to 0 (black), while pixels equal to or above the threshold are set to a specified intensity value \(A\) (commonly 255, white).  
This technique is widely used in image processing to separate foreground objects from the background.  

The transformation is defined by the following formula:

$$
f(D) = A \cdot u(D - T)
$$

Where:
- **D** → the original pixel value  
- **T** → the threshold value  
- **A** → the intensity value assigned when the condition is satisfied (usually 255)  
- **u(x)** → the unit step function, which is 0 if \(x < 0\) and 1 if \(x \geq 0\)  
- **f(D)** → the new pixel value (either 0 or \(A\))  

```python
from pictokit import Image

img = Image(path="examples/image.png")

# Apply thresholding with threshold T and intensity A
img.thresholding(A=1, T=150, hist=True)

# Show original and transformed images side by side
img.compare_images()
```

Example result of contrast expansion:  

![Thresholding Example](.github/readme/img_threshold.png)

### Digital Negative
Digital negative is a **point operation** that inverts the intensity of every pixel in the image.  
Dark areas become bright, and bright areas become dark, producing an effect similar to photographic film negatives.  
This technique is commonly used for image enhancement and visualization.  

The transformation is defined by the following formula:

$$
f(D) = 255 - D
$$

Where:  
- **D** → the original pixel value  
- **255** → the maximum intensity value in 8-bit images  
- **f(D)** → the new pixel value (the inverted intensity)  

```python
from pictokit import Image

img = Image(path="examples/digital_negative.png")

# Apply digital negative transformation
img.digital_negative(hist=True)

# Show original and transformed images side by side
img.compare_images()
```

Example result of digital negative:  

![Digital Negative Example](.github/readme/digital_negative.png)
---

## Academic Motivation

This project was created in the context of **Image Processing courses**, to consolidate theoretical knowledge through practical implementations.  
It aims to provide both a **learning resource for students** and a **useful toolkit for developers** who want to explore image transformations.  

---

## Notes

If you want to contribute, please check the [CONTRIBUTING.md](CONTRIBUTING.md) file.  
Suggestions, bug reports, and improvements are always welcome.  
---
