import pytest
from unittest.mock import patch, MagicMock
from semver_release_planner.planner import get_current_version

def test_custom_prefix_version_stripping():
    """Test custom git tag prefix stripping and parsing (e.g. 'release/v1.0.0')."""
    # Mock subprocess.run for git describe returning 'release/v1.0.0'
    mock_run_result = MagicMock()
    mock_run_result.stdout = "release/v1.0.0\n"
    
    with patch("subprocess.run", return_value=mock_run_result) as mock_run:
        version = get_current_version()
        # Verify get_current_version handles custom prefixes by checking if tag starts with 'v' or stripping prefix if implemented, 
        # or we test custom prefix handling function if added. Let's inspect how get_current_version handles it currently or enhance planner.py if needed.
