from typing import List, Optional, Tuple
from pydantic import BaseModel, Field, model_validator
from datetime import datetime, timedelta, timezone

from utils.common import now_hours
    
    
class StationSchema(BaseModel):
    id: int
    height: int
    name: str
    lon: float
    lat: float
    created_at: datetime
    updated_at: datetime
    parameters: Optional[List['ParameterSchema']] = None

    class Config:
        exclude_none = True
        from_attributes = True
        
        
class StationQuery(BaseModel):  
    station: Optional[int] = None           
    start_date: Optional[datetime] = now_hours() - timedelta(days=10)
    end_date: Optional[datetime] = now_hours()

    @property
    def date(self) -> Tuple[Optional[datetime], Optional[datetime]]:
        return (self.start_date, self.end_date)

    class Config:
        from_attributes = True
        
    def model_dump(self, **kwargs):
        if self.start_date is None and self.end_date is None:
            return []
        
        # Pass the 'exclude' parameter to remove 'start_date' and 'end_date' from the dump
        exclude = kwargs.get("exclude", [])
        exclude.extend(["start_date", "end_date"])
        
        # Now call the original model_dump method with the updated exclude fields
        data = super().model_dump(**kwargs, exclude=exclude)
        
        # Add the 'date' field as a tuple of (start_date, end_date)
        data["date"] = (self.start_date.replace(tzinfo=None), self.end_date.replace(tzinfo=None))
        
        return data

        
class ParameterAdd(BaseModel):
    station: int
    date: int
    tavg: Optional[float] = None
    tmin: Optional[float] = None
    tmax: Optional[float] = None
    havg: Optional[int] = None
    hmin: Optional[int] = None
    etavg: Optional[float] = None
    etmin: Optional[float] = None
    etmax: Optional[float] = None
    windavg: Optional[float] = None
    windimp: Optional[float] = None
    visavg: Optional[float] = None
    pavg: Optional[float] = None
    pmin: Optional[float] = None
    pmax: Optional[float] = None
    poavg: Optional[float] = None
    pomin: Optional[float] = None
    pomax: Optional[float] = None
    night: Optional[float] = None
    day: Optional[float] = None
    summary: Optional[float] = None
    rain: Optional[float] = None
    snow: Optional[float] = None
    fog: Optional[float] = None
    duststorm: Optional[float] = None
    
    class Config:
        from_attributes = True        
        
    
class ParameterSchema(ParameterAdd):
    id: int


class ParameterUpdate(ParameterAdd):
    station: Optional[int] = None 


class ParameterQuery(BaseModel):
    id: Optional[int] = None
    station: Optional[int] = None            
    start_date: Optional[datetime] = now_hours() - timedelta(days=10)
    end_date: Optional[datetime] = now_hours()

    @property
    def date(self) -> Tuple[Optional[datetime], Optional[datetime]]:
        return (self.start_date, self.end_date)

    class Config:
        from_attributes = True
        
    def model_dump(self, **kwargs):
        if self.start_date is None and self.end_date is None:
            return []
        
        # Pass the 'exclude' parameter to remove 'start_date' and 'end_date' from the dump
        exclude = kwargs.get("exclude", [])
        exclude.extend(["start_date", "end_date"])
        
        # Now call the original model_dump method with the updated exclude fields
        data = super().model_dump(**kwargs, exclude=exclude)
        
        # Add the 'date' field as a tuple of (start_date, end_date)
        data["date"] = (self.start_date.replace(tzinfo=None), self.end_date.replace(tzinfo=None))
        
        return data
