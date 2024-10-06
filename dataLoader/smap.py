import cv2
import h5py
import numpy as np
from matplotlib import pyplot as plt

from img_util import np_array_to_gray_image, merge_img, np_array_to_rgba_image, lat_lon_to_x_y, point_lat_lon_x_y


class SmapDataset:
    def __init__(self, file_path):

        self.field_list = ['Soil_Moisture_Retrieval_Data_AM', 'Soil_Moisture_Retrieval_Data_PM','Metadata']


        # 파일 열기
        file = h5py.File(file_path, 'r')

        self.ds_dict = {}
        self.ds_img = {}

        print(file.keys())
        for key in self.field_list:
            # np array로 바꿀수 있는것만 변환
            # 하위 데이터 딕셔너리도 모두 순회하며 np array로 변환
            if isinstance(file[key], h5py.Dataset):
                self.ds_dict[key] = np.array(file[key])
            else:
                self.ds_dict[key] = {}
                for sub_key in file[key].keys():
                    self.ds_dict[key][sub_key] = np.array(file[key][sub_key])









    def remove_outlier(self, data):
        # float32는 결측 데이터가 -9999.0, UINT16은 65534, UINT8은 254
        # numpy array의 타입을 확인하고 결측치를 모두 0 혹은 0.0으로 변환
        if data.dtype == np.float32:
            data[data == -9999.0] = 0.0
        elif data.dtype == np.uint16:
            data[data == 65534] = 0
        elif data.dtype == np.uint8:
            data[data == 254] = 0
        return data

    def calc_fill_value_rate(self, data):
        # 결측치 비율을 계산하는 함수

        if data.dtype == np.float32:
            fill_value_rate = np.sum(data == -9999.0) / data.size
        elif data.dtype == np.uint16:
            fill_value_rate = np.sum(data == 65534) / data.size
        elif data.dtype == np.uint8:
            fill_value_rate = np.sum(data == 254) / data.size
        else:
            fill_value_rate = -1.0
        return fill_value_rate





    # 다른 일자 데이터셋 클래스를 받아서 ds_dict를 순회하면 모든 numpy array를 merge_img 함수로 합치는 함수
    def merge_ds(self, other):
        for key in self.ds_dict.keys():

            if isinstance(self.ds_dict[key], np.ndarray):
                pass
            else:
                for sub_key in self.ds_dict[key].keys():
                    try:
                        img1= self.ds_dict[key][sub_key]
                        img2 = other.ds_dict[key][sub_key]
                        sum_img = merge_img(img1, img2)
                        self.ds_dict[key][sub_key] = sum_img
                    except:
                        pass

    # 모든 이미지를 저장
    def calc_img(self,shape= (7200,3600)):
        # ds_dict에 있는 모든 데이터셋을 이미지로 저장
        for key in self.ds_dict.keys():
            if key == 'Metadata':
                continue

            if isinstance(self.ds_dict[key], np.ndarray):
                pass
            else:
                self.ds_img[key] = {}
                for sub_key in self.ds_dict[key].keys():
                    try:

                        data = self.remove_outlier(self.ds_dict[key][sub_key])
                        data_min = np.min(data)
                        # 만약 sub_key의 스트링에서   temperature 라는 단어가 포함된 상태라면
                        # 최소값을 253.15로 설정

                        if sub_key.find('temperature') != -1:
                            data_min = 253.15

                        img = np_array_to_rgba_image(data, data_min, np.max(data))
                        img = cv2.resize(img, shape, interpolation=cv2.INTER_CUBIC)
                        self.ds_img[key][sub_key] =img
                    except Exception as e:
                        print(e)



    def get_img_slice(self, key, sub_key,start_lat,end_lat,start_lon,end_lon):
        start_x, end_x, start_y, end_y = lat_lon_to_x_y(start_lat, end_lat, start_lon, end_lon)

        slice_img = self.ds_img[key][sub_key][start_y:end_y, start_x:end_x]

        return slice_img

    def all_ds_save_img(self, path):
        for key in self.ds_img.keys():
            if key == 'Metadata':
                continue

            if isinstance(self.ds_img[key], np.ndarray):
                cv2.imwrite(path + key + '.png', self.ds_img[key])
            else:
                for sub_key in self.ds_img[key].keys():
                    try:
                        cv2.imwrite(path + key + '_' + sub_key + '.png', self.ds_img[key][sub_key])
                    except:
                        pass

    def print_fill_value_rate(self):

        print_list = []
        # 모든 데이터의 결측치 비율을 계산
        for key in self.ds_dict.keys():
            if key == 'Metadata':
                continue

            if isinstance(self.ds_dict[key], np.ndarray):
                pass
            else:
                for sub_key in self.ds_dict[key].keys():
                    try:

                        fill_value_rate = self.calc_fill_value_rate(self.ds_dict[key][sub_key])
                        # 결측치 비율을 퍼센트로 바꿔서

                        print_list.append((f"{key}_{sub_key}: {fill_value_rate*100:.2f}%",fill_value_rate))


                    except:
                        pass
        # print_list에서 flag가 포함된 문자열은 제거
        print_list = [x for x in print_list if 'flag' not in x[0]]
        print_list = list(sorted(print_list, key=lambda x: x[1], reverse=True))
        for p in print_list:
            print(p[0])

    # 위도 경도에 해당하는 인덱스의 모든 데이터셋의 포인트 값을  dict로 반환
    def get_points(self, lat, lon):
        point_dict = {}
        px , py = point_lat_lon_x_y(lat,lon)
        x_rate = 3856/7200
        y_rate = 1928/3600



        px = int(px * x_rate)
        py = int(py * y_rate)
        print(px,py)

        for key in self.ds_dict.keys():
            if key == 'Metadata':
                continue

            if isinstance(self.ds_dict[key], np.ndarray):
                pass
            else:
                for sub_key in self.ds_dict[key].keys():
                    try:
                        data = self.ds_dict[key][sub_key]
                        point_dict[key + '_' + sub_key] = data[py, px]
                    except:
                        pass
        return point_dict

    # 인덱스로 포인트 dict 순회 반환
    def get_points_by_index(self, px, py):
        point_dict = {}

        for key in self.ds_dict.keys():
            if key == 'Metadata':
                continue

            if isinstance(self.ds_dict[key], np.ndarray):
                pass
            else:
                for sub_key in self.ds_dict[key].keys():
                    try:
                        data = self.ds_dict[key][sub_key]
                        point_dict[key + '_' + sub_key] = data[py, px]
                    except:
                        pass
        return point_dict



if __name__ == '__main__':
    # HDF5 파일 경로
    day_1 = '20240801'
    day_2 = '20240802'
    day_3 = '20240803'

    smap_0801 = SmapDataset('./SMAP/SMAP_L3_SM_P_E_'+day_1+'_R19240_002.h5')
    smap_0802 = SmapDataset('./SMAP/SMAP_L3_SM_P_E_'+day_2+'_R19240_002.h5')
    smap_0803 = SmapDataset('./SMAP/SMAP_L3_SM_P_E_'+day_3+'_R19240_002.h5')


    smap_0803.merge_ds(smap_0802)
    smap_0803.merge_ds(smap_0801)


    smap_0803.calc_img()
    smap_0803.all_ds_save_img('./smap_img_3/')


