from typing import List

from fastapi import HTTPException
from schemas.station import ParameterAdd, ParameterSchema, ParameterUpdate
from utils.unitofwork import IUnitOfWork


class StationService:
    async def get_stations(self, uow: IUnitOfWork, filters = None):
        async with uow:
            if filters:
                filters = filters.model_dump()
                if filters["station"]:
                    station = await uow.station.find_one(id=filters["station"])
                    station.parameters = await uow.parameter.find_all(
                        filters=filters,
                        order_by="date",
                        order_desc=True
                    )
                    return station
                else:
                    stations = await uow.station.find_all()
                    for station in stations:
                        filters["station"] = station.id
                        station.parameters = await uow.parameter.find_all(
                            filters=filters,
                            order_by="date",
                            order_desc=True
                        )
            return stations
        
    async def get_station(self, uow: IUnitOfWork, filters = None):
        async with uow:
            station = await uow.station.find_one(number=filters.station)
            if not station:
                raise HTTPException(status_code=404, detail="Station not found")
            
            station.parameters = await uow.parameter.find_all(
                    filters=filters.model_dump(),
                    order_by="date",
                    order_desc=True
                )
            
            return station
    

class ParameterService:
    async def add_parameter(self, uow: IUnitOfWork, parameter: ParameterAdd):
        parameter_dict = parameter.model_dump()
        async with uow:
            parameter_id = await uow.parameter.add_one(parameter_dict)
            await uow.commit()
            return await uow.parameter.find_one(id=parameter_id)
        
    async def get_parameters(self, uow: IUnitOfWork, filters, limit: int = None) -> List[ParameterSchema]:
        async with uow:
            filter_by = filters.model_dump(exclude_none=True)
            if filters.start_date or filters.end_date:
                filter_by["datetime"] = (filters.start_date, filters.end_date)

            return await uow.parameter.find_all(
                filters=filter_by,
                order_by="datetime",
                order_desc=True,
                limit=limit if limit else None
            )
    
    async def edit_parameter(self, uow: IUnitOfWork, parameter_id: int, parameter: ParameterUpdate):
        parameter_dict = parameter.model_dump()
        async with uow:
            await uow.parameter.edit_one(parameter_id, parameter_dict)
            await uow.commit()