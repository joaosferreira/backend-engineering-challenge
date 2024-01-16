from datetime import datetime

from pydantic import ValidationError
import pytest

from unbabel_cli.models import AverageDeliveryTime, TranslationDelivered


@pytest.fixture
def event_data():
    return {
        "timestamp": "2018-12-26 18:11:08.509654",
        "translation_id": "5aa5b2f39f7254a75aa5",
        "source_language": "en",
        "target_language": "fr",
        "client_name": "airliberty",
        "event_name": "translation_delivered",
        "nr_words": 30,
        "duration": 20.5,
    }


def test_translation_delivered_model(event_data):
    expected = TranslationDelivered(
        timestamp=datetime(2018, 12, 26, 18, 11, 8, 509654),
        translation_id="5aa5b2f39f7254a75aa5",
        source_language="en",
        target_language="fr",
        client_name="airliberty",
        event_name="translation_delivered",
        nr_words=30,
        duration=20.5
    )

    assert TranslationDelivered(**event_data) == expected


def test_translation_delivered_model_wit_invalid_event_name(event_data):
    event_data["event_name"] = "invalid_event"

    with pytest.raises(ValidationError):
        TranslationDelivered(**event_data)


def test_average_delivery_time_model():
    data = {"date": "2018-12-26 18:11:00", "average_delivery_time": 0.0}

    expected = AverageDeliveryTime(
        date="2018-12-26 18:11:00",
        average_delivery_time=0.0
    )

    assert AverageDeliveryTime(**data) == expected
