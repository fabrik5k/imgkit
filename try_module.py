from pictokit import Image

img = Image(path='./.github/readme/img_threshold.png')
print(img)
# Apply contrast expansion with low and high limits and show histogram
# img.contrast_expansion(low_limit=150, high_limit=250, hist=True)
img.histogram()
img.thresholding(A=1, T=150, hist=True)

# Show original and transformed images side by side
img.compare_images()
