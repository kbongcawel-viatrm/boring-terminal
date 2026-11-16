# Commit safety gate

This repository provides a local Git `pre-commit` hook in `.githooks/pre-commit`.
It scans **staged additions** before each commit for common credential patterns,
private-key markers, sensitive filenames, email addresses, US Social Security
numbers, and common US phone-number formats. Findings report only a file, line,
and category—not the matched content. The hook uses Python 3's standard library
and Git; no network access or external scanner is required.

## Enable it in a checkout

The current checkout is configured with:

```bash
git config --local core.hooksPath .githooks
```

For a fresh clone, run that command from the repository root to enable its local
hook. `core.hooksPath` is local Git configuration and is not transferred by
clone. Confirm with:

```bash
git config --local --get core.hooksPath
```

The committed hook file is executable and runs automatically for normal commits
once this setting is present. Git options such as `--no-verify` can bypass local
hooks, so this is a guardrail, not an enforceable server-side policy. Teams that
need a non-bypassable gate should repeat scanning in protected-branch CI or a
server-side receive hook.

## Run and test

Run the fixture-only test without staging or changing files:

```bash
python3 scripts/pre-commit-sensitive-scan.py --self-test
```

To manually scan the current index, run:

```bash
python3 scripts/pre-commit-sensitive-scan.py
```

The scanner examines added lines in the staged diff; it does not inspect unstaged
or untracked files, prior Git history, binary file contents, or the commit
message. Review all files before staging. Do not put secrets or personal data in
Git and rely on detection. Patterns can miss novel/encoded secrets and can flag
legitimate example data; review findings carefully and replace sensitive
examples with unmistakable placeholders. If a real credential was staged or
committed, remove it and revoke/rotate it—the hook cannot undo disclosure.

The hook intentionally blocks likely personal identifiers such as email, phone,
and SSN values. It cannot reliably identify every kind of personal information
(for example, a person's name or address) without substantial false positives;
review staged changes for those manually.