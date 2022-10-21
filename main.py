# ----------------------------------------------------------------------------
# Filename    : main.py
# Created By  : Ting-Wei, Zhang (ghnmqdtg)
# Created Date: 2022/10/21
# version ='1.0'
# Inspired by : https://levelup.gitconnected.com/introduction-to-histogram-equalization-for-digital-image-enhancement-420696db9e43
# ---------------------------------------------------------------------------
import os
import numpy as np
import matplotlib.pyplot as plt
import utils
import config


def main():
    """
    To implement the histogram equalization
    """
    # Create folder if it doesn't exist
    utils.create_folder(config.SRC_FOLDER)
    utils.create_folder(config.DEST_FOLDER)

    # Get the path to the target files
    TARGET_PIC_SRC = os.path.join(config.SRC_FOLDER, config.TARGET_PIC)
    # Load files as np.array objects
    origin = utils.load_picture(TARGET_PIC_SRC)
    equalized = utils.hist_equalize(origin)

    # Save the original and equalized image in grayscale
    # The path to save the original
    DEST_PATH_ORIGINAL = os.path.join(config.DEST_FOLDER, f'img_original')
    DEST_PATH_EQUALIZED = os.path.join(config.DEST_FOLDER, f'img_equalized')
    # Save the picture
    utils.save_picture_rgb(DEST_PATH_ORIGINAL, origin)
    utils.save_picture_rgb(DEST_PATH_EQUALIZED, equalized)

    # Result analysis
    # Calculate the CDF and PDF of original image
    origin_hist_probability, origin_hist_cumulative = utils.get_hist(
        img_arr=origin, return_cumulative=True)
    ori_cdf = origin_hist_cumulative
    ori_pdf = origin_hist_probability

    # Calculate the CDF and PDF of and equalized image
    eq_hist_probability, eq_hist_cumulative = utils.get_hist(
        img_arr=equalized, return_cumulative=True)
    eq_cdf = eq_hist_cumulative
    eq_pdf = eq_hist_probability

    # Save the image
    plt.figure()
    plt.plot(ori_pdf)
    plt.plot(eq_pdf)
    plt.xlabel('Pixel intensity')
    plt.ylabel('Distribution')
    plt.legend(['Original', 'Equalized'])
    DEST_PATH_PDF = os.path.join(config.DEST_FOLDER, f'analysis_PDF.jpg')
    plt.savefig(DEST_PATH_PDF)

    plt.figure()
    plt.plot(ori_cdf)
    plt.plot(eq_cdf)
    plt.xlabel('Pixel intensity')
    plt.ylabel('Distribution')
    plt.legend(['Original', 'Equalized'])
    DEST_PATH_CDF = os.path.join(config.DEST_FOLDER, f'analysis_CDF.jpg')
    plt.savefig(DEST_PATH_CDF)


if __name__ == "__main__":
    # Run the process
    main()
