# ----------------------------------------------------------------------------
# Filename    : utils.py
# Created By  : Ting-Wei, Zhang (ghnmqdtg)
# Created Date: 2022/10/21
# version ='1.0'
# ---------------------------------------------------------------------------
import os
import numpy as np
from PIL import Image
import config


def create_folder(dir) -> None:
    """
    Create a folder if it doesn't already exist
    """

    if not os.path.exists(dir):
        os.makedirs(dir)


def load_picture(src_path: str) -> np.array:
    """
    Load and resize picture and return is as np.array

    Parameters
    ----------
    src_path : str
        The path to the source picture
    """

    img = Image.open(src_path)
    img = img.convert(mode='L')
    resized = img.resize(config.PICTURE_SIZE)
    img_arr = np.array(resized)
    return img_arr


def save_picture_rgb(dest_path: str, img_arr: np.array) -> None:
    """
    Save np.array image data in RGB JPG

    Parameters
    ----------
    dest_path : str
        The path to save the picture
    img_arr : np.array
        Image data in np.array
    """

    result = Image.fromarray(np.uint8(img_arr)).convert('RGB')
    result.save(f'{dest_path}.jpg')


def get_hist(img_arr: np.array, return_cumulative: bool = True) -> np.array:
    """
    Retrun the PDF (histogram) and the CDF (cumulative histogram) of the image

    Parameters
    ----------
    img_arr : np.array
        Image to be processed
    return_cumulative : bool
        Retrun the cumulative distribution or not

    Returns
    ----------
    hist : np.array
        The probability density of the img (PDF)
    hist_cumulative : np.array
        The cumulative distribution of the img (CDF)
    """

    # Flatten the image and calculate the histogram with binning
    hist_probability = np.bincount(img_arr.flatten(), minlength=256)
    # Normalize the histogram
    hist_normalized = hist_probability / (img_arr.shape[0] * img_arr.shape[1])
    # cumulative histogram
    hist_cumulative = np.cumsum(hist_normalized)

    if return_cumulative:
        return hist_probability, hist_cumulative
    else:
        return hist_probability


def hist_equalize(img_arr: np.array) -> np.array:
    """
    Process the histogram equalization to the image, and return the result

    Parameters
    ----------
    img_arr : np.array
        Image to be processed

    Returns
    ----------
    eq_img_array : np.array
        The equalized image
    """

    # STEP 1: Normalized cumulative histogram
    origin_hist_probability, origin_hist_cumulative = get_hist(
        img_arr, return_cumulative=True)

    # STEP 2: Mapping lookup table
    transform_map = np.floor(255 * origin_hist_cumulative).astype(np.uint8)

    # STEP 3: Transformation and write back into img_array
    # Flatten image array into 1D list
    origin_list = list(img_arr.flatten())
    # transform pixel values to equalize
    eq_img_list = [transform_map[pixel] for pixel in origin_list]
    # reshape and write back into img_array
    eq_img_array = np.reshape(np.asarray(eq_img_list), img_arr.shape)

    return eq_img_array
