import json
from pathlib import Path

import pytest
import yaml

import openapi_main

resource_parent = Path("resources")
schema_path = resource_parent / Path("openapi/openapi.yaml")
content_success_path = resource_parent / Path("json/test-openapi.json")
content_success_path2 = resource_parent / Path("json/test-openapi-lunch.json")
content_fail_path = resource_parent / Path("json/test-region-no-area.json")
content_empty_path = resource_parent / Path("json/empty.json")


def test_check_file() -> None:
    files = [
        schema_path,
        content_success_path,
        content_success_path2,
        content_fail_path,
        content_empty_path,
    ]
    for p in files:
        assert p.exists()
    return


@pytest.mark.parametrize("json_path, def_name, ", [
    (content_success_path, "User"),
    (content_success_path2, "lunch"),
])
def test_success(json_path: Path, def_name: str) -> None:
    schema = get_schema(schema_path, def_name)
    content = get_json(json_path)
    errors = openapi_main.do_validation(schema, [("", content)])
    assert not errors
    pass


def test_fail() -> None:
    schema = get_schema(schema_path, "User")
    path = content_fail_path
    content = get_json(path)
    errors = openapi_main.do_validation(schema, [(str(path), content)])
    assert errors
    assert len(errors) == 1
    file_name, error = errors[0]
    assert file_name == str(path)
    return


@pytest.mark.parametrize("def_name, ", [
    "User",
    "lunch",
])
def test_fail_empty(def_name: str) -> None:
    schema = get_schema(schema_path, def_name)
    path = content_empty_path
    content = get_json(path)
    errors = openapi_main.do_validation(schema, [(str(path), content)])
    assert errors
    assert len(errors) == 1
    file_name, error = errors[0]
    assert file_name == str(path)
    return


@pytest.mark.parametrize("json_path, def_name, ", [
    (content_success_path, "lunch"),
    (content_success_path2, "User"),
])
def test_fail_wrong_definition(json_path: Path, def_name: str) -> None:
    schema = get_schema(schema_path, def_name)
    content = get_json(json_path)
    errors = openapi_main.do_validation(schema, [(str(json_path), content)])
    assert errors
    return


def get_json(p: Path) -> dict:
    with p.open() as f:
        return json.load(f)


def get_schema(p: Path, target: str) -> dict:
    with p.open() as f:
        return yaml.safe_load(f)["components"]["schemas"][target]
