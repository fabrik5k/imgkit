from pictokit import Image

img = Image(path='./img_test/digital_negative.png')
print(img)
# Apply contrast expansion with low and high limits and show histogram
img.histogram()
img.digital_negative(hist=True)

# Show original and transformed images side by side
img.compare_images()
