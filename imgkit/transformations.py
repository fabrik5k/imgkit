def expansao_de_pixel(pixel, limite_L, limite_H):
def expansao_de_pixel(pixel: int, limite_L: int, limite_H: int) -> int:
  if pixel > limite_L and pixel < limite_H:
    result = 255 / (limite_H - limite_L) * (pixel - limite_L)
  else:
    result = pixel
  return result
