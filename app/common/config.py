import os

class Config:
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")  # Asegúrate de que esta variable de entorno contenga un valor entero válido.
    SECRET_KEY = os.getenv("SECRET_KEY")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    S3_BASE_URL = os.getenv("S3_BASE_URL")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
    S3_REGION = os.getenv("S3_REGION")
