from pathlib import Path
from snk_cli.validate import validate_config
from snk_cli.config import SnkConfig
import pytest

@pytest.mark.parametrize("config,annotations,expected", [
    (
        {"example": "1"},
        {"example": {"type": "int"}},
        {"example": 1}
    ),
    (
        {"example": 1},
        {"example": {"type": "str"}},
        {"example": "1"}
    ),
    (
        {"example": "1"},
        {"example": {"type": "float"}},
        {"example": 1.0}
    ),
    (
        {"example": "1"},
        {"example": {"type": "bool"}},
        {"example": True}
    ),
    # timestamp
    (
        {"example": "2021-01-01T00:00:00"},
        {"example": {"type": "str"}},
        {"example": "2021-01-01T00:00:00"}
    ),
    # None
    (
        {"example": None},
        {"example": {"type": "int"}},
        {"example": None}
    ),
    (
        {"example": None},
        {"example": {"type": "str"}},
        {"example": None}
    ),
    (
        {"example": None},
        {"example": {"type": "float"}},
        {"example": None}
    ),
    (
        {"example": None},
        {"example": {"type": "bool"}},
        {"example": None}
    ),
    # path type
    (
        {"example": "file"},
        {"example": {"type": "path"}},
        {"example": Path("file")}
    ),
    # list type
    (
        {"example": ["1", "2"]},
        {"example": {"type": "list[int]"}},
        {"example": [1, 2]}
    ),
    (
        {"example": ["1", "2"]},
        {"example": {"type": "list[str]"}},
        {"example": ["1", "2"]}
    ),
    (
        {"example": ["1", "2"]},
        {"example": {"type": "list[path]"}},
        {"example": [Path("1"), Path("2")]}
    ),
    # pair type
    (
        {"example": ["1", "2"]},
        {"example": {"type": "pair[int, int]"}},
        {"example": [1, 2]}   
    ),
    # choices
    (
        {"example": "a"},
        {"example": {"type": "str", "choices": ["a", "b"]}},
        {"example": "a"}
    ),
    # nested dictionary
    (
        {"example": {"nested": "1"}},
        {"example": {"nested": {"type": "int"}}},
        {"example": {"nested": 1}}
    ),
    # exception
    (
        {"example": "1"},
        {"example": {"type": "unknown"}},
        ValueError
    ),
    (
        {"example": "s"},
        {"example": {"type": "int"}},
        Exception
    ),
    (
        {"example": "1"},
        {"example": {"type": "list[int]"}},
        Exception
    ),
    (
        {"example": {"nested": "1"}},
        {"example": {"nested": {"type": "list[int]"}}},
        Exception
    ),
    ])
def test_validate_config(tmp_path, config, annotations, expected):
    """
    Tests for validate_config().
    """
    snk_config_path = tmp_path / "snk.yaml"
    SnkConfig(cli=annotations).to_yaml(snk_config_path)
    if isinstance(expected, type):
        with pytest.raises(expected):
            validate_config(config, snk_config_path)
    else:
        validate_config(config, snk_config_path)
        assert config == expected