from typing import Callable, Literal

import matplotlib.pyplot as plt
import numpy as np
from beartype import beartype

import pictokit.element_wise as elw
from pictokit.__about__ import __version__
from pictokit.constants import Mode
from pictokit.controls import calculate_histogram, load_image

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
        self.transform = np.array([])

    def __repr__(self) -> str:
        plt.imshow(self.img)
        plt.show()
        return f'<Image: shape={self.img.shape}, dtype={self.img.dtype}>'

    @property
    def img1d(self):
        return np.reshape(self.img, -1)

    @property
    def transform1d(self):
        return np.reshape(self.transform, -1)

    @beartype
    def __pixel_transform(self, func: Callable, args: dict, reset: bool = False):
        img1d = self.img1d if reset or self.transform.size == 0 else self.transform1d

        aux_arr = []
        for pixel in img1d:
            args['pixel'] = pixel
            new_pixel = int(func(**args))
            aux_arr.append(new_pixel)
        img_transform = np.array(aux_arr)
        self.transform = np.reshape(img_transform, self.img.shape)

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
        img = self.img if type == 'o' else self.transform

        values = calculate_histogram(img=img)
        bars = len(values)
        plt.figure(figsize=(8, 6))
        plt.bar(range(bars), values)
        plt.show()

    @beartype
    def contrast_expansion(
        self,
        low_limit: np.uint8 | int,
        high_limit: np.uint8 | int,
        hist: bool = False,
        reset: bool = False,
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

        Returns:
            None
        """
        args = {'low_limit': low_limit, 'high_limit': high_limit}
        self.__pixel_transform(func=elw.pixel_expansion, args=args)

        if hist:
            self.histogram(type='t')

    def thresholding(
        self,
        T: np.uint8 | int,
        A: np.uint8 | int,
        hist: bool = False,
        reset: bool = True,
    ) -> None:
        """Apply binary thresholding to the image.

        This operation assigns each pixel either 0 or a specified intensity value A,
        depending on whether the pixel is below or above the threshold T. Optionally,
        it can display the histogram of the transformed image and reset the image to
        its original state before applying the transformation.

        Args:
            T (np.uint8 | int): Threshold value. Pixels greater than or equal to T are
                set to A, otherwise set to 0.
            A (np.uint8 | int): Intensity value assigned to multiply pixels above the
                threshold.
            hist (bool, optional): If True, display the histogram of the resulting
                image. Defaults to False.
            reset (bool, optional): If True, reset the image transformed to its
                original state before applying the thresholding. If False, apply
                thresholding on the current state of the image. Defaults to True.

        Returns:
            None
        """
        args = {'T': T, 'A': A}
        self.__pixel_transform(func=elw.pixel_thresholding, args=args, reset=reset)

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
