---
name: github-sync-workflow
description: Pull, push, import, export, publish, or reconcile project content with GitHub. Use when Codex needs to sync a local workspace with a GitHub repository, commit and push changes, pull remote changes, recover from authentication failures such as SSH publickey or HTTPS token prompts, use the GitHub connector as a fallback publishing path, verify where moved content appears on GitHub, align local Git metadata after connector-based updates, or list all files that will be uploaded, downloaded, or modified before a sync starts.
---

# GitHub Sync Workflow

Use this skill to move content between a local Codex workspace and GitHub without losing files, leaking credentials, or confusing local Git state.

## Core Rules

- Inspect the repository before changing anything: current branch, remote URL, status, recent commits, and ignored files.
- Treat a dirty working tree as user-owned until proven otherwise. Do not discard changes unless the user explicitly asks and the effect is clear.
- Never commit secrets, `.env` files, local Codex runtime state, local Git metadata backups, generated tenant-specific API snapshots, or machine-local files.
- For a public project repository, publish tracked, sanitized reusable content by default. This includes documentation, product context, schemas, reusable methods, generic queries and scripts, result profiles, and installable project skills. Do not exclude an artifact merely because it is detailed technical context or a reusable skill.
- Keep credentials, tokens, hostnames, usernames, IP addresses, GUIDs, tenant identifiers, raw endpoint evidence, raw API responses, organization-specific exports, and local execution logs out of GitHub.
- Do not add routine GitHub sync reports to `local/project-change-log.md`. If a sync publishes or downloads durable project changes, append a sanitized entry for the underlying project/content change, not for the sync mechanics.
- Append useful sync activity to `local/sync-activity-log.md`: GitHub push/pull results, connector fallback, authentication or permission issues, metadata reconciliation, and troubleshooting notes. Skip noise-only entries. This file is local-only and must never be staged, committed, or pushed.
- If the sync publishes a durable project decision or a change that should be remembered by future GitHub imports, verify that a sanitized decision record exists under `notes-and-memory/decisions/`. Do not treat the local-only project change log as sufficient for reusable project memory.
- After adding any local log entry, check whether the event produced a reusable lesson. If yes, promote the sanitized lesson into the appropriate GitHub-synced artifact: `notes-and-memory/decisions/`, `tools-and-memory/query-method-memory/`, `project-context/`, `product-context/`, `queries_and_scripts/catalog_result_profiles/`, or `skills/`.
- Use `rg`, `git status --short --branch`, `git log --oneline --decorate -5`, `git remote -v`, and `git check-ignore` to understand the sync surface.
- Prefer normal Git operations when local credentials work. Use the GitHub connector when terminal push fails or when the user wants to avoid local credentials.
- After connector-based publishing, reconcile local metadata because local Git may still think it is ahead, behind, or diverged.
- Before starting any sync that changes local files or GitHub, list the exact files expected to be uploaded, downloaded, deleted, or modified.

## Mandatory File Preview

Before running a pull, push, connector publish, temporary-clone publish, rebase, merge, reset, or any other sync step that changes local files or GitHub, show a concise file preview.

For uploads to GitHub, list files by status from local Git:

```bash
git status --short
git diff --name-status
git diff --cached --name-status
git ls-files --others --exclude-standard
```

Group the preview as:

- `Upload/new`: untracked or newly staged files that will be added to GitHub.
- `Upload/modified`: tracked files that will be changed on GitHub.
- `Upload/deleted`: tracked files that will be removed from GitHub.
- `Local-only ignored`: relevant ignored files that will not be uploaded, especially credentials, local runtime state, raw tenant snapshots, or Git metadata.

For downloads from GitHub, fetch first when network access is available, then list incoming remote changes before merging, rebasing, resetting, or pulling:

```bash
git fetch origin <branch>
git diff --name-status HEAD..origin/<branch>
```

Group the preview as:

- `Download/new`: files that will appear locally.
- `Download/modified`: local files that will be changed by the remote.
- `Download/deleted`: local files that will be removed by the remote.

For operations that both download and upload, show both previews before making changes. If a preview includes generated files, large reference files, public context, or reusable skills, still list them explicitly. If any file looks private or ambiguous, pause and inspect or ask before syncing.

## Standard Pull

1. Confirm the working tree state with `git status --short --branch`.
2. Fetch the tracked branch.
3. Show the mandatory download preview with `git diff --name-status HEAD..origin/<branch>`.
4. If clean, pull, merge, or fast-forward the tracked branch.
5. If dirty, identify changed files and protect user edits before pulling.
6. After pulling, report the new branch state and any visible content moves.

Use exact dates or commit hashes when explaining what changed.

## Standard Commit And Push

1. Review pending changes with `git status --short`, `git diff --stat`, and targeted diffs.
2. Check ignored/secret-sensitive paths before staging.
3. Show the mandatory upload preview before staging or committing. Include untracked files that will be added.
4. Stage only intended files.
5. Show the staged upload preview with `git diff --cached --name-status`.
6. Commit with a clear message.
7. Push the current branch.
8. Verify GitHub contains the expected files using the GitHub connector or a fetch.

If the push fails with `Permission denied (publickey)`, `could not read Username`, token prompts, or similar credential errors, do not keep retrying blindly. Switch to the connector fallback if available.

## macOS Prerequisites For Terminal GitHub Access

Use these checks before restoring HTTPS Git access on macOS:

```bash
git --version
brew --version
gh --version
git credential-manager --version
```

Required tools:

- Git, usually provided by Apple Command Line Tools or Homebrew.
- Homebrew, when installing missing CLI tools.
- GitHub CLI, installed with `brew install gh`.
- Git Credential Manager, installed with `brew install --cask git-credential-manager`.
- A browser session that can open `https://github.com/login/device` for GitHub CLI device-code authentication.

Recommended macOS install commands:

```bash
xcode-select --install
brew install gh
brew install --cask git-credential-manager
```

Check credential helper state:

```bash
git config --global --get-regexp 'credential|gh' || true
git config --system --get-regexp 'credential|gh' || true
```

Common macOS credential helpers include `osxkeychain`, Git Credential Manager, and the GitHub CLI helper. VS Code can push with its own GitHub login even when terminal Git has no valid credential, so verify terminal auth separately with `gh auth status` and a real `git push` or read-only `git ls-remote`.

## Restore GitHub CLI HTTPS Access

Use this workflow when HTTPS push fails because password authentication is not supported, Git cannot read a username, SSH public key authentication fails, or the GitHub CLI is installed but not logged in.

1. Check tools and auth state:

```bash
gh --version
gh auth status || true
git credential-manager --version || true
git config --global --get-regexp 'credential|gh' || true
```

2. Start GitHub CLI browser login for HTTPS Git operations:

```bash
gh auth login --hostname github.com --web --git-protocol https
```

3. When prompted, answer yes to authenticating Git with GitHub credentials. In non-interactive shells, preselect yes:

```bash
printf 'Y\n' | gh auth login --hostname github.com --web --git-protocol https
```

4. Have the user open `https://github.com/login/device`, enter the one-time device code printed by the CLI, and approve the login.

5. Verify the login:

```bash
gh auth status
```

Expected result: logged in to `github.com`, active account set, Git operations protocol `https`, and token scopes that include `repo` for private or write operations.

6. Configure Git to use GitHub CLI as the credential helper:

```bash
gh auth setup-git
git config --global --get-regexp 'credential|gh' || true
```

Expected GitHub helper entries include:

```text
credential.https://github.com.helper !.../gh auth git-credential
credential.https://gist.github.com.helper !.../gh auth git-credential
```

7. Retry the push:

```bash
git push origin <branch>
```

Important handling notes:

- GitHub does not support account passwords for Git operations. If Git prompts for a password over HTTPS, use a personal access token or configure `gh`/Git Credential Manager instead.
- Do not ask the user to paste tokens into chat.
- `gh auth login` may need write access to `~/.config/gh` to store `hosts.yml`.
- `gh auth setup-git` may need write access to `~/.gitconfig` and the temporary `~/.gitconfig.lock` file.
- If the CLI reports that credentials were saved in plain text, keep `~/.config/gh/hosts.yml` out of the project and never commit it.
- If terminal Git has no credential but VS Code can push, VS Code is using its own authentication session. Terminal access still needs `gh`, Git Credential Manager, SSH, or a personal access token.

## Temporary Clone Push Recovery

Use this when the main workspace has restricted Git metadata, for example a redirected `.git` file pointing to a local metadata backup that the sandbox cannot write.

1. Create a temporary clone under `/tmp`.
2. Before copying, list every file that will be copied into the temporary clone and every ignored/local file that will be excluded.
3. Copy only the intended, sanitized files into the temporary clone.
4. In the temporary clone, show `git status --short` and `git diff --name-status` before committing.
5. Commit there with the repo's existing author identity if needed.
6. Push from the temporary clone after `gh` HTTPS authentication is working.
7. Verify the remote branch moved with:

```bash
git ls-remote https://github.com/<owner>/<repo>.git refs/heads/<branch>
```

8. Check the commit through GitHub or fetch it locally.

After a temporary-clone push, the main project folder can still show the same files as uncommitted because its local metadata did not create the pushed commit. Reconcile the main workspace carefully after confirming GitHub has the expected commit.

## Connector Fallback Publishing

Use the GitHub connector when local push cannot authenticate but the connector has access.

1. Confirm the remote repository and current remote branch head.
2. Show the mandatory upload preview for the files that will be represented in the connector tree.
3. Build the intended GitHub tree from the local tracked content only.
4. Exclude ignored local content such as `.env`, `.codex/`, `skills/.system/`, `local/`, `.DS_Store`, SQLite files, and generated tenant-specific snapshots. Keep tracked installable project skills under `skills/` in the connector tree.
5. Before creating the commit, list connector-tree file paths that will be added, modified, deleted, or moved relative to the remote branch head.
6. Create blobs or tree entries through the connector.
7. Create a commit whose parent is the current remote branch head.
8. Update the branch ref without force unless the user explicitly approved force-push behavior.
9. Verify representative files on GitHub after the update.

For large file sets, create trees in chunks and carry the returned tree SHA into the next chunk. Report the final commit link.

## Local Metadata Reconciliation

After connector-based publishing, local Git may still show old remote metadata. If the local working tree is clean and the remote tree is the intended content, tell the user to run or run with permission:

```bash
git fetch origin main
git reset --hard origin/main
git status
```

Explain that this aligns local history with GitHub and does not remove project content when the working tree is clean and GitHub already has the intended files.

If the user wants to preserve local commit history, avoid hard reset and discuss the tradeoff before rebasing or merging.

## Content Location Checks

When the user says content is missing on GitHub:

1. Check whether the content was moved into a new folder structure.
2. Verify representative files directly on GitHub.
3. Provide direct GitHub links to the new locations.
4. Explain root-level folder changes plainly.

For the Orbital project pattern, existing query and script content may live under:

```text
queries_and_scripts/
```

## Credential Handling

- Do not ask the user to paste tokens into chat.
- Keep real credentials in ignored local files only.
- Commit `.env.example` templates when useful, not real `.env` files.
- If terminal push should work long term, recommend configuring either HTTPS with a GitHub token in the user's credential manager or an SSH key registered in GitHub.
- If Codex can use the GitHub connector, prefer it for publishing when the user wants to avoid local terminal credentials.

## Global Alignment

This workspace copy extends the global GitHub-sync baseline with Orbital public-repository boundaries and local-log rules. Keep the global release guardrails intact when updating either copy.

- Do not use a blind workspace-to-global `rsync --delete` for this skill when the global copy contains a newer `VERSION`, `scripts/version_skill.py`, or retained release history.
- Merge the current skill files deliberately, validate each variant, and create a local release snapshot for each changed copy.
- Keep `versions/` local-only. Publish the current `SKILL.md`, `VERSION`, agent metadata, and release script needed by a newly imported project.

## Outcome Guardrails, Version Review, And Retention

Apply `$skill-governance-guardrail` to every material update of this skill, its scripts, references, or assets. Before editing, inspect retained history and record the four release inputs below:

1. **Problem and success:** state the observed problem and a falsifiable success criterion.
2. **Trigger boundary:** give one request that should trigger the skill and one similar request that must not; review the frontmatter description against both.
3. **Dependencies and conflicts:** check related skills, referenced files, scripts, and tools for overlap, stale references, or contradictory instructions.
4. **Risk-based validation:** classify the change as `documentation`, `code`, or `sensitive`; run and record the relevant validation. For `sensitive`, also validate a failure or safe-rejection path.

```bash
python3 scripts/version_skill.py --history
```

After validation, increment `VERSION` and create the release snapshot. The command rejects missing outcome data, an unchanged release, or an unreviewed reintroduction from an older retained version.

```bash
python3 scripts/version_skill.py \
  --version "$(tr -d '\n' VERSION)" \
  --change-type maintenance \
  --change-summary "Describe the user-visible improvement." \
  --problem-statement "Describe the observed failure or gap." \
  --success-criteria "State the observable result that proves the improvement." \
  --positive-trigger "A request that should activate this skill." \
  --negative-trigger "A similar request that should use another approach." \
  --dependency-review "State checked skills, files, tools, and conflicts." \
  --risk-tier documentation \
  --review-notes "State the previous release and regression risks reviewed." \
  --validation "State the exact command or task and its result." \
  --keep 5
```

For `code`, run the changed script or a representative test. For `sensitive`, add `--failure-path-validation` with the rejected-input or safe-failure test. Keep at most five local snapshots in `versions/`. Publish only current files, including `VERSION` and `scripts/version_skill.py`, to GitHub; never publish `versions/` or runtime state.
