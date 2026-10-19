# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "codeowners>=0.7",
#     "httpx>=0.28",
# ]
# ///
"""Check that all CODEOWNERS ownership groups have approved a pull request.

This script is intended to run in a GitHub Actions workflow. It reads
environment variables set by the workflow to determine the PR context,
parses the CODEOWNERS file, and sets a commit status based on whether
all required approvals are present.

Required environment variables:
    GITHUB_TOKEN: Token with org:read, statuses:write, and pull_request:read
    PR_NUMBER: Pull request number
    PR_AUTHOR: GitHub username of the PR author
    REPO: Repository in "owner/repo" format
    SHA: Commit SHA to set the status on
    RUN_URL: URL to the workflow run for the status target_url
    GITHUB_STEP_SUMMARY: Path to the step summary file (set by Actions)
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

import httpx
from codeowners import CodeOwners

STATUS_CONTEXT = "codeowner-approval"

logger = logging.getLogger(__name__)


def main() -> None:
    """Check codeowner approvals and set a commit status on the PR."""
    logging.basicConfig(level=logging.INFO)

    token = os.environ["GITHUB_TOKEN"]
    pr_number = os.environ["PR_NUMBER"]
    pr_author = os.environ["PR_AUTHOR"]
    repo = os.environ["REPO"]
    sha = os.environ["SHA"]
    run_url = os.environ.get("RUN_URL", "")

    org = repo.split("/")[0]

    client = httpx.Client(
        base_url="https://api.github.com",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=30,
    )

    # Parse CODEOWNERS
    codeowners_path = Path(".github/CODEOWNERS")
    if not codeowners_path.exists():
        codeowners_path = Path("CODEOWNERS")
    if not codeowners_path.exists():
        logger.info("No CODEOWNERS file found; setting status to success.")
        set_status(
            client, repo, sha, "success", "No CODEOWNERS file found", run_url
        )
        return

    codeowners = CodeOwners(codeowners_path.read_text())

    # Get changed files
    changed_files = get_changed_files(client, repo, pr_number)
    if not changed_files:
        logger.info("No changed files found.")
        set_status(client, repo, sha, "success", "No changed files", run_url)
        return

    # Group files by ownership
    owner_groups: dict[frozenset[str], list[str]] = {}
    for filepath in changed_files:
        owners = codeowners.of(filepath)
        if not owners:
            continue
        # owners is a list of (kind, name) tuples; extract the names
        owner_names = frozenset(name for _kind, name in owners)
        owner_groups.setdefault(owner_names, []).append(filepath)

    if not owner_groups:
        logger.info(
            "No changed files have codeowners; setting status to success."
        )
        set_status(
            client, repo, sha, "success", "No codeowner rules apply", run_url
        )
        return

    # Get approving reviewers
    approving_reviewers = get_approving_reviewers(client, repo, pr_number)

    # Check each ownership group
    results: list[GroupResult] = []
    all_satisfied = True

    for owner_names, files in sorted(
        owner_groups.items(), key=lambda x: sorted(x[0])
    ):
        satisfied, approver = check_group_satisfied(
            client, org, pr_author, approving_reviewers, owner_names
        )
        results.append(
            GroupResult(
                owners=sorted(owner_names),
                files=files,
                satisfied=satisfied,
                approver=approver,
            )
        )
        if not satisfied:
            all_satisfied = False

    _report_results(
        client,
        repo=repo,
        sha=sha,
        run_url=run_url,
        results=results,
        all_satisfied=all_satisfied,
    )


def _report_results(
    client: httpx.Client,
    *,
    repo: str,
    sha: str,
    run_url: str,
    results: list[GroupResult],
    all_satisfied: bool,
) -> None:
    """Build a description from results, set the commit status, and exit."""
    if all_satisfied:
        description = "All codeowner approvals satisfied"
        state = "success"
    else:
        pending = [r for r in results if not r.satisfied]
        pending_owners = ", ".join(" ".join(r.owners) for r in pending)
        description = f"Pending approval from: {pending_owners}"
        # GitHub status descriptions are limited to 140 characters
        if len(description) > 140:
            description = description[:137] + "..."
        state = "failure"

    set_status(client, repo, sha, state, description, run_url)
    write_summary(results, all_satisfied=all_satisfied)

    if not all_satisfied:
        logger.warning("FAILED: %s", description)
        sys.exit(1)
    else:
        logger.info("SUCCESS: %s", description)


class GroupResult:
    """Result of checking a single ownership group."""

    def __init__(
        self,
        owners: list[str],
        files: list[str],
        *,
        satisfied: bool,
        approver: str,
    ) -> None:
        self.owners = owners
        self.files = files
        self.satisfied = satisfied
        self.approver = approver


def get_changed_files(
    client: httpx.Client, repo: str, pr_number: str
) -> list[str]:
    """Get all changed files in a pull request (paginated)."""
    files: list[str] = []
    page = 1
    while True:
        resp = client.get(
            f"/repos/{repo}/pulls/{pr_number}/files",
            params={"per_page": 100, "page": page},
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        files.extend(item["filename"] for item in data)
        if len(data) < 100:
            break
        page += 1
    return files


def get_approving_reviewers(
    client: httpx.Client, repo: str, pr_number: str
) -> set[str]:
    """Get the set of users who have given an approving review.

    Only considers the latest review from each user; if a user approved
    and then later requested changes, the approval is not counted.
    """
    page = 1
    # Map from reviewer login to their latest review state
    latest_reviews: dict[str, str] = {}
    while True:
        resp = client.get(
            f"/repos/{repo}/pulls/{pr_number}/reviews",
            params={"per_page": 100, "page": page},
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        for review in data:
            user = review["user"]["login"]
            state = review["state"]
            # Only track meaningful states
            if state in ("APPROVED", "CHANGES_REQUESTED", "DISMISSED"):
                latest_reviews[user] = state
        if len(data) < 100:
            break
        page += 1
    return {
        user for user, state in latest_reviews.items() if state == "APPROVED"
    }


def is_team_member(
    client: httpx.Client, org: str, team_slug: str, username: str
) -> bool:
    """Check if a user is a member of an organization team."""
    resp = client.get(f"/orgs/{org}/teams/{team_slug}/members/{username}")
    # 204 = is a member, 404 = not a member
    return resp.status_code == 204


def is_owner_match(
    client: httpx.Client, org: str, username: str, owner: str
) -> bool:
    """Check if a username matches an owner entry.

    Owner entries can be either @username or @org/team-name.
    """
    # Strip leading @
    owner_clean = owner.lstrip("@")
    if "/" in owner_clean:
        # Team reference: org/team-slug
        team_slug = owner_clean.split("/", 1)[1]
        return is_team_member(client, org, team_slug, username)
    else:
        # Individual user
        return username.lower() == owner_clean.lower()


def check_group_satisfied(
    client: httpx.Client,
    org: str,
    pr_author: str,
    approving_reviewers: set[str],
    owner_names: frozenset[str],
) -> tuple[bool, str]:
    """Check if an ownership group's approval requirement is satisfied.

    Returns (satisfied, approver_name). The approver is the PR author if
    they are a member of the owning group, or the first approving reviewer
    who is a member.
    """
    # Check if PR author is a member of any owner in this group
    for owner in owner_names:
        if is_owner_match(client, org, pr_author, owner):
            return True, f"{pr_author} (author)"

    # Check if any approving reviewer is a member
    for reviewer in sorted(approving_reviewers):
        for owner in owner_names:
            if is_owner_match(client, org, reviewer, owner):
                return True, reviewer

    return False, ""


def set_status(
    client: httpx.Client,
    repo: str,
    sha: str,
    state: str,
    description: str,
    target_url: str,
) -> None:
    """Set a commit status on the given SHA."""
    resp = client.post(
        f"/repos/{repo}/statuses/{sha}",
        json={
            "state": state,
            "description": description,
            "context": STATUS_CONTEXT,
            "target_url": target_url,
        },
    )
    resp.raise_for_status()


def write_summary(results: list[GroupResult], *, all_satisfied: bool) -> None:
    """Write a GitHub Actions step summary."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    lines: list[str] = []
    status = (
        "All approvals satisfied" if all_satisfied else "Pending approvals"
    )
    lines.append(f"## CODEOWNERS Approval: {status}\n")
    lines.append("| Owners | Status | Approved By | Files |")
    lines.append("|--------|--------|-------------|-------|")

    for result in results:
        owners_str = " ".join(f"`{o}`" for o in result.owners)
        if result.satisfied:
            status_str = "Approved"
            approver_str = result.approver
        else:
            status_str = "**Pending**"
            approver_str = "-"
        # Show first 3 files, with count if more
        if len(result.files) <= 3:
            files_str = ", ".join(f"`{f}`" for f in result.files)
        else:
            files_str = ", ".join(f"`{f}`" for f in result.files[:3])
            files_str += f" (+{len(result.files) - 3} more)"
        lines.append(
            f"| {owners_str} | {status_str} | {approver_str} | {files_str} |"
        )

    with Path(summary_path).open("a") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
