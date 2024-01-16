from datetime import datetime
import json
from typing import Any, Dict, List

from .models import AverageDeliveryTime, TranslationDelivered


def parse_event_data(data: Dict[str, Any]) -> List[TranslationDelivered]:
    """
    Parse and filter events.

    Args:
        data: Input dictionary containing event data.

    Returns:
        List of TranslationDelivered objects.

    Raises:
        ValueError: If the input dictionary does not contain an 'events' key.
    """
    if "events" not in data:
        raise ValueError("input should be a dict with 'events' key")
    return [TranslationDelivered(**event) for event in data["events"] if event["event_name"] == "translation_delivered"]


def serialize_results(results: List[AverageDeliveryTime]) -> str:
    """
    Serialize a list of results into a JSON string.

    Args:
        results: List of results.

    Returns:
        str: JSON representation of the results.
    """
    json_data = {
        "averages": [
            {"date": model.date.strftime("%Y-%m-%d %H:%M:%S"), "average_delivery_time": model.average_delivery_time}
            for model in results
        ]
    }
    return json.dumps(json_data)
