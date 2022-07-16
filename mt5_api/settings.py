from pydantic import BaseSettings

class Settings(BaseSettings):
    mt5_path: str = "C:\Program Files\Rico - MetaTrader 5\terminal64.exe" 
    mt5_login: str = ""
    mt5_password: str = ""
    mt5_server: str = ""
    mt5_timeout: int = 60000