# Agent guidance

This repository is `boring-terminal`, a personal Bash configuration for
Fedora/Linux. Read `README.md` before changing shell behavior and inspect the
relevant section of `bashrc_template` before proposing commands or edits.

## Shared agent context

- The two repository skills are [Planning](.agents/skills/planning/SKILL.md)
  (read-only discovery and plan) and [Acting](.agents/skills/acting/SKILL.md)
  (authorized implementation and validation). Use the phase-appropriate skill;
  both incorporate the repository's Harness² and shell-safety guidance.
- For additional Harness² context and repository setup rationale, read
  [`docs/improved-google-harness.md`](docs/improved-google-harness.md).
- Before configuring MCP integrations, read [`docs/mcp-setup.md`](docs/mcp-setup.md)
  and treat [`.cline/mcp.json`](.cline/mcp.json) as a credential-free Cline
  project template, not proof that servers are connected or authenticated.
- The repository pre-commit hook scans staged additions for common secrets and
  personal-data patterns; see [`docs/commit-safety.md`](docs/commit-safety.md).
- `AGENTS.md` and `docs/` contain shareable project guidance. Keep private
  session transcripts, user data, and credentials out of version control.
- Use an AI tool's own memory/session features only as that tool documents
  them; do not assume they sync across tools. Promote reviewed, durable,
  non-sensitive project facts into this repository's docs when appropriate.
- MCP, plugins, hooks, and scripts may perform external actions or execute
  code. Keep credentials out of the repository, review permissions and side
  effects, and get explicit confirmation before consequential writes or
  destructive operations.

## Shell safety

- Do not source `bashrc_template` as a validation step; its top-level
  statements execute. Use `bash -n ./bashrc_template` for syntax checking.
- Do not install the template into `~/.bashrc`, edit user shell startup files,
  change container/image trust, provision tools, or start/alter containers
  unless that specific operation is requested and its effects are clear.
- Preserve unrelated working-tree changes. Inspect `git status` and diffs
  before editing or reporting completion.
- Validate changes with safe, targeted checks and clearly state what was not
  exercised.

## Documentation and changes

- Keep this file concise; put detailed setup and rationale in `docs/` or a
  focused skill.
- Prefer minimal, reviewable changes. Verify commands against the checked-in
  README and implementation.
- Do not claim a plugin, MCP server, skill, session, or memory integration is
  active unless the corresponding client configuration and authentication have
  actually been verified.