### Nos decargamos el modelo desde el bucket de S3
import pandas as pd
import joblib
import sklearn
from aws.aws_helpers import download_artifact, decompress_artifact
from config import cfg

def create_needed_files():
    print(f"s3://{cfg.BUCKET_MODEL}/{cfg.MODEL_KEY}")
    download_artifact(f"s3://{cfg.BUCKET_MODEL}/{cfg.MODEL_KEY}", ".")
    #decompress_artifact(filepath="model.tar.gz")

def return_model():
    create_needed_files()
    pipeline = joblib.load("pipeline.pkl")
    return pipeline

model = return_model()