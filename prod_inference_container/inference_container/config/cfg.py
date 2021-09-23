import sys
import logging
BUCKET_MODEL = "###"
BUCKET_OUT = "###"
MODEL_KEY = 'model/pipeline.pkl'
USER = "###"

logger_app_name = 'Dataday-Prod'
logger = logging.getLogger(logger_app_name)
logger.setLevel(logging.INFO)
consoleHandle = logging.StreamHandler(sys.stdout)
consoleHandle.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
consoleHandle.setFormatter(formatter)
logger.addHandler(consoleHandle)