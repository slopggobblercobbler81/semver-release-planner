import pytest
from semver_release_planner.planner import Commit, calculate_next_version, generate_changelog

def test_commit_parsing():
    c1 = Commit("abcdef123", "feat(auth): add login endpoint")
    assert c1.type == "feat"
    assert c1.scope == "auth"
    assert c1.breaking is False
    assert c1.description == "add login endpoint"

    c2 = Commit("abcdef456", "fix!: critical security patch", "BREAKING CHANGE: api changed")
    assert c2.type == "fix"
    assert c2.breaking is True

def test_calculate_next_version():
    c_feat = [Commit("111", "feat: new feature")]
    c_fix = [Commit("222", "fix: bugfix")]
    c_break = [Commit("333", "feat!: breaking change")]

    assert calculate_next_version("1.2.3", c_fix) == "1.2.4"
    assert calculate_next_version("1.2.3", c_feat) == "1.3.0"
    assert calculate_next_version("1.2.3", c_break) == "2.0.0"

def test_generate_changelog():
    commits = [
        Commit("1234567", "feat(ui): add button"),
        Commit("abcdef0", "fix(api): resolve timeout")
    ]
    changelog = generate_changelog(commits, "1.1.0")
    assert "# Changelog" in changelog
    assert "## v1.1.0" in changelog
    assert "add button" in changelog
    assert "resolve timeout" in changelog
#endif
