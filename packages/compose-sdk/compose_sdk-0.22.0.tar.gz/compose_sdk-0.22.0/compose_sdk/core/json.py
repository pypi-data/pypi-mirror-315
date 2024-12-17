from datetime import datetime, date, time
from decimal import Decimal
import json
from uuid import UUID
from pathlib import Path
from enum import Enum


class JSON:
    # Remove callable objects from the data and serialize datetimes.
    @staticmethod
    def serialize(obj):
        if isinstance(obj, dict):
            return {k: JSON.serialize(v) for k, v in obj.items() if not callable(v)}
        elif isinstance(obj, (list, tuple, set, frozenset)):
            return [JSON.serialize(item) for item in obj if not callable(item)]
        elif isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        elif callable(obj):
            return None
        elif isinstance(obj, (Decimal, UUID, Path)):  # Combined string conversions
            return str(obj)
        elif isinstance(obj, (bytes, bytearray)):
            return "$$COULD_NOT_SERIALIZE_BYTES$$"
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return obj

    @staticmethod
    def stringify(data):
        cleaned_data = JSON.serialize(data)
        return json.dumps(cleaned_data)

    @staticmethod
    def remove_keys(data: dict, keys_to_ignore: list[str]):
        return {k: v for k, v in data.items() if k not in keys_to_ignore}

    @staticmethod
    def parse(data):
        return json.loads(data)
