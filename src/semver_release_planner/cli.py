import sys
from semver_release_planner.planner import (
    get_commits_since_last_tag,
    get_current_version,
    calculate_next_version,
    generate_changelog
)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "changelog":
        current_v = get_current_version()
        commits = get_commits_since_last_tag()
        next_v = calculate_next_version(current_v, commits)
        print(generate_changelog(commits, next_v))
    else:
        current_v = get_current_version()
        commits = get_commits_since_last_tag()
        next_v = calculate_next_version(current_v, commits)
        print(f"Current Version: {current_v}")
        print(f"Next Version:    {next_v}")
        print(f"Commits found:   {len(commits)}")

if __name__ == "__main__":
    main()
