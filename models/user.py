from sqlalchemy import func

from db import db
from models.enums import RoleType


class BaseUserModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    updated_on = db.Column(db.DateTime, onupdate=func.now())


class UserModel(BaseUserModel):
    __tablename__ = "users"
    role = db.Column(db.Enum(RoleType), default=RoleType.user, nullable=False)
    deleted_on = db.Column(db.DateTime, onupdate=func.now())


class StaffModel(BaseUserModel):
    __tablename__ = "staffs"
    role = db.Column(db.Enum(RoleType), default=RoleType.staff, nullable=False)


class AdminModel(BaseUserModel):
    __tablename__ = "admins"
    role = db.Column(db.Enum(RoleType), default=RoleType.admin, nullable=False)

