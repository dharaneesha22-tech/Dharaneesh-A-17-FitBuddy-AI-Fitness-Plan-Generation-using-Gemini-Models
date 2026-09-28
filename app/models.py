from sqlalchemy import Column, Integer, Float, String, Text
from .database import Base


class FitnessPlan(Base):

    __tablename__ = "fitness_plans"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    age = Column(Integer, nullable=False)

    weight = Column(Float, nullable=False)

    goal = Column(String(100), nullable=False)

    intensity = Column(String(50), nullable=False)

    workout_plan = Column(Text, nullable=False)

    nutrition_tip = Column(Text, nullable=False)