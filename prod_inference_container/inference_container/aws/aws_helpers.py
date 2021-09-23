import boto3
import pandas
import csv
import time 
from time import sleep
import os

def download_artifact(s3_path: str, local_path: str, aditional_args:str=""):
    return os.system(command=f"aws s3 cp {s3_path} {local_path} {aditional_args}")

def decompress_artifact(filepath: str, destinationpath:str=None):
    if destinationpath is None:
        return os.system(command=f"tar xfv {filepath}")
    elif destinationpath is not None:
        return os.system(command=f"tar xfv {filepath} -C {destinationpath}")

def upload_artifact(local_path: str, s3_path: str, aditional_args:str=""):
    return os.system(command=f"aws s3 cp {local_path} {s3_path} {aditional_args}")