from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    firebase_uid = Column(String, nullable = False, unique = True)
    auth_type = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))
    is_verified = Column(Boolean, nullable = False, server_default = text("True"))
    role = Column(Integer, server_default = text("1"))
    last_login = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))
    is_deleted = Column(Boolean, nullable = False, server_default = text("False"))

class DeletedUsers(Base):
    __tablename__ = "deleted_users"

    firebase_uid = Column(String, primary_key=True, nullable = False, unique = True)
    auth_type = Column(String, nullable = False)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    email= Column(String, nullable = True)
    phone= Column(String, nullable = True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))

class HomePageBanners(Base):
    __tablename__ = "home_page_banners"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))
    image_link = Column(String, nullable = False)
    index = Column(Integer, primary_key=True, nullable=False)

class BlueDartOrders(Base):
    __tablename__ = "bd_orders"
    # id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    bd_awb_no = Column(String, nullable = False, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))
    bd_ccrcrdref = Column(String, nullable = True)
    bd_cluster_code = Column(String, nullable = True)
    bd_destination_area = Column(String, nullable=True)
    bd_destination_location = Column(String, nullable=True)
    bd_is_error = Column(Boolean, nullable=True)
    bd_token_number = Column(String, nullable=True)
    bd_status_information = Column(String, nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)


class Orders(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, nullable = False, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    product_id = Column(String, nullable = False)
    merchant_id = Column(String, nullable = False)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable = False)
    customer_name = Column(String, nullable = False)
    customer_full_address = Column(String, nullable=False)
    customer_pincode = Column(String, nullable=False)
    customer_address_type = Column(String, nullable=False)
    customer_phone_number = Column(String, nullable=False)
    customer_payment_method = Column(String, nullable=False)
    order_quantity = Column(Integer, nullable=False, server_default=text('1'))
    actual_order_quantity = Column(Integer, nullable=False, server_default=text('1'))
    related_to_order_id = Column(String, nullable = False)
    transaction_id = Column(String, nullable=True)
    payable = Column(String, nullable=False)
    delivery_charge = Column(String, nullable=False)
    product_listed_price = Column(String, nullable=False)
    bd_order_id = Column(String, ForeignKey('bd_orders.bd_awb_no', ondelete="CASCADE"), nullable = False)
    special_instructions = Column(String, nullable=True)
    is_delivered = Column(Boolean, nullable = False, server_default = text("False"))


    user = relationship("User")
    bd_order = relationship("BlueDartOrders")


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))
    feedback = Column(String, nullable = False)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable = False)

    user = relationship("User")

class OTP(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("Now()"))
    username = Column(String, nullable = False)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable = False)
    firebase_uid = Column(String, nullable = False, unique = False)
    otp = Column(String, nullable = False)
    otp_type = Column(String, nullable = False)
    is_used = Column(Boolean, nullable = False, server_default = text("False"))