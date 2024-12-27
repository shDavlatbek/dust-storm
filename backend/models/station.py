from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from schemas.station import StationSchema, ParameterSchema

class Station(Base):
    __tablename__ = "station"
    pydantic_model = StationSchema
    height: Mapped[int] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(String(length=250), nullable=False)
    lon: Mapped[float] = mapped_column(nullable=False)
    lat: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), 
        nullable=True, 
        default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), 
        nullable=True, 
        onupdate=func.now(), 
        default=func.now()
    )
    

class Parameter(Base):
    __tablename__ = "parameter"
    pydantic_model = ParameterSchema
    station: Mapped[int] = mapped_column(ForeignKey("station.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    tavg: Mapped[float] = mapped_column(nullable=True)
    tmin: Mapped[float] = mapped_column(nullable=True)
    tmax: Mapped[float] = mapped_column(nullable=True)
    havg: Mapped[int] = mapped_column(nullable=True)
    hmin: Mapped[int] = mapped_column(nullable=True)
    etavg: Mapped[float] = mapped_column(nullable=True)
    etmin: Mapped[float] = mapped_column(nullable=True)
    etmax: Mapped[float] = mapped_column(nullable=True)
    windavg: Mapped[float] = mapped_column(nullable=True)
    windimp: Mapped[float] = mapped_column(nullable=True)
    visavg: Mapped[float] = mapped_column(nullable=True)
    pavg: Mapped[float] = mapped_column(nullable=True)
    pmin: Mapped[float] = mapped_column(nullable=True)
    pmax: Mapped[float] = mapped_column(nullable=True)
    poavg: Mapped[float] = mapped_column(nullable=True)
    pomin: Mapped[float] = mapped_column(nullable=True)
    pomax: Mapped[float] = mapped_column(nullable=True)
    night: Mapped[float] = mapped_column(nullable=True)
    day: Mapped[float] = mapped_column(nullable=True)
    summary: Mapped[float] = mapped_column(nullable=True)
    rain: Mapped[float] = mapped_column(nullable=True)
    snow: Mapped[float] = mapped_column(nullable=True)
    fog: Mapped[float] = mapped_column(nullable=True)
    duststorm: Mapped[float] = mapped_column(nullable=True)

# class Date(Base):
#     __tablename__ = "parameter"
#     pydantic_model = ParameterSchema
#     station: Mapped[int] = mapped_column(ForeignKey("station.id"), nullable=False)
#     date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False) 
    

# class Temperature(Base):
#     __tablename__ = "temperature"
#     pydantic_model = TemperatureSchema
#     date: Mapped[int] = mapped_column(ForeignKey("date.id"), nullable=False)
#     tavg: Mapped[float] = mapped_column(nullable=True)
#     tmin: Mapped[float] = mapped_column(nullable=True)
#     tmax: Mapped[float] = mapped_column(nullable=True)   
    

# class Humidity(Base):
#     pydantic_model = HumiditySchema
#     date: Mapped[int] = mapped_column(ForeignKey("date.id"), nullable=False)
#     havg: Mapped[int] = mapped_column(nullable=True)
#     hmin: Mapped[int] = mapped_column(nullable=True)
    

# class EffektiveTemperature(Base):
#     __tablename__ = "effective_temperature"
#     pydantic_model = EffektiveTemperatureSchema
#     date: Mapped[int] = mapped_column(ForeignKey("date.id"), nullable=False)
#     etavg: Mapped[float] = mapped_column(nullable=True)
#     etmin: Mapped[float] = mapped_column(nullable=True)
#     etmax: Mapped[float] = mapped_column(nullable=True)


# class Wind(Base):
#     pydantic_model = WindSchema
#     date: Mapped[int] = mapped_column(ForeignKey("date.id"), nullable=False)
#     wavg: Mapped[float] = mapped_column(nullable=True)
#     wimp: Mapped[float] = mapped_column(nullable=True)


# class Pressure(Base):
#     pydantic_model = PressureSchema
#     date: Mapped[int] = mapped_column(ForeignKey("date.id"), nullable=False)
#     pavg: Mapped[float] = mapped_column(nullable=True)
#     pmin: Mapped[float] = mapped_column(nullable=True)
#     pmax: Mapped[float] = mapped_column(nullable=True)
#     poavg: Mapped[float] = mapped_column(nullable=True)
#     pomin: Mapped[float] = mapped_column(nullable=True)
#     pomax: Mapped[float] = mapped_column(nullable=True)
    

# class Precipitation(Base):
#     pydantic_model = PrecipitationSchema
#     date: Mapped[int] = mapped_column(ForeignKey("date.id"), nullable=False)
#     night: Mapped[float] = mapped_column(nullable=True)
#     day: Mapped[float] = mapped_column(nullable=True)
#     summary: Mapped[float] = mapped_column(nullable=True)
    
    
# class MeteorologicalProcess(Base):
#     __tablename__ = "meteorological_process"
#     pydantic_model = MeteorologicalProcessSchema
#     date: Mapped[int] = mapped_column(ForeignKey("date.id"), nullable=False)
#     rain: Mapped[float] = mapped_column(nullable=True)
#     snow: Mapped[float] = mapped_column(nullable=True)
#     fog: Mapped[float] = mapped_column(nullable=True)
#     duststorm: Mapped[float] = mapped_column(nullable=True)   