from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import partial
from typing import Generator, List, Union

from .models import AverageDeliveryTime, TranslationDelivered


@dataclass
class TimeInterval:
    """
    Represents a time interval for datetimes.

    Attributes:
        start: The starting (i.e., left) endpoint of the interval.
        end: The ending (i.e., right) endpoint of the interval.
    """
    start: datetime
    end: datetime


def calculate_average(points: List[float], n_decimal: int = 2) -> Union[float, None]:
    """
    Calculate the unweighted average of a list of floating-point numbers.

    Args:
        points: List of floating-point numbers.
        n_decimal: Number of decimal places to round the result to.

    Returns:
        The calculated unweighted average. Returns None if the input list is empty.
    """
    if len(points) > 0:
        avg = sum(points)/len(points)
        return round(avg, n_decimal)
    return None


def calculate_closed_time_interval(first: datetime, last: Union[datetime, None] = None) -> TimeInterval:
    """
    Calculate a closed time interval.

    The time interval starts at the beginning of `first`'s minute (i.e., 0 seconds, 0 microseconds) and
    ends on the beginning of the next minute of `first`. If `last` is provided then the interval ends on
    the beginning of `last`'s next minute instead.

    Args:
        first: The starting datetime of the interval.
        last: The ending datetime of the interval.
            If not provided, the interval will be a single minute starting from the 'first' datetime.

    Returns:
        TimeInterval: An instance of `TimeInterval` representing the closed time interval.

    Raises:
        ValueError: If `first` is greater than or equal to `last`.
    """
    if last and first >= last:
        raise ValueError("first datetime must be before last datetime")

    start = first.replace(second=0, microsecond=0)
    end = (last.replace(second=0, microsecond=0) if last else start) + timedelta(minutes=1)
    return TimeInterval(start, end)


def generate_time_range(interval: TimeInterval, step: timedelta = timedelta(minutes=1)) -> Generator[datetime, None, None]:
    """
    Generate datetime objects within a specified time interval (inclusive) using a given time step.

    Args:
        interval: An instance of `TimeInterval` with start and end datetimes.
        step: The time step between generated datetimes.

    Yields:
        Datetime objects within the specified interval.

    Raises:
        ValueError: If the step is not a positive timedelta or does not evenly divide the time interval.
    """
    if not isinstance(step, timedelta) or step <= timedelta(0):
        raise ValueError("step must be a positive timedelta")
    if (interval.end - interval.start) % step != timedelta(0):
        raise ValueError("step must evenly divide the time interval")

    current = interval.start
    while current <= interval.end:
        yield current
        current += step


def is_in_window(date: datetime, event: TranslationDelivered, window_size: int = 10):
    """
    Check if an event occurred in a time window before the given time.

    Args:
        date: The reference date.
        event: The event to check.
        window_size: The size of the time window in minutes.

    Returns:
        True if the event is within the time window, False otherwise.

    Raises:
        ValueError: If the window size is a non-positive integer.
    """
    if window_size <= 0:
        raise ValueError("window size must be a positive integer")

    return date - timedelta(minutes=window_size) <= event.timestamp <= date


def calculate_moving_averages(events: List[TranslationDelivered], window_size: int = 10) -> List[AverageDeliveryTime]:
    """
    Calculate moving averages of delivery times for a list of translation events.

    Args:
        events: List of delivered translations.
        window_size: Size of the moving window in minutes.

    Returns:
        List of averages representing moving averages.

    Raises:
        ValueError: If the window size is a non-positive integer.
    """
    if window_size < 0:
        raise ValueError("window size must be a positive integer")

    if len(events) == 0:
        return []

    sorted_events = sorted(events, key=lambda x: x.timestamp)

    first, last = sorted_events[0].timestamp, sorted_events[-1].timestamp if len(events) > 1 else None
    averages = []
    for date in generate_time_range(calculate_closed_time_interval(first, last=last)):
        is_in_sized_window = partial(is_in_window, date, window_size=window_size)
        events_in_window = list(filter(is_in_sized_window, sorted_events))
        average_duration = calculate_average([event.duration for event in events_in_window])
        averages.append(
            AverageDeliveryTime(
                date=date,
                average_delivery_time=average_duration if average_duration else 0.0
            )
        )

    return averages
