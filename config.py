import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:Timmy055055@localhost:5432/Enchong'

class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://database_rzcc_user:vzHmHnYl7XI27VZ52vyHcyHgoKLZ6iT6@dpg-crfuoabqf0us73dd198g-a/database_rzcc'
