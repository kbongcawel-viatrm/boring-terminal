#!/usr/bin/env python3
"""Scan staged additions for common secrets and personal-data patterns."""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Pattern:
    category: str
    expression: re.Pattern[str]


PATTERNS = (
    Pattern("private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    Pattern("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    Pattern("GitHub access token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    Pattern("GitLab access token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    Pattern("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    Pattern("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    Pattern(
        "credential assignment",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|"
            r"password|passwd|secret|private[_-]?key)\b\s*[:=]\s*['\"]?"
            r"(?!['\"]?(?:$|none\b|null\b|changeme\b|example\b|replace\b|"
            r"your[_-]|<|\$\{|\*))[^\s'\";,]{8,}"
        ),
    ),
    Pattern("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    Pattern("US Social Security number", re.compile(r"\b(?!000|666|9\d\d)\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b")),
    Pattern("possible US phone number", re.compile(r"(?<!\d)(?:\+?1[ .-]?)?\(?[2-9]\d{2}\)?[ .-][2-9]\d{2}[ .-]\d{4}(?!\d)")),
)

SENSITIVE_PATH = re.compile(
    r"(?:^|/)(?:\.env(?:\..*)?|id_(?:rsa|ed25519|ecdsa)|"
    r".*\.(?:pem|p12|pfx|key)|credentials\.json|serviceaccount(?:key)?\.json)$",
    re.I,
)


def staged_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "--cached", "--no-ext-diff", "--no-color", "--unified=0", "--no-renames"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def scan(diff: str) -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    path = "(unknown)"
    line_number = 0
    new_line = 0

    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
            if SENSITIVE_PATH.search(path):
                findings.append((path, 0, "sensitive filename"))
        elif line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,\d+)?", line)
            new_line = int(match.group(1)) if match else 0
        elif line.startswith("+") and not line.startswith("+++"):
            line_number = new_line
            for pattern in PATTERNS:
                if pattern.expression.search(line[1:]):
                    findings.append((path, line_number, pattern.category))
            new_line += 1
        elif line.startswith(" "):
            new_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            continue

    return findings


def self_test() -> int:
    fixtures = (
        ("safe placeholder", 'TOKEN="${env:ACCESS_TOKEN}"', False),
        (
            "generic secret assignment",
            'api_key="' + "not-a-real-but-long-secret-value" + '"',
            True,
        ),
        ("email address", "contact person" + "@" + "example.com", True),
        ("private key marker", "-----BEGIN " + "PRIVATE KEY-----", True),
        ("safe documentation", "Use a secret manager; never commit credentials.", False),
    )
    failures = 0
    for name, content, expected in fixtures:
        diff = f"--- a/example.txt\n+++ b/example.txt\n@@ -0,0 +1 @@\n+{content}\n"
        detected = bool(scan(diff))
        if detected != expected:
            print(f"FAIL: {name}", file=sys.stderr)
            failures += 1
    if failures:
        return 1
    print(f"Sensitive scanner self-test passed ({len(fixtures)} cases).")
    return 0


def main() -> int:
    if sys.argv[1:] == ["--self-test"]:
        return self_test()
    if sys.argv[1:]:
        print("Usage: pre-commit-sensitive-scan.py [--self-test]", file=sys.stderr)
        return 2

    try:
        findings = scan(staged_diff())
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Sensitive-data check could not run: {error}", file=sys.stderr)
        return 2

    if findings:
        print("Commit blocked: possible sensitive or personal data in staged changes:", file=sys.stderr)
        for path, line_number, category in findings:
            location = f"{path}:{line_number}" if line_number else path
            print(f"  {location}: {category}", file=sys.stderr)
        print("Remove/redact the data, or use an approved secret store. Do not bypass this check for real secrets.", file=sys.stderr)
        return 1

    print("Sensitive-data check passed: no configured patterns found in staged additions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())