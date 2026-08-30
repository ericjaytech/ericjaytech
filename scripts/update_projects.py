"""Refresh the featured-projects block in the GitHub profile README."""

from __future__ import annotations

import datetime as dt
import html
import json
import os
from pathlib import Path
from typing import Any
from urllib import request

README_PATH = Path("README.md")
START_MARKER = "<!-- PROJECTS:START -->"
END_MARKER = "<!-- PROJECTS:END -->"
MAX_PROJECTS = 3


def _github_api_get(url: str) -> list[dict[str, Any]]:
    """Return decoded JSON from a GitHub API list endpoint."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ericjaytech-profile-readme",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    api_request = request.Request(url, headers=headers)
    with request.urlopen(api_request, timeout=30) as response:
        payload = json.load(response)

    if not isinstance(payload, list):
        raise TypeError("Expected a list response from the GitHub repositories API.")

    return payload


def _shorten(text: str, limit: int = 150) -> str:
    """Return a compact description without breaking words unnecessarily."""
    cleaned = " ".join(text.split())
    if len(cleaned) <= limit:
        return cleaned

    shortened = cleaned[: limit - 1].rsplit(" ", 1)[0]
    return f"{shortened}…"


def _format_month(timestamp: str | None) -> str:
    """Format an ISO GitHub timestamp as an abbreviated month and year."""
    if not timestamp:
        return ""

    parsed = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return parsed.strftime("%b %Y")


def _select_repositories(
    repositories: list[dict[str, Any]],
    owner: str,
) -> list[dict[str, Any]]:
    """Choose recent, public, original repositories for the profile."""
    candidates = [
        repo
        for repo in repositories
        if not repo.get("fork", False)
        and not repo.get("archived", False)
        and repo.get("name", "").casefold() != owner.casefold()
    ]

    candidates.sort(
        key=lambda repo: repo.get("pushed_at") or "",
        reverse=True,
    )

    described = [repo for repo in candidates if repo.get("description")]
    undescribed = [repo for repo in candidates if not repo.get("description")]

    return (described + undescribed)[:MAX_PROJECTS]


def _render_projects(repositories: list[dict[str, Any]]) -> str:
    """Render selected repositories as a compact full-width HTML table."""
    if not repositories:
        return (
            f"{START_MARKER}\n"
            '<table width="100%">\n'
            "<tr><td>\n"
            "<strong>Public projects are on the way.</strong><br/>\n"
            "<sub>This section will refresh automatically as repositories "
            "are published.</sub>\n"
            "</td></tr>\n"
            "</table>\n"
            f"{END_MARKER}"
        )

    rows = []
    for repo in repositories:
        name = html.escape(str(repo.get("name", "Project")))
        url = html.escape(str(repo.get("html_url", "#")), quote=True)
        description = html.escape(
            _shorten(str(repo.get("description") or "Public project."))
        )
        language = html.escape(str(repo.get("language") or "Repository"))
        updated = _format_month(repo.get("pushed_at"))
        stars = int(repo.get("stargazers_count") or 0)

        metadata = f"<code>{language}</code>"
        if stars:
            metadata += f" · ★ {stars}"
        if updated:
            metadata += f"<br/><sub>updated {updated}</sub>"

        rows.append(
            "<tr>\n"
            '<td width="72%" valign="top">\n'
            f'<a href="{url}"><strong>{name}</strong></a><br/>\n'
            f"<sub>{description}</sub>\n"
            "</td>\n"
            '<td width="28%" align="right" valign="top">\n'
            f"{metadata}\n"
            "</td>\n"
            "</tr>"
        )

    return (
        f"{START_MARKER}\n"
        '<table width="100%">\n'
        + "\n".join(rows)
        + "\n</table>\n"
        + END_MARKER
    )


def _replace_block(readme: str, replacement: str) -> str:
    """Replace the dynamic project section while preserving hand-written copy."""
    start = readme.find(START_MARKER)
    end = readme.find(END_MARKER)

    if start == -1 or end == -1 or end < start:
        raise ValueError("README project markers are missing or out of order.")

    end += len(END_MARKER)
    return f"{readme[:start]}{replacement}{readme[end:]}"


def main() -> None:
    """Fetch repositories and update README.md when the rendered block changes."""
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "ericjaytech")
    url = (
        f"https://api.github.com/users/{owner}/repos"
        "?per_page=100&sort=pushed&direction=desc"
    )

    repositories = _github_api_get(url)
    selected = _select_repositories(repositories, owner)
    replacement = _render_projects(selected)

    current = README_PATH.read_text(encoding="utf-8")
    updated = _replace_block(current, replacement)

    if updated == current:
        print("README project block is already current.")
        return

    README_PATH.write_text(updated, encoding="utf-8")
    print(f"Updated README with {len(selected)} featured project(s).")


if __name__ == "__main__":
    main()
