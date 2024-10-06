from dataLoader.h5_reader import H5Reader
from dataLoader.smap import SmapDataset


class AllDataLoader:
    def __init__(self):

        self.smap_dataset = None
        self.ecostress_dataset = None
        self.modis = None


        # mmap load

        day_1 = '20240801'
        day_2 = '20240802'
        day_3 = '20240803'

        smap_0801 = SmapDataset('./data/SMAP/SMAP_L3_SM_P_E_' + day_1 + '_R19240_002.h5')
        smap_0802 = SmapDataset('./data/SMAP/SMAP_L3_SM_P_E_' + day_2 + '_R19240_002.h5')
        smap_0803 = SmapDataset('./data/SMAP/SMAP_L3_SM_P_E_' + day_3 + '_R19240_002.h5')

        smap_0803.merge_ds(smap_0802)
        smap_0803.merge_ds(smap_0801)

        smap_0803.calc_img()
        dict_points = smap_0803.get_points(30.85232,30.64332)
        field_list =['Soil_Moisture_Retrieval_Data_AM_soil_moisture',
                    'Soil_Moisture_Retrieval_Data_AM_vegetation_water_content',
                    'Soil_Moisture_Retrieval_Data_AM_vegetation_opacity',
                    'Soil_Moisture_Retrieval_Data_AM_bulk_density',
                    'Soil_Moisture_Retrieval_Data_AM_clay_fraction',
                    'Soil_Moisture_Retrieval_Data_AM_surface_temperature',
                    'Soil_Moisture_Retrieval_Data_AM_surface_temperature']
        for key in dict_points.keys():
            if key in field_list:
                print(f"{key}: {dict_points[key]}")

        self.smap_dataset = smap_0803



        # modis load
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days #1km pix +-30deg VZ
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days #1km pix used
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days Avg sun zen angle
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days EVI
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days EVI std dev
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days MIR reflectance
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days NDVI
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days NDVI std dev
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days NIR reflectance
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days VI Quality
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days blue reflectance
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days pixel reliability
        # MODIS_Grid_16Day_VI_CMG_Data Fields_CMG 0.05 Deg 16 days red reflectance
        # XDim:MODIS_Grid_16Day_VI_CMG
        # YDim:MODIS_Grid_16Day_VI_CMG

        modis_path = 'data/MOD13C1/MOD13C1.A2024257.061.2024275180829.h5'
        import numpy as np
        # 3600 7200
        self.modis = H5Reader(modis_path)
        self.modis.calc_img()









