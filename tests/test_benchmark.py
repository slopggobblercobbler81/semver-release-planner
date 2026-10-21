import time
import pytest
from semver_release_planner.planner import Commit, calculate_next_version, generate_changelog

def test_benchmark_commit_parsing():
    """Benchmark parsing overhead for bulk conventional commit analysis."""
    commit_messages = [
        ("hash_feat", "feat(core): implement new feature number {i}"),
        ("hash_fix", "fix(api): resolve issue {i}"),
        ("hash_chore", "chore: minor housekeeping {i}"),
        ("hash_break", "feat(auth)!: major breaking authentication change {i}")
    ]
    
    start_time = time.perf_counter()
    commits = []
    for i in range(1000):
        h, msg = commit_messages[i % len(commit_messages)]
        commits.append(Commit(f"{h}_{i}", msg.format(i=i)))
    duration = time.perf_counter() - start_time

    assert len(commits) == 1000
    assert duration < 1.0

def test_benchmark_version_calculation():
    """Benchmark calculation of next semantic version across 1,000 commits."""
    commits = [
        Commit(f"h_{i}", f"feat: add feature {i}") for i in range(500)
    ] + [
        Commit(f"h_{i}", f"fix: resolve bug {i}") for i in range(500, 1000)
    ]
    
    start_time = time.perf_counter()
    next_ver = calculate_next_version("1.2.3", commits)
    duration = time.perf_counter() - start_time

    assert next_ver == "1.3.0"
    assert duration < 0.5

def test_benchmark_changelog_generation():
    """Benchmark markdown changelog rendering with 400 grouped commits."""
    commits = [
        Commit(f"h_feat_{i}", f"feat(module): feature item {i}") for i in range(200)
    ] + [
        Commit(f"h_fix_{i}", f"fix(module): bug fix item {i}") for i in range(200)
    ]

    start_time = time.perf_counter()
    changelog = generate_changelog(commits, "2.0.0")
    duration = time.perf_counter() - start_time

    assert "## v2.0.0" in changelog
    assert len(changelog) > 0
    assert duration < 0.5
