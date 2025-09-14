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

- **Basic image loading and visualization**  
  Images can be loaded directly from disk or from memory arrays and displayed using standard Python visualization tools. This provides a straightforward way to inspect input data before applying transformations.  

  ```python
  from pictokit import Image

  # Load image from file
  img = Image(path="examples/image.png")

  # Display the original image
  print(img)

![Image Display Example](.github/readme/img.png)

---

- **Histogram analysis and equalization**
Functions are available to compute and plot image histograms, giving insights into the distribution of pixel intensities.  

```python
from pictokit import Image

img = Image(path="examples/image.png")

# Plot histogram of the original image
img.histogram()
```

![Plot Histogram Example](.github/readme/img_histogram.png)

---

- **Contrast expansion**
Contrast can also be improved through expansion techniques, where pixel values are stretched to cover a broader intensity range. This helps highlight details that might otherwise be lost in darker or brighter regions of the image.  

```python
from pictokit import Image

img = Image(path="examples/image.png")

# Apply contrast expansion with low and high limits and show histogram
img.contrast_expansion(low_limit=50, high_limit=200, hist=True)

# Show original and transformed images side by side
img.compare_images()
```

Example result of contrast expansion:  

![Contrast Expansion Example](https://via.placeholder.com/600x300?text=Contrast+Expansion+Example)
---

## Academic Motivation

This project was created in the context of **Image Processing courses**, to consolidate theoretical knowledge through practical implementations.  
It aims to provide both a **learning resource for students** and a **useful toolkit for developers** who want to explore image transformations.  

---

## Notes

If you want to contribute, please check the [CONTRIBUTING.md](CONTRIBUTING.md) file.  
Suggestions, bug reports, and improvements are always welcome.  
---
