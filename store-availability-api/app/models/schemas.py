from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Interval(BaseModel):
    store_id: str
    state: str
    start: datetime
    end: datetime
    duration_seconds: int

class StoreMetrics(BaseModel):
    store_id: str
    uptime_seconds: int
    downtime_seconds: int
    availability_percent: float
    state_changes: int
    interval_count: int
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None

class GlobalMetrics(BaseModel):
    total_stores: int
    avg_availability_percent: float
    total_uptime_seconds: int
    total_downtime_seconds: int
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None

class ChatRequest(BaseModel):
    question: str
    store_id: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]