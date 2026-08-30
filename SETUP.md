# Eric Jay GitHub Profile — V2 setup

This bundle is designed for the special GitHub profile repository:

`ericjaytech/ericjaytech`

## What changed in V2

- Shorter hero subtitle so it renders cleanly at GitHub's profile width.
- Wider, more restrained header artwork with an abstract systems motif.
- Larger and cleaner contact buttons.
- Less CV-style repetition above the fold.
- Full-width capability and impact sections.
- A dynamic **Selected projects** section that refreshes from Eric's public repositories.
- Contribution animation retained, with light/dark mode support.
- Profile-view counter moved to the footer where it does not compete with the branding.

## Install

Copy these files into the repository root, preserving their paths:

- `README.md`
- `assets/header.svg`
- `.github/workflows/update-projects.yml`
- `.github/workflows/snake.yml`
- `scripts/update_projects.py`

Then commit and push to `main`.

## First run

Open the repository's **Actions** tab and manually run:

1. **Refresh featured projects**
2. **Generate contribution animation**

The project workflow will replace only the content between:

- `<!-- PROJECTS:START -->`
- `<!-- PROJECTS:END -->`

Everything outside those markers remains hand-maintained.

## Workflow permissions

If either workflow receives a permissions error:

1. Open **Settings → Actions → General**.
2. Find **Workflow permissions**.
3. Allow **Read and write permissions** for the repository.
4. Run the workflow again.

## Dynamic-project selection

The project updater selects up to three repositories that are:

- public;
- not forks;
- not archived; and
- not the `ericjaytech` profile repository itself.

Repositories with descriptions are preferred, then sorted by recent pushes. This means the
profile improves naturally as Eric publishes stronger work without turning the README into
a noisy GitHub-statistics dashboard.

## Recommended repository hygiene

For anything intended to appear on the profile:

- give the repository a concise description;
- add a strong README;
- include a useful screenshot or diagram where appropriate;
- set relevant repository topics; and
- archive experiments that should no longer be surfaced.

The dynamic section is only as strong as the underlying public repositories.
