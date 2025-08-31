from imgkit.transformations import expansao_de_pixel

pixels = [99,100,101,109,110,111]
resultado = [expansao_de_pixel(pixel, 120, 110) for pixel in pixels]

print(pixels)
print(resultado)
