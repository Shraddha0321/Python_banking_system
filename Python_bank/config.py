class Config:
    SECRET_KEY = 'Sample123'
    MONGO_URI = 'mongodb://localhost:27017/python_banking'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400
