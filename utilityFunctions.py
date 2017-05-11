import numpy as np
import settings as st


def gauss2D(shape, sigma):
    """
       Gaussian mask
       obtained from http://stackoverflow.com/questions/17190649/how-to-obtain-a-gaussian-filter-in-python
    """
    print sigma
    m, n = [(ss-1.)/2. for ss in shape]
    y, x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h


def sliding_window(src_img):
    src_window_matrix = []
    for i in range(st.half_window, src_img.shape[0]-st.half_window-1):
        for j in range(st.half_window, src_img.shape[1]-st.half_window-1):
            src_window_matrix.append(np.reshape(src_img[i-st.half_window:i + st.half_window + 1, j - st.half_window: j + st.half_window + 1], (2 * st.half_window + 1) ** 2))
    return np.double(src_window_matrix)
