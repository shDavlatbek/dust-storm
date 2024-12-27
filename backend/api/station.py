from datetime import datetime
from fastapi import APIRouter, Depends, Query
from api.auth import fastapi_users

from api.dependencies import UOWDep
from services.station import StationService, ParameterService
from schemas.station import ParameterSchema, ParameterQuery, ParameterAdd, ParameterUpdate, StationQuery
from typing import Annotated, Optional


router = APIRouter(
    prefix="/station",
    tags=["Station"],
)


CACHE_EXPIRE = 3600
TIMEOUT = 30


@router.get("/")
async def get_stations(
    uow: UOWDep,
    filters: Annotated[StationQuery, Query()] = None,
    user=Depends(fastapi_users.current_user(active=True))
):
    return await StationService().get_stations(uow, filters)


@router.get("/parameter")
async def get_parameters(
    uow: UOWDep,
    filters: Annotated[ParameterQuery, Query()],
    user=Depends(fastapi_users.current_user(active=True))
):
    return await ParameterService().get_parameters(uow, filters)


@router.post("/parameter/add")
async def add_parameter(
    uow: UOWDep,
    parameter: ParameterAdd,
    user=Depends(fastapi_users.current_user(active=True))
):
    return {"parameter": await ParameterService().add_parameter(uow, parameter)}


@router.post("/parameter/edit")
async def edit_parameter(
    uow: UOWDep,
    parameter_id: int,
    parameter: ParameterUpdate,
    user=Depends(fastapi_users.current_user(active=True))
):  
    await ParameterService().edit_parameter(uow, parameter_id, parameter)
    return {"ok": True}


@router.get("/{id}")
async def get_station(
    uow: UOWDep,
    filters: Annotated[StationQuery, Query()],
    user=Depends(fastapi_users.current_user(active=True))
):
    return await StationService().get_station(uow, filters)