import os
class Config:
    SECRET_KEY='9b3a86e6e1c2d144d56576319e788c27'
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS= True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
