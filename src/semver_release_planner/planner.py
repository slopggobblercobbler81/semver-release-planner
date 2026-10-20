import re
import subprocess
from typing import List, Tuple, Dict, Optional

class Commit:
    def __init__(self, commit_hash: str, subject: str, body: str = ""):
        self.hash = commit_hash
        self.subject = subject
        self.body = body
        self.type, self.scope, self.breaking, self.description = self._parse_conventional(subject, body)

    def _parse_conventional(self, subject: str, body: str) -> Tuple[str, Optional[str], bool, str]:
        # Pattern: type(scope)?: description or type!: description
        pattern = r"^([a-z]+)(?:\(([^)]+)\))?(!)?:\s+(.*)$"
        match = re.match(pattern, subject)
        if not match:
            return "other", None, False, subject
        
        c_type, scope, breaking_excl, desc = match.groups()
        breaking = bool(breaking_excl) or ("BREAKING CHANGE" in body) or ("BREAKING-CHANGE" in body)
        return c_type, scope, breaking, desc

def get_commits_since_last_tag() -> List[Commit]:
    try:
        tag_result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True, text=True, check=True
        )
        last_tag = tag_result.stdout.strip()
        rev_range = f"{last_tag}..HEAD"
    except subprocess.CalledProcessError:
        rev_range = "HEAD"

    log_result = subprocess.run(
        ["git", "log", rev_range, "--format=%H%x1f%s%x1f%b%x1e"],
        capture_output=True, text=True, check=True
    )
    
    commits = []
    raw_commits = log_result.stdout.split("\x1e")
    for raw in raw_commits:
        parts = raw.strip().split("\x1f")
        if len(parts) >= 2 and parts[0]:
            commit_hash = parts[0]
            subject = parts[1]
            body = parts[2] if len(parts) > 2 else ""
            commits.append(Commit(commit_hash, subject, body))
            
    return commits

def get_current_version() -> str:
    try:
        tag_result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True, text=True, check=True
        )
        tag = tag_result.stdout.strip()
        if tag.startswith('v'):
            tag = tag[1:]
        return tag
    except subprocess.CalledProcessError:
        return "0.0.0"

def calculate_next_version(current_version: str, commits: List[Commit]) -> str:
    parts = current_version.split('.')
    major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
    minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
    patch = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0

    has_breaking = any(c.breaking for c in commits)
    has_feat = any(c.type == 'feat' for c in commits)
    has_fix = any(c.type == 'fix' for c in commits)

    if has_breaking:
        major += 1
        minor = 0
        patch = 0
    elif has_feat:
        minor += 1
        patch = 0
    elif has_fix or len(commits) > 0:
        patch += 1

    return f"{major}.{minor}.{patch}"

def generate_changelog(commits: List[Commit], version: str) -> str:
    features = [c for c in commits if c.type == 'feat']
    fixes = [c for c in commits if c.type == 'fix']
    breaking = [c for c in commits if c.breaking]

    lines = [f"# Changelog\n", f"## v{version}\n"]
    
    if breaking:
        lines.append("### Breaking Changes\n")
        for c in breaking:
            scope_str = f"({c.scope}): " if c.scope else ""
            lines.append(f"- **{c.type}** {scope_str}{c.description} ({c.hash[:7]})")
        lines.append("")

    if features:
        lines.append("### Features\n")
        for c in features:
            scope_str = f"({c.scope}): " if c.scope else ""
            lines.append(f"- {scope_str}{c.description} ({c.hash[:7]})")
        lines.append("")

    if fixes:
        lines.append("### Bug Fixes\n")
        for c in fixes:
            scope_str = f"({c.scope}): " if c.scope else ""
            lines.append(f"- {scope_str}{c.description} ({c.hash[:7]})")
        lines.append("")

    return "\n".join(lines)
