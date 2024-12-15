#!/usr/bin/env python3

import io
import textwrap

import pytest

from datetime import datetime as dt
from datetime import timezone as tz

from cashlog import load_data, save_data, compute_totals


def test_load_data():
    data_out_expected = [
        {'datetime': dt(2020, 1, 1, tzinfo=tz.utc),
         'amount': 5, 'desc': 'First gift'},
        {'datetime': dt(2020, 1, 3, tzinfo=tz.utc),
         'amount': 7.5, 'desc': 'Second gift'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': -3.1, 'desc': 'First expense'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': 0, 'desc': 'Zero'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': 0, 'desc': 'Negative zero'},
    ]

    csv = textwrap.dedent('''\
        datetime,amount,desc
        2020-01-01 00:00:00+00:00,+5,First gift
        2020-01-03 00:00:00+00:00,+7.500,Second gift
        2020-01-05 00:00:00+00:00,-3.1,First expense
        2020-01-05 00:00:00+00:00,+0,Zero
        2020-01-05 00:00:00+00:00,-0,Negative zero
    ''')

    data, delimiter = load_data(io.StringIO(csv))

    assert data == data_out_expected
    assert delimiter == ','

    csv = textwrap.dedent('''\
        datetime|amount|desc
        2020-01-01 00:00:00+00:00|+5|First gift
        2020-01-03 00:00:00+00:00|+7.500|Second gift
        2020-01-05 00:00:00+00:00|-3.1|First expense
        2020-01-05 00:00:00+00:00|+0|Zero
        2020-01-05 00:00:00+00:00|-0|Negative zero
    ''')

    data, delimiter = load_data(io.StringIO(csv))

    assert data == data_out_expected
    assert delimiter == '|'

    csv = textwrap.dedent('''\
        sep=/
        datetime/amount/desc
        2020-01-01 00:00:00+00:00/+5/First gift
        2020-01-03 00:00:00+00:00/+7.500/Second gift
        2020-01-05 00:00:00+00:00/-3.1/First expense
        2020-01-05 00:00:00+00:00/+0/Zero
        2020-01-05 00:00:00+00:00/-0/Negative zero
    ''')

    data, delimiter = load_data(io.StringIO(csv))

    assert data == data_out_expected
    assert delimiter == '/'

    with pytest.raises(ValueError) as exc_info:
        load_data(io.StringIO('This is invalid content'))
    assert exc_info.value.args == (
        'Content must start with either "sep=" or "datetime"',)

    csv = textwrap.dedent('''\
        datetime,amount,desc
        2020-01-01 00:00:00+00:00,123,
    ''')

    with pytest.raises(ValueError) as exc_info:
        load_data(io.StringIO(csv))
    assert exc_info.value.args == ('Amount 123 does not start with - or +',)

    csv = textwrap.dedent('''\
        datetime,amount,desc
        2020-01-01 00:00:00+00:00,+10,
        2020-01-05 00:00:00+00:00,+20,
        2020-01-03 00:00:00+00:00,+30,
    ''')

    with pytest.raises(ValueError) as exc_info:
        load_data(io.StringIO(csv))
    assert exc_info.value.args == (
        'Invalid entry order: 2020-01-05 00:00:00+00:00 > '
        '2020-01-03 00:00:00+00:00',)


def test_save_data():
    data = [
        {'datetime': dt(2020, 1, 1, tzinfo=tz.utc),
         'amount': 5, 'total': 5, 'desc': 'First gift'},
        {'datetime': dt(2020, 1, 3, tzinfo=tz.utc),
         'amount': 7.5, 'total': 12.5, 'desc': 'Second gift'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': -3.1, 'total': 9.4, 'desc': 'First expense'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': 0, 'total': 9.4, 'desc': 'First zero'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': 0, 'total': 9.4, 'desc': 'Second zero'},
    ]

    csv = textwrap.dedent('''\
        datetime,amount,total,desc
        2020-01-01 00:00:00+00:00,5,5,First gift
        2020-01-03 00:00:00+00:00,7.5,12.5,Second gift
        2020-01-05 00:00:00+00:00,-3.1,9.4,First expense
        2020-01-05 00:00:00+00:00,0,9.4,First zero
        2020-01-05 00:00:00+00:00,0,9.4,Second zero
    ''')

    buf = io.StringIO()
    save_data(data, buf)
    buf.seek(0)

    assert buf.read() == csv

    csv = textwrap.dedent('''\
        datetime|amount|total|desc
        2020-01-01 00:00:00+00:00|5|5|First gift
        2020-01-03 00:00:00+00:00|7.5|12.5|Second gift
        2020-01-05 00:00:00+00:00|-3.1|9.4|First expense
        2020-01-05 00:00:00+00:00|0|9.4|First zero
        2020-01-05 00:00:00+00:00|0|9.4|Second zero
    ''')

    buf = io.StringIO()
    save_data(data, buf, '|')
    buf.seek(0)

    assert buf.read() == csv

    csv = textwrap.dedent('''\
        datetime;amount;total;desc
        2020-01-01 00:00:00+00:00;+5.00;5.00;First gift
        2020-01-03 00:00:00+00:00;+7.50;12.50;Second gift
        2020-01-05 00:00:00+00:00;-3.10;9.40;First expense
        2020-01-05 00:00:00+00:00;+0.00;9.40;First zero
        2020-01-05 00:00:00+00:00;+0.00;9.40;Second zero
    ''')

    buf = io.StringIO()
    save_data(data, buf, ';', '{:+.2f}', '{:.2f}')
    buf.seek(0)

    assert buf.read() == csv


def test_compute_totals():
    data_in_orig = [
        {'datetime': dt(2020, 1, 1, tzinfo=tz.utc),
         'amount': 5, 'desc': 'First gift'},
        {'datetime': dt(2020, 1, 3, tzinfo=tz.utc),
         'amount': 7.5, 'desc': 'Second gift'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': -3.1, 'desc': 'First expense'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': 0, 'desc': 'First zero'},
    ]

    data_out_expected = [
        {'datetime': dt(2020, 1, 1, tzinfo=tz.utc),
         'amount': 5, 'total': 5, 'desc': 'First gift'},
        {'datetime': dt(2020, 1, 3, tzinfo=tz.utc),
         'amount': 7.5, 'total': 12.5, 'desc': 'Second gift'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': -3.1, 'total': 9.4, 'desc': 'First expense'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': 0, 'total': 9.4, 'desc': 'First zero'},
    ]

    data_in = [x.copy() for x in data_in_orig]
    data_in_copy = [x.copy() for x in data_in]
    data_out = list(compute_totals(data_in))
    assert data_in == data_in_copy
    assert data_out == data_out_expected
