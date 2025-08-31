def expansao_de_pixel(pixel, limite_L, limite_H):
  if pixel > limite_L and pixel < limite_H:
    result = 255/(limite_H - limite_L) * (pixel - limite_L)
  else:
    result = pixel
  return result
