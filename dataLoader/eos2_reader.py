from pyhdf.SD import SD, SDC
import numpy as np
import requests
from pydap.client import open_url

from h4_reader import H4Reader
from img_util import np_array_to_gray_image
foo = H4Reader('./data/MOD13C1/MOD13C1.A2024257.061.2024275180829.hdf')

class EosReader:
    def __init__(self,all_load = False):

        edl_token = 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6Imx6YWsiLCJleHAiOjE3MzI3ODI5NTcsImlhdCI6MTcyNzU5ODk1NywiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292In0.CllLCWRe-eTXYG9S6grq63e62eGeOMR4YKcyRkvPJAn4uvfSr8mttJYiQHB9ByPbmIqFyp_xf5iOTlCVsJ4TyIPHvK63s40jE9WJPpwja_DgZZdUbLrRHDkMntLq_I4qaHKvvciqn6i6RnTQ8r5S4d1qROKLWyS0b-ELG07rv-3b5BZ9F5dIiLZFLhp06su6B6JFQpMx9GJ976kaTiPa-B918MtcoykiSrmp_YTE0o_JwjC8JWkUzcTOJmf6heegONqDtF5tTzmWo2cxMq5rFn33m9IyGjjxNvrFHqVoZwpfSm6-v5j4GH6k8rUul_NmvH_cxAkPpEQJ9xbmIz1_WQ'

        auth_hdr = "Bearer " + edl_token
        my_session = requests.Session()
        my_session.headers = {"Authorization": auth_hdr}
        import numpy as np
        # OPeNDAP URL
        dataset_url = 'https://opendap.cr.usgs.gov/opendap/hyrax/DP137/MOLT/MOD13C1.061/2024.09.13/MOD13C1.A2024257.061.2024275180829.hdf'
        self.gpm_ds = open_url(dataset_url, session=my_session, protocol='dap4')
        # np array로 바꿀수 있는것만 변환

        self.dict_ds={}
        self.dict_img = {}


        field_list = self.gpm_ds.keys()

        for key in field_list:

            self.dict_ds[key] = np.array(self.gpm_ds[key][:])
            print(key + " loaded")
        # ds_dict에 있는 모든 데이터셋을 이미지로 저장
        for key in self.dict_ds.keys():
            try:
                ds = self.dict_ds[key]
                if len(ds.shape) == 3:
                    ds = np.squeeze(ds)

                self.dict_img[key] = np_array_to_gray_image(ds, 0, np.max(ds))
            except:
                pass





