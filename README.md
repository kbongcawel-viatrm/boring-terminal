<div align="center">

![boring-terminal banner](assets/boring-banner.webp)

# `boring-terminal`

### A considered command line for a more capable shell.

**A Bash configuration for Fedora and Linux workflows, with terminal helpers, workspace and container tooling, and an optional SRE/DevOps toolbox.**

`SHELL CONFIG` &nbsp;·&nbsp; `FEDORA` &nbsp;·&nbsp; `PODMAN` &nbsp;·&nbsp; `SRE / DEVOPS`

</div>

<hr />

> **DESIGNED TO FEEL AT HOME IN YOUR TERMINAL**<br />
> Clear status signals. Connected workflows. Tools that stay close to the shell.

## `01` &nbsp; Overview

`boring-terminal` is a personal Bash configuration distributed as a single `bashrc_template`. It adds shell functions, aliases, environment defaults, validation helpers, and workflows for workspaces, Podman, Fedora Toolbox, and cloud/SRE development.

The visual language of this README takes inspiration from connected nodes and clean fintech interfaces: compact labels, clear sections, and purposeful signal. The artwork and identity are original to this documentation.

## `02` &nbsp; What’s inside

| Area | What it offers |
| --- | --- |
| **Shell foundation** | Global Bash definitions, user PATH setup, and support for loading `~/.bashrc.d/` snippets. |
| **Terminal feedback** | Consistent status messages, dividers, and a progress display for non-interactive commands. |
| **Configuration checks** | Helpers such as `getbash`, `getpath`, and `bashconfigcheck` for inspecting configuration. |
| **Workspace workflows** | Functions for workspace setup, synchronization, shortcuts, and connections. |
| **Containers** | Podman helpers, including `burnerbox` for a persistent development sandbox. |
| **SRE / DevOps tooling** | `sretoolbox` to create or reuse a Fedora Toolbox and provision a development toolchain. |
| **Shell conveniences** | Aliases and functions for common system, cloud, and development tasks. |

> **Heads up:** this is a personal, opinionated configuration—not a minimal or universally safe default. Read the template before installing it. In particular, its `rm` alias expands to `rm -rf`.

## `03` &nbsp; Requirements

- Bash
- Git, to clone this repository
- A backup of your existing `~/.bashrc`
- For optional Toolbox provisioning: Fedora Toolbox, Podman, and `curl`

Some functions call external utilities or assume a Fedora/Linux environment. Those tools are only needed for the corresponding workflows; inspect `bashrc_template` before using a function on another distribution.

## `04` &nbsp; Install

### Back up your current configuration

```bash
if [[ -e ~/.bashrc ]]; then
  cp -a ~/.bashrc ~/.bashrc.bak
fi
```

### Get the repository

Use the SSH clone URL if your GitHub SSH key is configured, or switch to HTTPS if preferred.

```bash
git clone git@github.com:kbongcawel-viatrm/boring-terminal.git
cd boring-terminal
```

### Review and validate

```bash
less ./bashrc_template
bash -n ./bashrc_template
```

No output from `bash -n` means Bash did not find a syntax error. It does **not** test commands that run when the file is sourced.

### Install and load

```bash
install -m 600 ./bashrc_template ~/.bashrc
source ~/.bashrc
```

`install` replaces `~/.bashrc` after the backup step. To undo the change, restore the backup with `cp -a ~/.bashrc.bak ~/.bashrc`, then start a new shell or run `source ~/.bashrc`.

## `05` &nbsp; Everyday entry points

### Run a shell function through `kimctl`

`kimctl` dispatches a function defined in the current shell and reports whether it succeeded. For example:

```bash
kimctl getpath
kimctl getbash
```

Use `kimctl` for functions that need the current shell—for example, to preserve interactive prompts, terminal access, or shell state. The included Bash completion suggests available functions.

### Create or enter the SRE Toolbox

```bash
sretoolbox --help
sretoolbox
sretoolbox sre-dev --enter
```

The function creates or reuses a Fedora Toolbox, provisions its toolchain, and enters it when requested. The default container name is `sre-devops-f44`; choose a name and image with `sretoolbox NAME --image IMAGE`. Provisioning can download and install third-party tools, so review the provisioning function in `bashrc_template` before running it. Lynis, AIDE, and ClamAV installed this way operate in the Toolbox—not as host security agents.

### Start the `burnerbox` development sandbox

```bash
burnerbox
```

`burnerbox` creates or starts a persistent Podman container and opens an interactive Bash session. It mounts `~/workspace/` at `/workspace`; review its container options and mount behavior in the template before use.

## `06` &nbsp; Configuration notes

- The template loads regular files from `~/.bashrc.d/` when that directory exists.
- It sets a restrictive `umask` and filters `PATH` entries so only absolute paths remain. Relative entries—including `.`—are removed.
- Terminal colors are suppressed when output is not a TTY or `NO_COLOR` is set; `KIMCTL_QUIET=1` suppresses supported terminal messages.
- Some commands and aliases are intentionally opinionated. Check the aliases near the end of the file before adopting them.
- Sourcing the template executes its top-level shell statements. Syntax validation alone does not guarantee side-effect-free sourcing.

## `07` &nbsp; Troubleshooting

**Check Bash syntax**

```bash
bash -n ~/.bashrc
```

**Inspect the active configuration**

```bash
getbash
getpath
```

**Restore the previous file**

```bash
cp -a ~/.bashrc.bak ~/.bashrc
source ~/.bashrc
```

If an optional workflow reports a missing command, install its prerequisite for your distribution or skip that workflow. Many helpers depend on external tools and are not required just to load the configuration.

## `08` &nbsp; Repository map

```text
boring-terminal/
├── README.md          # Overview, installation, and usage notes
├── bashrc_template    # Bash configuration and helper functions
└── LICENSE            # Project license
```

## `09` &nbsp; License

Distributed under the GNU General Public License, version 3.0. See [`LICENSE`](LICENSE) for the full terms.

<hr />

<div align="center">

`BORING TERMINAL` &nbsp;·&nbsp; **Less noise. More signal.**

</div>