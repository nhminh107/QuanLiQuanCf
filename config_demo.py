# config.py.example
DB_CONFIG = {
    "driver": "{SQL Server}",
    "server": "YOUR_SERVER_NAME_HERE",
    "database": "YOUR_DB_NAME_HERE",
    "trusted_connection": "yes"
}

# Cấu hình đường dẫn thư mục
IMAGE_PATH = "assets/images/"
MODELS_PATH = "models/"
SERVICE_PATH = "services/"
UI_PATH = "ui/"


VAT_RATE = 0.1  # 10%
DEFAULT_PASSWORD_HASH = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92" # Hash của 123456