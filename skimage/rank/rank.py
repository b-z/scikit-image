"""
:author: Olivier Debeir, 2012
:license: modified BSD
"""

__docformat__ = 'restructuredtext en'

import warnings
from skimage import img_as_ubyte
import numpy as np

from .generic import find_bitdepth
import _crank16,_crank8

__all__ = ['mean']


def mean(image, selem, out=None, mask=None, shift_x=False, shift_y=False):
    """Return greyscale local mean of an image.

    Mean is computed on the given structuring element.

    Parameters
    ----------
    image : ndarray
        Image array (uint8 array or uint16). If image is uint16, as the algorithm uses max. 12bit histogram,
        an exception will be raised if image has a value > 4095
    selem : ndarray
        The neighborhood expressed as a 2-D array of 1's and 0's.
    out : ndarray
        The array to store the result of the morphology. If None is
        passed, a new array will be allocated.
    mask : ndarray (uint8)
        Mask array that defines (>0) area of the image included in the local neighborhood.
        If None, the complete image is used (default).
    shift_x, shift_y : bool
        shift structuring element about center point. This only affects
        eccentric structuring elements (i.e. selem with even numbered sides).
        Shift is bounded to the structuring element sizes.

    Returns
    -------
    local mean : uint8 array or uint16 array depending on input image
        The result of the local mean.

    Examples
    --------
    to be updated
    >>> # Local mean
    >>> from skimage.morphology import square
    >>> ima8 = 255*np.array([[0, 0, 0, 0, 0],
    ...                           [0, 1, 1, 1, 0],
    ...                           [0, 1, 1, 1, 0],
    ...                           [0, 1, 1, 1, 0],
    ...                           [0, 0, 0, 0, 0]], dtype=np.uint8)
    >>> mean(ima8, square(3))
    array([[ 63,  85, 127,  85,  63],
           [ 85, 113, 170, 113,  85],
           [127, 170, 255, 170, 127],
           [ 85, 113, 170, 113,  85],
           [ 63,  85, 127,  85,  63]], dtype=uint8)

    >>> ima16 = 4095*np.array([[0, 0, 0, 0, 0],
    ...                           [0, 1, 1, 1, 0],
    ...                           [0, 1, 1, 1, 0],
    ...                           [0, 1, 1, 1, 0],
    ...                           [0, 0, 0, 0, 0]], dtype=np.uint16)
    >>> mean(ima16, square(3))
    array([[1023, 1365, 2047, 1365, 1023],
           [1365, 1820, 2730, 1820, 1365],
           [2047, 2730, 4095, 2730, 2047],
           [1365, 1820, 2730, 1820, 1365],
           [1023, 1365, 2047, 1365, 1023]], dtype=uint16)

    """
    selem = img_as_ubyte(selem)
    if mask is not None:
        mask = img_as_ubyte(mask)
    if image.dtype == np.uint8:
        return _crank8.mean(image,selem,shift_x=shift_x,shift_y=shift_y,mask=mask,out=out)
    elif image.dtype == np.uint16:
        bitdepth = find_bitdepth(image)
        if bitdepth>11:
            raise ValueError("only uint16 <4096 image (12bit) supported!")
        return _crank16.mean(image,selem,shift_x=shift_x,shift_y=shift_y,mask=mask,bitdepth=bitdepth+1,out=out)
    else:
        raise TypeError("only uint8 and uint16 image supported!")

