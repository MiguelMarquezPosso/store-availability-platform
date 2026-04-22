from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional, List

from app.config.settings import settings
from app.repositories.data_repository import DataRepository
from app.services.availability_service import AvailabilityService
from app.models.schemas import StoreMetrics, GlobalMetrics, Interval

router = APIRouter()
service = AvailabilityService(DataRepository(settings.data_zip_url))

@router.get("/stores", response_model=List[str])
def list_stores():
    return service.list_store_ids()

@router.get("/global", response_model=GlobalMetrics)
def global_metrics(
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None)
):
    return service.get_global_metrics(from_date, to_date)

@router.get("/store/{store_id}", response_model=StoreMetrics)
def store_metrics(
    store_id: str,
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None)
):
    return service.get_store_metrics(store_id, from_date, to_date)

@router.get("/store/{store_id}/intervals", response_model=List[Interval])
def store_intervals(
    store_id: str,
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None)
):
    return service.get_store_intervals(store_id, from_date, to_date)