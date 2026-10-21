import pytest
from unittest.mock import patch, MagicMock
from semver_release_planner.planner import get_current_version, parse_version_tag

def test_custom_prefix_version_stripping():
    """Test custom git tag prefix stripping and parsing (e.g. 'release/v1.0.0')."""
    mock_run_result = MagicMock()
    mock_run_result.stdout = "release/v1.0.0\n"
    
    with patch("subprocess.run", return_value=mock_run_result):
        version = get_current_version()
        assert version == "1.0.0"

def test_parse_version_tag():
    assert parse_version_tag("v2.4.1") == "2.4.1"
    assert parse_version_tag("app-v1.0.3") == "1.0.3"
    assert parse_version_tag("release/v3.0.0-rc.1") == "3.0.0-rc.1"
