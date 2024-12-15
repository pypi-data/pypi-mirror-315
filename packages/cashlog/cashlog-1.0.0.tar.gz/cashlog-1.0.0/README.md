# cashlog

[![GitHub main workflow](https://img.shields.io/github/actions/workflow/status/dmotte/cashlog/main.yml?branch=main&logo=github&label=main&style=flat-square)](https://github.com/dmotte/cashlog/actions)
[![PyPI](https://img.shields.io/pypi/v/cashlog?logo=python&style=flat-square)](https://pypi.org/project/cashlog/)

:snake: **Cash** flow **tracker**.

## Installation

This utility is available as a Python package on **PyPI**:

```bash
pip3 install cashlog
```

## Usage

There are some files in the [`example`](example) directory of this repo that can be useful to demonstrate how this tool works, so let's change directory first:

```bash
cd example/
```

We need a Python **virtual environment** ("venv") with some packages to do the demonstration:

```bash
python3 -mvenv venv
venv/bin/python3 -mpip install -r requirements.txt
```

Now we need some **input data**. You can take a look at the tests in [`test_cli.py`](test/test_cli.py) to understand the file format and create your own CSV input file.

Then we can **compute the totals**:

```bash
python3 -mcashlog --fmt-amount='{:+.2f}' --fmt-total='{:.2f}' input.csv output.csv
```

And finally display some nice **plots** using the [`plots.py`](example/plots.py) script (which uses the [_Plotly_](https://github.com/plotly/plotly.py) Python library):

```bash
venv/bin/python3 plots.py -at output.csv
```

**Tip**: if you want to somehow **filter the data** before generating the plots, you can use the `awk` command:

```bash
awk -F, 'NR==1 || ($2+0 >= 5 || $2+0 <= -5)' output.csv > output-filtered.csv
```

For more details on how to use this command, you can also refer to its help message (`--help`).

## Development

If you want to contribute to this project, you can install the package in **editable** mode:

```bash
pip3 install -e . --user
```

This will just link the package to the original location, basically meaning any changes to the original package would reflect directly in your environment ([source](https://stackoverflow.com/a/35064498)).

If you want to run the tests, you'll have to install the `pytest` package and then run:

```bash
pytest test
```
