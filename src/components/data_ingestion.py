import sys
import os
import numpy as np
import pandas as pd
from src.constant import *
from src.exception import VisibilityException
from src.logger import logging

from src.data_access.visibility_data import VisibilityData
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(artifact_folder, "data_ingestion")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.utils = MainUtils()

    def export_data_into_raw_data_dir(self) -> pd.DataFrame:
        """
        Method Name :   export_data_into_raw_data_dir
        Description :   Reads 75k records from MongoDB Atlas and saves locally.
        """
        try:
            logging.info(f"Exporting data from MongoDB database: {MONGO_DATABASE_NAME}")
            raw_batch_files_path = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(raw_batch_files_path, exist_ok=True)

            # Pulls 'visibility-db' from your constants
            visibility_data = VisibilityData(database_name=MONGO_DATABASE_NAME)
            
            # FIXED: Points exactly to the 'visibility' collection seen in your 75k import
            coll_name = "visibility" 
            logging.info(f"Fetching data from collection: {coll_name}")
            
            dataset = visibility_data.get_collection_data(collection_name=coll_name)
            print(f"DEBUG: Dataset contains {len(dataset)} rows.")
            
            # If the dataset is empty, we stop here with a clear error
            if dataset is None or dataset.empty:
                raise Exception(f"Fetched collection '{coll_name}' is empty! Check Atlas connection.")

            logging.info(f"Successfully fetched {len(dataset)} rows from MongoDB.")

            # Save data to artifacts folder
            feature_store_file_path = os.path.join(raw_batch_files_path, coll_name + '.csv')
            dataset.to_csv(feature_store_file_path, index=False)
            logging.info(f"Raw data saved to: {feature_store_file_path}")
            
            return dataset

        except Exception as e:
            raise VisibilityException(e, sys)

    def initiate_data_ingestion(self) -> str:
        """
        Method Name :   initiate_data_ingestion
        Description :   Starts the ingestion process and returns the directory path.
        """
        logging.info("Entered initiate_data_ingestion method")
        try:
            self.export_data_into_raw_data_dir()
            logging.info("Exited initiate_data_ingestion method successfully")
            return self.data_ingestion_config.data_ingestion_dir
        except Exception as e:
            raise VisibilityException(e, sys) from e