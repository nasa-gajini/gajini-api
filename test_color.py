import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm

import cv2
import numpy as np
img = cv2.imread('./img/NDVI_cut.png')
img  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
normalized_array = img/255.0
for color_map in plt.colormaps():
    print(color_map)
    rgba_array = plt.get_cmap(color_map)(normalized_array)
    rgba_array[..., 3] = (normalized_array > 0).astype(np.float32)  # Make 0 values transparent
    rgba_array = (rgba_array * 255).astype(np.uint8)
    cv2.imwrite('./img/NDVI_'+color_map+'_.png',rgba_array)
