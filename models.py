from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)

    bmi = Column(Float)

    age_group = Column(String)

    lifestyle_risk = Column(String)

    city_tier = Column(String)

    income_lpa = Column(Float)

    occupation = Column(String)

    predicted_premium = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
