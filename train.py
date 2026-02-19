from dotenv import load_dotenv
load_dotenv() # This loads the variables from your .env file

from src.pipeline.training_pipeline import TraininingPipeline

pipeline = TraininingPipeline()
pipeline.run_pipeline()