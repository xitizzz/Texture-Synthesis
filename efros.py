import numpy as np
import settings as st
from skimage import io, morphology, exposure
from random import randint
from math import ceil, floor
import matplotlib.pyplot as plt
import time

from utilityFunctions import gauss2D, sliding_window
from findMatches import find_mathces, find_matches_efficient


def efros_algorithm(src_img_path, window_size, new_image_row, new_image_col, output_name):
    start_time = time.time()
    max_error_threshold = st.ERROR_THRESHOLD
    sample = io.imread(src_img_path)

    sample = sample / 255.00

    # plt.imshow(sample, cmap="gray")
    # plt.show()

    img_row, img_col = np.shape(sample)

    sigma = st.window_size / 6.4;

    img_window = sliding_window(sample)
    print img_window.shape
    number_pixel = new_image_row * new_image_col
    interval = ceil(number_pixel/100)
    new_image = np.zeros((new_image_row, new_image_col))

    # #Seed
    seed_size = st.SEED_SIZE
    random_row = randint(0, img_row - seed_size)
    random_col = randint(0, img_col - seed_size)
    seed = sample[random_row:random_row + seed_size, random_col:random_col + seed_size]
    new_image[floor(new_image_row / 2):floor(new_image_row / 2) + seed_size,
    floor(new_image_col / 2):floor(new_image_col / 2) + seed_size] = seed

    number_filled = seed_size * seed_size
    is_filled = np.zeros((new_image_row, new_image_col))
    is_filled[floor(new_image_row / 2):floor(new_image_row / 2) + seed_size,
    floor(new_image_col / 2):floor(new_image_col / 2) + seed_size] = np.ones((seed_size, seed_size))

    gaussian_mask = gauss2D((window_size, window_size), sigma=sigma)
    print gaussian_mask.shape

    new_image_padded = np.lib.pad(new_image, st.half_window, 'constant', constant_values=0)
    is_filled_padded = np.lib.pad(is_filled, st.half_window, 'constant', constant_values=0)

    while number_filled < number_pixel:
        progress = False
        candidate_pixel_row, candidate_pixel_col = np.nonzero(morphology.binary_dilation(is_filled) - is_filled)
        neighborHood = []
        for i in range(len(candidate_pixel_row)):
            pixel_row = candidate_pixel_row[i]
            pixel_col = candidate_pixel_col[i]
            neighborHood.append(np.sum(is_filled[pixel_row - st.half_window : pixel_row + st.half_window + 1,
                                       pixel_col - st.half_window : pixel_col + st.half_window + 1]))
        # print candidate_pixel_row.shape
        order = np.argsort(-np.array(neighborHood, dtype=int))
        # print order
        for x, i in enumerate(order): #range(len(candidate_pixel_row)):
            pixel_row = candidate_pixel_row[i]
            pixel_col = candidate_pixel_col[i]
            # print pixel_row, pixel_col
            # best_match = find_mathces(new_image_padded[pixel_row - st.half_window + st.half_window:pixel_row + st.half_window +st.half_window+1,
            #                                pixel_col - st.half_window + st.half_window :pixel_col + st.half_window+st.half_window+1],
            #                                sample,
            #                                is_filled_padded[pixel_row - st.half_window + st.half_window :pixel_row + st.half_window + st.half_window+1,
            #                                pixel_col - st.half_window + st.half_window :pixel_col + st.half_window + st.half_window + 1],
            #                                gaussian_mask)
            best_match = find_matches_efficient(
                new_image_padded[pixel_row - st.half_window + st.half_window:pixel_row + st.half_window + st.half_window + 1,
                pixel_col - st.half_window + st.half_window:pixel_col + st.half_window + st.half_window + 1],
                img_window,
                is_filled_padded[pixel_row - st.half_window + st.half_window:pixel_row + st.half_window + st.half_window + 1,
                pixel_col - st.half_window + st.half_window:pixel_col + st.half_window + st.half_window + 1],
                gaussian_mask)
            """
            DEBUG code to verify correctness of efficient method
            """
            # if len(best_match)!=len(best_match_t):
            #     print "ooooh NO"
            # for i in range(len(best_match)):
            #     if not np.isclose(best_match[i][0], best_match_t[i][0]):
            #         print "Ooops "+str(best_match[i][0])+" "+str(best_match_t[i][0])
            #     if best_match[i][1]!=best_match_t[i][1]:
            #         print "pixel val"
            # print (len(best_match))
            pick = randint(0, len(best_match)-1)
            # print "Matches= ", len(best_match)
            if best_match[pick][0]<=max_error_threshold:
                new_image_padded[st.half_window+pixel_row][st.half_window+pixel_col] = best_match[pick][1]
                new_image[pixel_row][pixel_col]=best_match[pick][1]
                is_filled_padded[st.half_window+pixel_row][st.half_window+pixel_col] = 1
                is_filled[pixel_row][pixel_col]=1
                number_filled+=1
                if number_filled % interval == 0:
                    if randint(0, 50) == 0:
                        st.quote()
                    else:
                        print "Pixels filled {:d}/{:d} | {:d}% | Time = {:3.2f} sec".format(number_filled, number_pixel, int(number_filled/interval), time.time()-start_time)
                progress = True
        if not progress:
            max_error_threshold *= 1.1
            print "new threshold = " + str(max_error_threshold)

    # new_image = new_image*255

    io.imsave(st.output_path+output_name, new_image)
    # io.imshow(new_image)
    plt.show()