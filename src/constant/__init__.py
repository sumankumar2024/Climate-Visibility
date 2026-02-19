from datetime import datetime
import os


AWS_S3_BUCKET_NAME ="alpha-climate-visibility-2026"  #"visibility-bucket-im"
MONGO_DATABASE_NAME = "visibility-db"
MONGO_COLLECTION_NAME = "visibility"

TARGET_COLUMN = "VISIBILITY"
CLUSTER_LABEL_COLUMN = "Cluster0"

MODEL_FILE_NAME = "model"
MODEL_FILE_EXTENSION = ".pkl"

artifact_folder_name = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
artifact_folder =  os.path.join("artifacts", artifact_folder_name)