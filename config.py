import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    app_name: str = "Food Delivery API"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./food_delivery.db")
    secret_key: str = os.getenv("SECRET_KEY", "change-this-secret-key")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    algorithm: str = os.getenv("ALGORITHM", "HS256")


settings = Settings()
