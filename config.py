import os


class Config:

    MYSQL_USER = os.getenv("MYSQL_USER", "emi_user")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "emi_password")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "emi_calculator")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}"
        f"/{MYSQL_DATABASE}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False