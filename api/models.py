from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base

class Fire(Base):
    __tablename__ = "fires"

    id = Column(Integer, primary_key=True, index=True)
    acquisition_datetime = Column(DateTime, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    brightness = Column(Float, nullable=False)
    confidence = Column(Integer, nullable=False)
    region = Column(String, nullable=False)