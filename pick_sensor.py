import cv2

from dataLoader.h5_reader import H5Reader
from dataLoader.smap import SmapDataset

day_1 = '20240801'
day_2 = '20240802'
day_3 = '20240803'

smap_0801 = SmapDataset('./data/SMAP/SMAP_L3_SM_P_E_' + day_1 + '_R19240_002.h5')
smap_0802 = SmapDataset('./data/SMAP/SMAP_L3_SM_P_E_' + day_2 + '_R19240_002.h5')
smap_0803 = SmapDataset('./data/SMAP/SMAP_L3_SM_P_E_' + day_3 + '_R19240_002.h5')

smap_0803.merge_ds(smap_0802)
smap_0803.merge_ds(smap_0801)

smap_0803.calc_img()
field_list = ['Soil_Moisture_Retrieval_Data_AM_soil_moisture',
              'Soil_Moisture_Retrieval_Data_AM_vegetation_water_content',
              'Soil_Moisture_Retrieval_Data_AM_vegetation_opacity',
              'Soil_Moisture_Retrieval_Data_AM_bulk_density',
              'Soil_Moisture_Retrieval_Data_AM_clay_fraction',
              'Soil_Moisture_Retrieval_Data_AM_surface_temperature',
              'Soil_Moisture_Retrieval_Data_AM_surface_temperature']

modis_path = 'data/MOD13C1/MOD13C1.A2024257.061.2024275180829.h5'
import numpy as np

# 3600 7200
modis = H5Reader(modis_path)
modis.calc_img()
# 마우스 콜백 함수
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        x_rate =  7200/3856
        y_rate =  3600/1928


        dict_ptr = smap_0803.get_points_by_index(x, y)
        dict_modis = modis.get_points_by_index(int(x*x_rate), int(y*y_rate))

        print(" ===============================")
        print("SMAP")
        for key in dict_ptr.keys():
            if key in field_list:
                value = dict_ptr[key]
                key = key.replace("Soil_Moisture_Retrieval_Data_AM_"," ")
                if isinstance(value, float):  # 값이 float 타입인지 확인
                    print(f"{value:.3f} : {key}")
                else:
                    print(f"{value} : {key}")

        print(" MODIS")
        for key in dict_modis.keys():

            value = dict_modis[key]

            if isinstance(value, float):
                print(f"{value:.3f} : {key}")
            else:
                print(f"{value} : {key}")


# 이미지 로드
image_path = 'merged_soil_moisture.png'  # 이미지 경로 지정
img = cv2.imread(image_path)

if img is not None:
    # 윈도우 생성 및 이미지 표시
    cv2.namedWindow('image')
    cv2.imshow('image', img)

    # 마우스 콜백 설정
    cv2.setMouseCallback('image', click_event)

    # 키보드 입력 대기 (ESC 키로 종료)
    while True:
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
else:
    print("Image not found. Check the path.")
