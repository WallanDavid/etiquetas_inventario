# app/models.py

from sqlalchemy import Column, Integer, String
from app.db import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    codigo = Column(String, unique=True, index=True)
    quantidade = Column(Integer, default=0)
