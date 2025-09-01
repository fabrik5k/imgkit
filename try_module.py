from imgkit.transformations import expansao_de_pixel

pixels = [255]
resultado = [expansao_de_pixel(pixel, 0, 255) for pixel in pixels]

print(pixels)
print(resultado)
