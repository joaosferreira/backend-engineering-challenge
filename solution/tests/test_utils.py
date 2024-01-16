from datetime import datetime

import pytest

from unbabel_cli.models import AverageDeliveryTime, TranslationDelivered
from unbabel_cli.utils import parse_event_data, serialize_results


@pytest.mark.parametrize("events, expected", [
    ([], []),
    (
        [
            {
                "timestamp": "2018-12-26 18:11:08.509654",
                "translation_id": "5aa5b2f39f7254a75aa5",
                "source_language": "en",
                "target_language": "fr",
                "client_name": "airliberty",
                "event_name": "translation_delivered",
                "nr_words": 30,
                "duration": 20
            }
        ],
        [
                TranslationDelivered(
                timestamp=datetime(2018, 12, 26, 18, 11, 8, 509654),
                translation_id="5aa5b2f39f7254a75aa5",
                source_language="en",
                target_language="fr",
                client_name="airliberty",
                event_name="translation_delivered",
                nr_words=30,
                duration=20
            )
        ]
    )
])
def test_parse_event_data(events, expected):
    result = parse_event_data({"events": events})
    assert result == expected


def test_parse_event_data_with_no_events_field():
    with pytest.raises(ValueError):
        parse_event_data({})


@pytest.mark.parametrize("results, expected", [
    ([], "{\"averages\": []}"),
    (
        [AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 0), average_delivery_time=10.5)],
        "{\"averages\": [{\"date\": \"2018-12-26 18:00:00\", \"average_delivery_time\": 10.5}]}"
    )
])
def test_serialize_results(results, expected):
    result = serialize_results(results)
    assert result == expected
