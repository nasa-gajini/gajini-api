from pyhdf.SD import SD, SDC
import numpy as np

import numpy as np
class H4Reader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.hdf_file = SD(file_path, SDC.READ)
        print(self.hdf_file)

        # 저장할 딕셔너리 초기화
        ds_dict = {}

        # 모든 데이터셋과 필드 순회
        datasets_dict = self.hdf_file.datasets()
        for ds_name in datasets_dict.keys():
            ds = self.hdf_file.select(ds_name)
            info = ds.info()
            data = ds.get()  # 데이터를 numpy 배열로 변환




    def get_dataset(self, dataset_name):
        return self.hdf_file.select(dataset_name)

