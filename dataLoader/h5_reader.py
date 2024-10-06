import h5py
import numpy as np
import cv2

import img_util


class H5Reader:
    def __init__(self, file_path):
        self.ds_dict = {}
        self.file = h5py.File(file_path, 'r')
        self.img_dict= {} # 이미지 데이터를 저장할 딕셔너리

        # 모든 데이터셋을 순회하며 데이터를 읽고 딕셔너리에 저장
        def extract_data(name, obj):
            if isinstance(obj, h5py.Dataset):  # 데이터셋인지 확인
                self.ds_dict[name] = np.array(obj)  # 데이터셋 데이터를 NumPy 배열로 변환

        self.file.visititems(extract_data)  # 모든 아이템에 대해 extract_data 함수 실행

    def calc_img(self):
        for key in self.ds_dict.keys():
            data = self.ds_dict[key]
            key=key.replace('/','_')
            print(key)
            img =  img_util.np_array_to_rgba_image(data,data.min(),data.max())
            self.img_dict[key]=img
        return

    def get_img_slice(self, path, start_lat, end_lat, start_lon, end_lon):

        img = self.img_dict[path]

        start_x,end_x,start_y,end_y = img_util.lat_lon_to_x_y(start_lat, end_lat, start_lon, end_lon)

        slice_img = img[start_y:end_y, start_x:end_x]


        return slice_img

    def get_points_by_index(self, x, y):
        dict_ptr = {}
        for key in self.ds_dict.keys():
            img = self.ds_dict[key]
            try:
                dict_ptr[key] = img[y, x]
            except:
                pass
        return dict_ptr

    def get_point_by_lat_lon(self, lat, lon):
        x, y = img_util.point_lat_lon_x_y(lat, lon)
        return self.get_points_by_index(x, y)


    # 모든 데이터셋을 이미지로 저장
    def save_img(self, path):
        for key in self.ds_dict.keys():
            data = self.ds_dict[key]
            key=key.replace('/','_')
            print(key)


            img =  img_util.np_array_to_gray_image(data,data.min(),data.max())

            cv2.imwrite(path + key + '.png', img)

        return


