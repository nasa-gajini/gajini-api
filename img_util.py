import json
import numpy as np
import cv2
import requests
from pydap.client import open_url
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm

def np_array_to_rgba_image(np_array, vmin, vmax):
    normalized_array = (np.clip(np_array, vmin, vmax) - vmin) / (vmax-vmin)  # Ensure values are within 0-1500
    colormap = plt.get_cmap('RdBu_r')
    #colormap = matplotlib.cm.cmap_d['RdBu_r']
    rgba_array = colormap(normalized_array)
    rgba_array[..., 3] = (normalized_array > 0).astype(np.float32)  # Make 0 values transparent
    rgba_array = (rgba_array * 255).astype(np.uint8)
    return rgba_array


def np_array_to_gray_image(np_array, vmin, vmax):
    normalized_array = (np.clip(np_array, vmin, vmax) - vmin) / (vmax-vmin)  # Ensure values are within 0-1500

    # uint8 gray img (0~255)  변환
    gray_array = (normalized_array * 255).astype(np.uint8)


    return gray_array


def merge_img(img1, img2):
    sum_img = img1.copy()
    # 결측치 비율을 계산하는 함수

    if img1.dtype == np.float32:
        sum_img[sum_img == -9999.0] = img2[sum_img == -9999.0]

    elif img1.dtype == np.uint16:
        sum_img[sum_img == 65534] = img2[sum_img == 65534]

    elif img1.dtype == np.uint8:
        sum_img[sum_img == 254] = img2[sum_img == 254]

    return sum_img
def lat_lon_to_x_y(start_lat, end_lat,start_lon, end_lon):
    px_angle = 0.05
    py_angle = 0.05

    start_x = int((start_lon + 180) / px_angle)
    end_x = int((end_lon + 180) / px_angle)
    start_y = int((90 - start_lat) / py_angle)
    end_y = int((90 - end_lat) / py_angle)
    return start_x,end_x,start_y,end_y


def point_lat_lon_x_y(lat, lon):
    px_angle = 0.05
    py_angle = 0.05

    x = int((lon + 180) / px_angle)
    y = int((90 - lat) / py_angle)

    return x,y