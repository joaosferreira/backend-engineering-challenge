from datetime import datetime, timedelta

import pytest

from unbabel_cli.core import (
    calculate_average,
    calculate_closed_time_interval,
    calculate_moving_averages,
    generate_time_range,
    is_in_window,
    TimeInterval
)
from unbabel_cli.models import AverageDeliveryTime, TranslationDelivered


@pytest.mark.parametrize("points, expected", [
    ([], None),
    ([0.0], 0.0),
    ([1.0], 1.0),
    ([1.0, 2.0, 3.0], 2.0),
    ([1.5, 2.5, 3.5], 2.5),
    ([0.1, 0.2, 0.3], 0.2),
])
def test_calculate_average(points, expected):
    result = calculate_average(points)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize("first, last, expected", [
    (datetime(2018, 12, 26, 18, 0, 5), None, TimeInterval(datetime(2018, 12, 26, 18, 0), datetime(2018, 12, 26, 18, 1))),
    (datetime(2018, 12, 26, 18, 0, 5), datetime(2018, 12, 26, 18, 0, 55), TimeInterval(datetime(2018, 12, 26, 18, 0), datetime(2018, 12, 26, 18, 1))),
    (datetime(2018, 12, 26, 18, 0, 15), datetime(2018, 12, 26, 18, 2, 45), TimeInterval(datetime(2018, 12, 26, 18, 0, 0), datetime(2018, 12, 26, 18, 3, 0))),
])
def test_calculate_closed_time_interval(first, last, expected):
    result = calculate_closed_time_interval(first, last=last)
    assert result == expected


@pytest.mark.parametrize("first, last", [
    (datetime(2018, 12, 26, 18, 2, 0), datetime(2018, 12, 26, 18, 1, 0)),
    (datetime(2018, 12, 26, 18, 0, 0), datetime(2018, 12, 26, 18, 0, 0)),
])
def test_calculate_closed_time_interval_with_unordered_dates(first, last):
    with pytest.raises(ValueError):
        list(calculate_closed_time_interval(first, last=last))


@pytest.fixture
def sample_time_interval():
    return TimeInterval(
        start=datetime(2018, 12, 26, 18, 0),
        end=datetime(2018, 12, 26, 18, 6)
    )


@pytest.mark.parametrize("step, expected", [
    (timedelta(minutes=1), [
        datetime(2018, 12, 26, 18, 0),
        datetime(2018, 12, 26, 18, 1),
        datetime(2018, 12, 26, 18, 2),
        datetime(2018, 12, 26, 18, 3),
        datetime(2018, 12, 26, 18, 4),
        datetime(2018, 12, 26, 18, 5),
        datetime(2018, 12, 26, 18, 6)
    ]),
    (timedelta(minutes=2), [
        datetime(2018, 12, 26, 18, 0),
        datetime(2018, 12, 26, 18, 2),
        datetime(2018, 12, 26, 18, 4),
        datetime(2018, 12, 26, 18, 6)
    ]),
    (timedelta(minutes=3), [
        datetime(2018, 12, 26, 18, 0),
        datetime(2018, 12, 26, 18, 3),
        datetime(2018, 12, 26, 18, 6),
    ]),
])
def test_generate_time_range(sample_time_interval, step, expected):
    result = list(generate_time_range(sample_time_interval, step=step))
    assert result == expected


@pytest.mark.parametrize("step", [
    timedelta(minutes=0),
    timedelta(minutes=-1)
])
def test_generate_time_range_with_invalid_step(sample_time_interval, step):
    with pytest.raises(ValueError, match="step must be a positive timedelta"):
        list(generate_time_range(sample_time_interval, step=step))


def test_generate_time_range_with_interval_not_divisible(sample_time_interval):
    with pytest.raises(ValueError, match="step must evenly divide the time interval"):
        list(generate_time_range(sample_time_interval, step=timedelta(minutes=4)))


@pytest.fixture
def sample_event():
    return TranslationDelivered(
        timestamp="2018-12-26 18:11:08.509654",
        translation_id="5aa5b2f39f7254a75aa5",
        source_language="en",
        target_language="fr",
        client_name="airliberty",
        event_name="translation_delivered",
        nr_words=30,
        duration=20
    )


@pytest.mark.parametrize("date, expected", [
    (datetime(2018, 12, 26, 18, 20, 0), True),
    (datetime(2018, 12, 26, 18, 21, 0), True),
    (datetime(2018, 12, 26, 18, 22, 0), False),
    (datetime(2018, 12, 26, 18, 23, 0), False),
])
def test_is_in_window(date, sample_event, expected):
    result = is_in_window(date, sample_event)
    assert result == expected


@pytest.mark.parametrize("window_size", [-1, 0])
def test_is_in_window_with_invalid_window_size(sample_event, window_size):
    with pytest.raises(ValueError):
        is_in_window(datetime(2018, 12, 26, 18, 0, 0), sample_event, window_size=window_size)


@pytest.mark.parametrize("events, expected", [
    ([], []),
    (
        [
            TranslationDelivered(
                timestamp="2018-12-26 18:11:08.509654",
                translation_id="5aa5b2f39f7254a75aa5",
                source_language="en",
                target_language="fr",
                client_name="airliberty",
                event_name="translation_delivered",
                nr_words=30,
                duration=20
            )
        ],
        [
            AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 11), average_delivery_time=0.0),
            AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 12), average_delivery_time=20.0)
        ]
    ),

])
def test_calculate_moving_averages(events, expected):
    result = calculate_moving_averages(events)
    assert result == expected


@pytest.fixture
def sample_events():
    return [
        TranslationDelivered(
            timestamp="2018-12-26 18:11:08.509654",
            translation_id="5aa5b2f39f7254a75aa5",
            source_language="en",
            target_language="fr",
            client_name="airliberty",
            event_name="translation_delivered",
            nr_words=30,
            duration=20
        ),
        TranslationDelivered(
            timestamp="2018-12-26 18:15:19.903159",
            translation_id="5aa5b2f39f7254a75aa4",
            source_language="en",
            target_language="fr",
            client_name="airliberty",
            event_name="translation_delivered",
            nr_words=30,
            duration=31
        ),
        TranslationDelivered(
            timestamp="2018-12-26 18:23:19.903159",
            translation_id="5aa5b2f39f7254a75bb3",
            source_language="en",
            target_language="fr",
            client_name="taxi-eats",
            event_name="translation_delivered",
            nr_words=100,
            duration=54
        )
    ]

def test_calculate_moving_averages_with_provided_example(sample_events):
    result = calculate_moving_averages(sample_events, window_size=10)

    expected = [
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 11), average_delivery_time=0.0),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 12), average_delivery_time=20.0),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 13), average_delivery_time=20.0),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 14), average_delivery_time=20.0),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 15), average_delivery_time=20.0),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 16), average_delivery_time=25.5),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 17), average_delivery_time=25.5),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 18), average_delivery_time=25.5),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 19), average_delivery_time=25.5),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 20), average_delivery_time=25.5),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 21), average_delivery_time=25.5),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 22), average_delivery_time=31.0),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 23), average_delivery_time=31.0),
        AverageDeliveryTime(date=datetime(2018, 12, 26, 18, 24), average_delivery_time=42.5)
    ]

    assert result == expected


def test_calculate_moving_averages_with_invalid_window_size(sample_event):
    with pytest.raises(ValueError):
        calculate_moving_averages([sample_event], window_size=-10)
