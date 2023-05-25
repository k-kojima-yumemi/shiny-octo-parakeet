import json
from pathlib import Path

import json_main

resource_parent = Path("resources")
schema_path = resource_parent / Path("json-schema/regions.json")
content_success_path = resource_parent / Path("json/test-region.json")
content_fail_path = resource_parent / Path("json/test-region-no-area.json")
content_empty_path = resource_parent / Path("json/empty.json")


def test_check_file() -> None:
    files = [
        schema_path,
        content_success_path,
        content_fail_path,
        content_empty_path,
    ]
    for p in files:
        assert p.exists()
    return


def test_success() -> None:
    schema = get_json(schema_path)
    content = get_json(content_success_path)
    errors = json_main.do_validation(schema, [("", content)])
    assert not errors
    pass


def test_fail() -> None:
    schema = get_json(schema_path)
    path = content_fail_path
    content = get_json(path)
    errors = json_main.do_validation(schema, [(str(path), content)])
    assert errors
    assert len(errors) == 1
    file_name, error = errors[0]
    assert file_name == str(path)
    return


def test_fail_empty() -> None:
    schema = get_json(schema_path)
    path = content_empty_path
    content = get_json(path)
    errors = json_main.do_validation(schema, [(str(path), content)])
    assert errors
    assert len(errors) == 1
    file_name, error = errors[0]
    assert file_name == str(path)
    return


def get_json(p: Path) -> dict:
    with p.open() as f:
        return json.load(f)
