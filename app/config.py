import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost:3306/ticket_management',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-me')
    SCHEDULER_API_ENABLED = True
    MONTHLY_TARGET_HOURS = int(os.getenv('MONTHLY_TARGET_HOURS', '168'))
