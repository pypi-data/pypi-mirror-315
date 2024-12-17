# winzy-macos-reminder

[![PyPI](https://img.shields.io/pypi/v/winzy-macos-reminder.svg)](https://pypi.org/project/winzy-macos-reminder/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-macos-reminder?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-macos-reminder/releases)
[![Tests](https://github.com/sukhbinder/winzy-macos-reminder/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-macos-reminder/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-macos-reminder/blob/main/LICENSE)

Create reminders in macos with cli

## Installation

First [install winzy](https://github.com/sukhbinder/winzy) by typing

```bash
pip install winzy
```

Then install this plugin in the same environment as your Winzy application.
```bash
winzy install winzy-macos-reminder
```
## Usage

```bash
usage: winzy remind [-h] [-dt DATETIME] [-df DATE_FORMAT] description

Create reminders in macos with cli

positional arguments:
  description           The description of the reminder.

optional arguments:
  -h, --help            show this help message and exit
  -dt DATETIME, --datetime DATETIME
                        The date and time for the reminder (e.g., '16 December 10am').
  -df DATE_FORMAT, --date-format DATE_FORMAT
                        The expected date format (default: '%d/%m/%Y').

```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-macos-reminder
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
