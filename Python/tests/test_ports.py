import pytest

from scanner.utils.ports import parse_ports, PortParseError


def test_single_port():
    assert parse_ports("22") == [22]


def test_multiple_ports():
    assert parse_ports("22,80,443") == [22, 80, 443]


def test_port_range():
    assert parse_ports("80-82") == [80, 81, 82]


def test_mixed_ports():
    assert parse_ports("22,80-82,443") == [22, 80, 81, 82, 443]


def test_invalid_port():
    with pytest.raises(PortParseError):
        parse_ports("abc")


def test_out_of_range_port():
    with pytest.raises(PortParseError):
        parse_ports("70000")


def test_reverse_range():
    with pytest.raises(PortParseError):
        parse_ports("100-1")
