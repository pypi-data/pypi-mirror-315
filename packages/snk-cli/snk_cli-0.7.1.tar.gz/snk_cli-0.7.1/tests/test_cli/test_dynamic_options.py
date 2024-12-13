import pytest
from snk_cli.config import SnkConfig
from snk_cli.options import Option
from snk_cli.options.utils import (
    create_option_from_annotation,
    build_dynamic_cli_options,
)


@pytest.fixture
def default_annotation_values():
    return {
        "test:name": "Test",
        "test:default": "default_value",
        "test:type": "str",
        "test:help": "Test help",
        "test:required": True,
    }


@pytest.fixture
def default_default_values():
    return {"test": "default_value"}


def test_create_option_from_annotation(
    default_annotation_values, default_default_values
):
    option = create_option_from_annotation(
        "test", default_annotation_values, default_default_values
    )

    assert isinstance(option, Option)
    assert option.name == "Test"
    assert option.default == "default_value"
    assert option.updated is False
    assert option.help == "Test help"
    assert option.type is str
    assert option.required is True


def test_create_option_from_annotation_type_Case_insensitive(
    default_annotation_values, default_default_values
):
    default_annotation_values["test:type"] = "STR"
    option = create_option_from_annotation(
        "test", default_annotation_values, default_default_values
    )
    assert option.type is str


def test_create_option_from_annotation_with_short(
    default_annotation_values, default_default_values
):
    default_annotation_values["test:short"] = "t"

    option = create_option_from_annotation(
        "test", default_annotation_values, default_default_values
    )

    assert option.short == "t"

def test_create_option_from_annotation_with_hidden(
    default_annotation_values, default_default_values
):
    default_annotation_values["test:hidden"] = True

    option = create_option_from_annotation(
        "test", default_annotation_values, default_default_values
    )

    assert option.hidden is True

def test_create_option_from_annotation_with_enums(
    default_annotation_values, default_default_values
):
    default_annotation_values["test:choices"] = ["a", "b", "c"]

    option = create_option_from_annotation(
        "test", default_annotation_values, default_default_values
    )

    assert option.choices == ["a", "b", "c"]


@pytest.fixture
def default_snakemake_config():
    return {
        "param1": "value1",
        "param2": "value2",
    }


@pytest.fixture
def default_snk_config():
    return SnkConfig(
        {
            "annotations": {
                "param1:name": "Parameter 1",
                "param2:name": "Parameter 2",
            }
        }
    )


def test_build_dynamic_cli_options(default_snakemake_config, default_snk_config):
    options = build_dynamic_cli_options(default_snakemake_config, default_snk_config)

    assert len(options) == 2
    assert all(isinstance(option, Option) for option in options)
    assert set([option.name for option in options]) == {"param1", "param2"}
