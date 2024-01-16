# Unbabel CLI

A simple command-line application for Unbabel's Backend Engineering Challenge.
## Requirements

Python 3.8

- [Click](https://click.palletsprojects.com/) for creating the command-line interface.
- [Pydantic](https://docs.pydantic.dev/) for data validation and parsing.

## Installation

To install the Unbabel CLI, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/joaosferreira/backend-engineering-challenge.git
    ```

2. Change to the correct directory:

    ```bash
    cd backend-engineering-challenge/solution
    ```

3. Install the command-line application and it's dependencies:

    ```bash
    pip install .
    ```

## Example

### Input

The Unbabel CLI expects a file with the following format as input:

```json
{
    "events": [
        {
            "timestamp": "2018-12-26 18:11:08.509654",
            "translation_id": "5aa5b2f39f7254a75aa5",
            "source_language": "en",
            "target_language": "fr",
            "client_name": "airliberty",
            "event_name": "translation_delivered",
            "nr_words": 30,
            "duration": 20
        },
        ...
    ]
}
```

### Usage

You can run the command-line application with:

```bash
unbabel_cli --input events.json --window-size 10
```

And get help with `ùnbabel_cli --help`.


## Testing

To run the tests you need to install the test dependecies:

```bash
pip install '.[test]'
```

And run:

```bash
pytest
```
