import numpy as np
import settings as st


def find_mathces(template, src_image, valid_mask, gauss_mask):
    total_weight = np.sum(np.multiply(gauss_mask, valid_mask))
    if total_weight == 0:
        print "Trouble"

    ssd = []
    pixel_val = []
    src_row, src_col = np.shape(src_image)
    for i in range(st.half_window, src_row-st.half_window-1):
        for j in range(st.half_window, src_col-st.half_window-1):
            distance = (template - src_image[i-st.half_window:i + st.half_window + 1, j - st.half_window:j + st.half_window + 1]) ** 2
            ssd.append(np.sum(distance * gauss_mask * valid_mask) / total_weight)
            pixel_val.append(src_image[i, j])

    min_error = min(ssd)
    # print "Min Err loop= "+str(min_error)
    rPack=[]

    for i in range(len(ssd)):
        if ssd[i]<=min_error*(1+st.ERROR_THRESHOLD):
            rPack.append((ssd[i], pixel_val[i]))

    # print len(rPack)
    if len(rPack)==0:
        print template
    return  rPack


def find_matches_efficient(template,image_window, valid_mask, gauss_mask):
    template = np.reshape(template, st.n_pixel_window)
    gauss_mask = np.reshape(gauss_mask, st.n_pixel_window)
    valid_mask = np.reshape(valid_mask, st.n_pixel_window)
    total_weight = np.sum(np.multiply(gauss_mask, valid_mask))
    distance = (image_window-template)**2
    ssd = np.sum((distance*gauss_mask*valid_mask) / total_weight, axis=1)
    min_error = min(ssd)
    # print "Min err mat= "+str(min_error)
    mid = ((2 * st.half_window + 1) ** 2) / 2;
    return [[err, image_window[i][mid]] for i, err in enumerate(ssd) if err <= min_error*(1+st.ERROR_THRESHOLD)]