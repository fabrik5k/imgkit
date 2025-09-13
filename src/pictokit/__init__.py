from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from beartype import beartype

import pictokit.transformations as tfm
from pictokit.__about__ import __version__
from pictokit.constants import Mode
from pictokit.controls import load_image

__all__ = [
    '__version__',
]


class Image:
    """
    Class for basic image operations from the Image Processing course.
    """

    @beartype
    def __init__(
        self,
        path: str | None = None,
        img_arr: np.ndarray | None = None,
        mode: Mode = 'any',
    ) -> None:
        """
        Initializes a new image instance.

        Args:
            path (Optional[str]): Filesystem path to the image file. Used to load the
                image from disk.
            img_arr (Optional[np.ndarray]): In-memory image array.
                Expected shapes:
                - (H, W) for grayscale
                - (H, W, C) for color, where C ∈ {3}
                Typical dtype: uint8.
            mode (Mode | str): Input policy for validation/conversion. Defaults `'any'`
                Options:
                - `'any'`: Accept input as-is (no forced conversion).
                - `'gray'`: Ensure grayscale; color inputs are converted.
                - `'color'`: Ensure 3-channel color; grayscale inputs are converted.

        Raises:
            FileNotFoundError: If `path` is provided and the file does not exist.
            ValueError: If neither `path` nor `img_arr` is provided, if `mode` is
                invalid, or if `img_arr` has an unsupported shape/dtype.
        """
        img = load_image(path, img_arr, mode)

        self.img = img
        self.img_shape = img.shape
        self.img1d = np.reshape(self.img, -1)
        self.transform = np.array([])
        self.transform1d = np.array([])

    def __repr__(self) -> str:
        plt.imshow(self.img)
        plt.show()
        return f'<Image: shape={self.img.shape}, dtype={self.img.dtype}>'

    @beartype
    def histogram(self, type: Literal['o', 't'] = 'o') -> None:
        """
        Plots the histogram of the image.

        Args:
            type (Literal["o", "t"], optional): Selects which image to use.
                - "o": Plot histogram of the original image.
                - "t": Plot histogram of the transformed image.
                Defaults to "o".

        Raises:
            ValueError: If `type` is not "o" or "t".
        """
        arr = self.img1d if type == 'o' else self.transform1d

        data = {'intensity': arr}
        df = pd.DataFrame(data)
        df = df['intensity'].value_counts().reset_index()
        plt.figure(figsize=(8, 6))
        plt.bar(df['intensity'], df['count'])
        plt.show()

    @beartype
    def contrast_expansion(
        self, low_limit: int, high_limit: int, hist: bool = False
    ) -> None:
        """
        Expands the contrast of the image by stretching pixel intensity values
        between the specified limits.

        Args:
            low_limit (int): Lower bound of the pixel intensity range.
            high_limit (int): Upper bound of the pixel intensity range.
            hist (bool, optional): If True, displays the histogram of the transformed
                image.
                Defaults to False.

        Attributes:
            transform (np.ndarray): The image resulting from a transformation applied
                to the instance.
            transform1d (np.ndarray): 1D array representation of the transformed image.

        Returns:
            None

        Raises:
            ValueError: If `low_limit` or `high_limit` are outside the valid pixel
                intensity range (0–255), or if `low_limit >= high_limit`.
        """
        aux_arr = []

        for pixel in self.img1d:
            args = {'pixel': pixel, 'low_limit': low_limit, 'high_limit': high_limit}
            new_pixel = int(tfm.pixel_expansion(**args))
            aux_arr.append(new_pixel)

        img_transform = np.array(aux_arr)

        self.transform = np.reshape(img_transform, self.img_shape)
        self.transform1d = np.array(aux_arr)

        if hist:
            self.histogram(type='t')

    def compare_images(self) -> None:
        """
        Displays the original image and the transformed image side by side
        to facilitate visual comparison.

        Attributes:
            img (np.ndarray): The original image.
            transform (np.ndarray): The image resulting from a transformation applied.

        Returns:
            None
        """
        _, axs = plt.subplots(1, 2, figsize=(10, 5))

        axs[0].imshow(self.img, cmap='gray')
        axs[0].set_title('Original')
        axs[0].axis('off')

        axs[1].imshow(self.transform, cmap='gray')
        axs[1].set_title('Transform')
        axs[1].axis('off')

        plt.show()
