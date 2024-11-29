import os
import pytest
from unittest.mock import patch, mock_open
from homework2.src.main import read_config, get_commit_hash_by_tag, build_dependency_graph


# Тестирование функции read_config
@patch("builtins.open", new_callable=mock_open, read_data="key: value")
def test_read_config(mock_file):
    config_path = "dummy_path"
    result = read_config(config_path)
    assert result == {"key": "value"}


# Тестирование функции get_commit_hash_by_tag
@patch("homework2.src.main.os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data="commit_hash")
def test_get_commit_hash_by_tag(mock_file, mock_exists):
    repo_path = "dummy_repo"
    tag_name = "v1.0.0"
    result = get_commit_hash_by_tag(repo_path, tag_name)
    assert result == "commit_hash"


# Тестирование функции build_dependency_graph
@patch("homework2.src.main.read_git_object", return_value="commit_content")
@patch("homework2.src.main.parse_commit", return_value=(["parent_hash"], "commit_message"))
def test_build_dependency_graph(mock_parse_commit, mock_read_object):
    repo_path = "dummy_repo"
    start_commit = "commit_hash"

    result = build_dependency_graph(repo_path, start_commit)

    # Ожидаемый граф
    expected_graph = [
        ("commit_hash", "parent_hash", "commit_message"),
        ("parent_hash", "parent_hash", "commit_message"),
    ]

    # Сравниваем множества для независимости от порядка
    assert set(result) == set(expected_graph)
