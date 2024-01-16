from datetime import datetime
from typing import Literal, Union

from pydantic import BaseModel, validator


class EventBase(BaseModel):
    timestamp: datetime
    event_name: str = Literal["translation_delivered"]

    @validator("timestamp", pre=True)
    def parse_timestamp_field(cls, timestamp: Union[datetime, str]) -> datetime:
        if isinstance(timestamp, str):
            return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        return timestamp


class TranslationDelivered(EventBase):
    translation_id: str
    source_language: str
    target_language: str
    client_name: str
    nr_words: int
    duration: float

    @validator("event_name")
    def validate_event_name(cls, value: str):
        if value != "translation_delivered":
            raise ValueError("event_name must be 'translation_delivered'")
        return value


class AverageDeliveryTime(BaseModel):
    date: datetime
    average_delivery_time: float
