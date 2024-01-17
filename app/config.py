from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_days: int
    aes_key: str
    iv: str
    blue_dart_client_id: str
    blue_dart_client_secret: str
    blue_dart_login_id: str
    blue_dart_licence_key: str
    blue_dart_api_type: str
    blue_dart_customer_code: str
    blue_dart_area_code: str
    merchant_phone_number: str
    gst_number: str
    merchant_pincode: str
    merchant_address: str
    mail_id: str
    otp_mail: str
    otp_password: str
    firebase_realtime_db_url: str
    blue_dart_tracking_licence_key: str
    

    class Config:
        env_file = ".env"

settings = Settings()