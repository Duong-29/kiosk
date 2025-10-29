import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

class Settings:
    def __init__(self):
        self.IP = os.getenv("IP", "127.0.0.1")
        self.PORT = int(os.getenv("PORT", 8000))

        # Database Config
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = os.getenv("DB_PORT", "3306")
        self.DB_USER = os.getenv("DB_USER", "root")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        self.DB_NAME = os.getenv("DB_NAME", "kiosk_python")

        #JWT config
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM","HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))

        #CORS config
        self.BACKEND_CORS_ORIGINS: list[str] = os.getenv("BACKEND_CORS_ORIGINS", "*").split(",")

        self.cryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

        self.SEPAY_API_KEY = "30f3185cc3aaf34b0628293691485fdf1b16aae89fafc385adab3010af9bf97d"

settings = Settings()