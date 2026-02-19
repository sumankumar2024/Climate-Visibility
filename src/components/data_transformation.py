import sys
import os
import pandas as pd
import numpy as np
import glob
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.constant import *
from src.exception import VisibilityException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    data_transformation_dir = os.path.join(artifact_folder, 'data_transformation')
    transformed_train_file_path = os.path.join(data_transformation_dir, 'train.npy')
    transformed_test_file_path = os.path.join(data_transformation_dir, 'test.npy') 
    transformed_object_file_path = os.path.join(data_transformation_dir, 'preprocessing.pkl')

class DataTransformation:
    def __init__(self, valid_data_dir):
        self.valid_data_dir = valid_data_dir
        self.data_transformation_config = DataTransformationConfig()
        self.utils = MainUtils()
        
    def drop_schema_columns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            _schema_config = self.utils.read_schema_config_file()
            df = dataframe.drop(columns=_schema_config["drop_columns"])
            return df
        except Exception as e:
            raise VisibilityException(e, sys)

    def get_merged_batch_data(self) -> pd.DataFrame:
        """
        Forcefully pulls the 75,083 rows directly from ingestion artifacts.
        """
        try:
            # We bypass the 'valid_data_dir' since we skipped the validation copy step
            ingestion_path = os.path.join("artifacts", artifact_folder_name, "data_ingestion")
            data_files = glob.glob(os.path.join(ingestion_path, "*.csv"))
            
            if len(data_files) == 0:
                 raise Exception(f"No CSV files found in {ingestion_path}!")

            logging.info(f"Merging {len(data_files)} files from ingestion for transformation.")
            csv_data = [pd.read_csv(f) for f in data_files]
            return pd.concat(csv_data)
        except Exception as e:
            raise VisibilityException(e, sys)
             
    def initiate_data_transformation(self):
        logging.info("Entered initiate_data_transformation method")
        try:
            # Fixed the 'self' argument error by removing staticmethod and calling correctly
            dataframe = self.get_merged_batch_data()
            
            dataframe = self.drop_schema_columns(dataframe=dataframe)
            
            # Ensure TARGET_COLUMN is 'VISIBILITY' as per your MongoDB screenshot
            X = dataframe.drop(columns=TARGET_COLUMN)
            y = dataframe[TARGET_COLUMN]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

            preprocessor = StandardScaler()
            X_train_scaled = preprocessor.fit_transform(X_train)
            X_test_scaled = preprocessor.transform(X_test)

            preprocessor_path = self.data_transformation_config.transformed_object_file_path
            os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
            self.utils.save_object(preprocessor_path, obj=preprocessor)

            train_arr = np.c_[X_train_scaled, np.array(y_train)]
            test_arr = np.c_[X_test_scaled, np.array(y_test)]

            return (train_arr, test_arr, preprocessor_path)

        except Exception as e:
            raise VisibilityException(e, sys) from e