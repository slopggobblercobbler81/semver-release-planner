"""semver-release-planner: Semantic versioning release calculator, breaking change analyzer, and changelog sequencer."""

from semver_release_planner.planner import (
    Commit,
    ReleasePlan,
    analyze_commits,
    calculate_next_version,
    generate_changelog,
)

__version__ = "1.0.0"

__all__ = [
    "Commit",
    "ReleasePlan",
    "analyze_commits",
    "calculate_next_version",
    "generate_changelog",
    "__version__",
]
