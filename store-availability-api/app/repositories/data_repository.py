import io
import csv
import zipfile
import requests
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional


class DataRepository:
    def __init__(self, zip_url: str):
        self.zip_url = zip_url
        self._cache: Optional[Dict[str, List[Tuple[datetime, int]]]] = None

    def _download_zip(self) -> zipfile.ZipFile:
        r = requests.get(self.zip_url, timeout=30)
        r.raise_for_status()
        return zipfile.ZipFile(io.BytesIO(r.content))

    def _parse_csv_stream(self, name: str, file_obj) -> Tuple[str, List[Tuple[datetime, int]]]:
        store_id = name.rsplit("/", 1)[-1].replace(".csv", "")

        reader = csv.reader(io.TextIOWrapper(file_obj, encoding="latin-1"))
        header = next(reader, None)
        if not header:
            return store_id, []

        timestamps = []
        for col in header[4:]:
            raw = col.split(" GMT")[0].strip()
            try:
                ts = datetime.strptime(raw, "%a %b %d %Y %H:%M:%S").replace(tzinfo=timezone.utc)
                timestamps.append(ts)
            except ValueError:
                continue

        row = next(reader, None)
        if not row:
            return store_id, []

        values = []
        for v in row[4:]:
            try:
                values.append(int(v))
            except ValueError:
                values.append(0)

        points = list(zip(timestamps, values))
        return store_id, points

    def load_all(self) -> Dict[str, List[Tuple[datetime, int]]]:
        if self._cache is not None:
            return self._cache

        data: Dict[str, List[Tuple[datetime, int]]] = {}
        z = self._download_zip()

        for name in z.namelist():
            if name.startswith(".") or "__MACOSX" in name:
                continue

            if name.lower().endswith(".csv"):
                with z.open(name) as f:
                    store_id, points = self._parse_csv_stream(name, f)
                    data[store_id] = points

        self._cache = data
        return data