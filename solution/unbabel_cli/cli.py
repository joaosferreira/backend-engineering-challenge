import json

import click

from .core import calculate_moving_averages
from .utils import parse_event_data, serialize_results


@click.command()
@click.option("-i", "--input", type=click.File("r"), required=True, help="name of file to read")
@click.option("-o", "--output", type=click.File("w"), default="-", help="name of file to write")
@click.option("-w", "--window-size", default=10, help="size of rolling window")
def cli(input, output, window_size):
    events = parse_event_data(json.load(input))
    result = calculate_moving_averages(events, window_size=window_size)

    s = serialize_results(result)
    if output.name != "<stdout>":
        output.write(s)
    else:
        click.echo(s)
