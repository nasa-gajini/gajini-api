from pydap.handlers.dap import unpack_dap4_data
import h5py
from h5_reader import H5Reader
path = 'data/MOD13C1/MOD13C1.A2024209.061.2024228074605.h5'
import numpy as np
# 3600 7200
ds = H5Reader(path)
ds.save_img('output/MOD13C1/')


