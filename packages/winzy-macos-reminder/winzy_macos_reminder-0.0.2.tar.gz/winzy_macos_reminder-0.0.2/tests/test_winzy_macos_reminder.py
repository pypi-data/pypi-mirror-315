import pytest
import winzy_macos_reminder as w

from argparse import Namespace, ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(["hello"])
    assert result.description == "hello"
    assert result.datetime is None
    assert result.date_format == "%d/%m/%Y"


def test_plugin(capsys):
    w.remind_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
