from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    __abstract__ = True

db = SQLAlchemy(model_class=Base)