
###  Punto de entrada de proceso. Partan leyendo de aqui y van revisando lo que necesitan. 
from config.cfg import BUCKET_OUT,CUSTOM_STOPWORDS,logger, USER
from model.make_model_pipeline import model
from data.modeling_data import procesamiento_base
import pandas as pd
import os
import numpy as np 
if __name__ == '__main__':
    PROCESO = os.getenv("PROCESO", None)
    FILE = os.getenv("KEY", None)
    #FILE_PATH = f"s3://{BUCKET}/{FILE}"
    #FILE = "s3://datadayprod/test/andres/test.csv"
    #PROCESO = "Predecir"
    
    if PROCESO == "Predecir" and FILE is not None:
        logger.info("Comenzando proceso")
        data_test = pd.read_csv(FILE)
        logger.info(f"Dim del archivo filas: {data_test.shape[0]}")
        data_test = procesamiento_base(data_test, CUSTOM_STOPWORDS)
        print(data_test.head())
        data_test = data_test.assign(pred = lambda df: model.predict(data_test))
        print(data_test)
        #print(data_train[["codigo_inmueble", "pred", "estrato"]].head())
        data_test.to_csv(f"s3://{BUCKET_OUT}/preds/{USER}/preds.csv")
        