from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from app.models.schemas import Interval, StoreMetrics, GlobalMetrics
from app.repositories.data_repository import DataRepository


class AvailabilityService:
    def __init__(self, repo: DataRepository):
        self.repo = repo
        self.data = self.repo.load_all()

    def _to_utc_aware(self, dt):
        if dt is None:
            return None
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    def _filter_points(self, points, from_date: Optional[datetime], to_date: Optional[datetime]):
        from_date = self._to_utc_aware(from_date)
        to_date = self._to_utc_aware(to_date)

        filtered = []
        for ts, val in points:
            ts = self._to_utc_aware(ts)

            if from_date and ts < from_date:
                continue
            if to_date and ts > to_date:
                continue
            filtered.append((ts, val))
        return filtered

    def get_store_points(self, store_id: str, from_date: Optional[datetime], to_date: Optional[datetime]):
        points = self.data.get(store_id, [])
        return self._filter_points(points, from_date, to_date)

    def summarize_store(self, store_id: str, from_date: Optional[datetime], to_date: Optional[datetime], sample_size: int = 50):
        points = self.get_store_points(store_id, from_date, to_date)
        if not points:
            return {"store_id": store_id, "points": [], "summary": "No data"}

        first_ts = points[0][0]
        last_ts = points[-1][0]
        values = [v for _, v in points]

        step = max(len(points) // sample_size, 1)
        sample = points[::step][:sample_size]

        return {
            "store_id": store_id,
            "from": first_ts.isoformat(),
            "to": last_ts.isoformat(),
            "total_points": len(points),
            "value_min": min(values),
            "value_max": max(values),
            "sample": [(ts.isoformat(), v) for ts, v in sample]
        }

    def _points_to_intervals(self, store_id: str, points: List[Tuple[datetime, int]]) -> List[Interval]:
        if len(points) < 2:
            return []

        intervals: List[Interval] = []
        prev_ts, prev_val = points[0]

        def state_from_delta(delta: int) -> str:
            return "online" if delta > 0 else "offline"

        current_state = "online"
        current_start = prev_ts

        for i in range(1, len(points)):
            ts, val = points[i]
            delta = val - prev_val
            state = state_from_delta(delta)

            if i == 1:
                current_state = state
                current_start = prev_ts

            if state != current_state:
                duration = int((ts - current_start).total_seconds())
                intervals.append(Interval(
                    store_id=store_id,
                    state=current_state,
                    start=current_start,
                    end=ts,
                    duration_seconds=duration
                ))
                current_state = state
                current_start = ts

            prev_ts, prev_val = ts, val

        last_ts = points[-1][0]
        duration = int((last_ts - current_start).total_seconds())
        intervals.append(Interval(
            store_id=store_id,
            state=current_state,
            start=current_start,
            end=last_ts,
            duration_seconds=duration
        ))

        return intervals

    def get_store_intervals(self, store_id: str, from_date: Optional[datetime], to_date: Optional[datetime]) -> List[Interval]:
        points = self.data.get(store_id, [])
        points = self._filter_points(points, from_date, to_date)
        return self._points_to_intervals(store_id, points)

    def get_store_metrics(self, store_id: str, from_date: Optional[datetime], to_date: Optional[datetime]) -> StoreMetrics:
        intervals = self.get_store_intervals(store_id, from_date, to_date)
        uptime = sum(i.duration_seconds for i in intervals if i.state == "online")
        downtime = sum(i.duration_seconds for i in intervals if i.state == "offline")
        total = uptime + downtime
        availability = (uptime / total * 100.0) if total > 0 else 0.0
        state_changes = max(len(intervals) - 1, 0)

        return StoreMetrics(
            store_id=store_id,
            uptime_seconds=uptime,
            downtime_seconds=downtime,
            availability_percent=round(availability, 2),
            state_changes=state_changes,
            interval_count=len(intervals),
            from_date=from_date,
            to_date=to_date
        )

    def get_global_metrics(self, from_date: Optional[datetime], to_date: Optional[datetime]) -> GlobalMetrics:
        total_uptime = 0
        total_downtime = 0
        availability_sum = 0.0
        store_count = len(self.data)

        for store_id in self.data.keys():
            m = self.get_store_metrics(store_id, from_date, to_date)
            total_uptime += m.uptime_seconds
            total_downtime += m.downtime_seconds
            availability_sum += m.availability_percent

        avg_availability = (availability_sum / store_count) if store_count > 0 else 0.0

        return GlobalMetrics(
            total_stores=store_count,
            avg_availability_percent=round(avg_availability, 2),
            total_uptime_seconds=total_uptime,
            total_downtime_seconds=total_downtime,
            from_date=from_date,
            to_date=to_date
        )

    def list_store_ids(self) -> List[str]:
        return list(self.data.keys())