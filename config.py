import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:Timmy055055@localhost:5432/Enchong'

class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://database2_mzbr_user:7jqkG1fZ09U3PtTB2J0F5hUd2nAItrv5@dpg-cs7m1erv2p9s73f54rtg-a/database2_mzbr'
    #internal database url