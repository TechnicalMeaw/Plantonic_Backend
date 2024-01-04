from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from .database import Base
from sqlalchemy.orm import relationships



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    firebase_uid = Column(String, nullable = False, unique = True)
    auth_type = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))
    is_verified = Column(Boolean, nullable = False, server_default = text("True"))
    role = Column(Integer, server_default = text("1"))
    last_login = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))

class HomePageBanners(Base):
    __tablename__ = "home_page_banners"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))
    image_link = Column(String, nullable = False)
    index = Column(Integer, primary_key=True, nullable=False)
