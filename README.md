# CSE 398/498 Project, 2026 Fall

This repository is for the class project of CSE 398/498 Vibe Research for Scientific Discovery, 2026 Fall.

## 1. Course Goal and Background

The goal of this project is that we each end up with our own **local coding agent harness**, customized for our own research and our own needs. It runs on our own machine, and we can add whatever tools and customizations fit the way we work.

We use **Codex** as our harness. What we learn should carry over, so we can later move to DeepSeek Harness or OpenCode.

## 2. Build Codex from Source

Repository: https://github.com/openai/codex

This is the main setup path for the course. We fork the upstream repository, build it ourselves, and use that fork as the place where all of our semester work lives.

If something below does not work, a good first move is to ask a coding agent how to fix it.

### 2.1 Fork the repository

Open https://github.com/openai/codex and click **Fork**. Create the fork under your own GitHub account. Keep the default name `codex`.

### 2.2 Add collaborators to your fork

Go to **Settings**, then **Collaborators**, then **Add people**, and add both of us so we can follow your progress:

* Instructor: `lichao-sun` (https://github.com/lichao-sun)
* TA: `soz223` (https://github.com/soz223)

### 2.3 Clone your fork

```bash
git clone https://github.com/<your-github-username>/codex.git
cd codex
git remote add upstream https://github.com/openai/codex.git
```

The `upstream` remote lets you pull in later changes from OpenAI without losing your own work.

### 2.4 Platform setup

**Linux and macOS.** Nothing extra is needed. Continue to 2.5.

**Windows.** The official system requirements list Windows only through WSL2, and the build instructions assume a Unix shell. So install WSL2 and do all of your work inside the Linux environment. Open PowerShell as administrator:

```powershell
wsl --install
```

Official guide: https://learn.microsoft.com/en-us/windows/wsl/install (you can let your coding agent walk you through it, or just ask any AI how to install WSL)

Reboot, open your new Ubuntu shell, and from that point follow the Linux instructions exactly. Keep the repository in your Linux home directory such as `~/code/`, never under `/mnt/c/`, or file I/O will be very slow. WSL1 is not supported.

### 2.5 Install the Rust toolchain

```bash
cd codex-rs
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
rustup component add rustfmt clippy
cargo install --locked just dotslash cargo-nextest
```

The toolchain version is pinned by `rust-toolchain.toml`, so rustup will fetch the correct one automatically.

### 2.6 Build

```bash
cargo build
cargo run --bin codex -- "explain this codebase to me"
```

Budget for this. A cold build compiles over a thousand crates, takes roughly 15 minutes on a 2 vCPU machine, and leaves about 15 GB in `target/`. Have 25 to 30 GB of free disk before you start. If you run out of space, `cargo clean` inside `codex-rs` clears it.

For a fast binary you can put on your PATH:

```bash
cargo build --release --bin codex
cp target/release/codex ~/.local/bin/codex-dev
```

Useful during development:

```bash
just fmt
just clippy
just test -p codex-tui
```

### 2.7 Sign in

Run the binary once and authenticate:

```bash
codex-dev
```

Inside the interface, or from the shell, run:

```bash
codex login
```

This opens a browser and signs you in with your ChatGPT account. Credentials are written in plain text to `~/.codex/auth.json`. **Never commit that file.** If you prefer an API key instead, use `codex login --api-key`.

Students at US and Canadian institutions can claim $100 of Codex credits at https://developers.openai.com/community/students

Verify with:

```bash
codex --version
codex login status
```

### 2.8 Commit your work all semester

All of the changes we make to the harness during this course live in your fork. Please commit and push regularly, roughly once a week and after each meaningful change. The commit history is how we follow progress across the semester, so a steady stream of small commits is much more useful to us than one large commit at the end of the term.

```bash
git add .
git commit -m "short description of what you changed"
git push origin main
```

Work on a branch when you are trying something risky, then merge it back into `main` once it builds.

## 3. What to Look At Next

Once Codex runs, these are the pieces we will actually customize. Each one is a topic we cover later in the semester, so there is no need to understand them yet. Knowing where they live is enough for now, and browsing them early makes those weeks easier.

| What it is                                                                           | Where it lives                                                      |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| Global configuration, such as model, provider, and approval policy                   | `~/.codex/config.toml`                                            |
| Credentials, written in plain text, never commit them                                | `~/.codex/auth.json`                                              |
| Project instructions loaded at the start of every session                            | `AGENTS.md` in your repository root                               |
| Skills, reusable procedures the agent can call on its own                            | `.agents/skills/` in a project, or `~/.agents/skills/` globally |
| MCP servers, external tools you plug into the agent                                  | `[mcp_servers]` in `config.toml`, or `codex mcp add`          |
| Hooks, your own code that fires around agent events                                  | `~/.codex/hooks.json` or `<repo>/.codex/hooks.json`             |
| Subagents, separate agents the main one can delegate to                              | `~/.codex/agents/<name>.toml`                                     |
| Session transcripts, a full log of every turn, useful for debugging your own changes | `~/.codex/sessions/YYYY/MM/DD/*.jsonl`                            |

Commands you can type inside the interface:

| Command           | What it does                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `/init`         | Scans the repository and writes a first draft of`AGENTS.md` for you                                                                 |
| `/status`       | Shows the current session state: model, working directory, token usage, and account                                                   |
| `/skills`       | Lists the skills currently visible to the agent                                                                                       |
| `/mcp`          | Lists connected MCP servers and the tools each one exposes                                                                            |
| `/debug-config` | Prints the configuration as it was actually resolved, and where each value came from. Use this whenever a setting seems to be ignored |
| `/compact`      | Summarizes the conversation so far to free up context in a long session                                                               |

## 4. Optional

### 4.1 Install Codex as a prebuilt package

If you want a stable copy alongside your development build, install the released binary. This does not replace anything in Section 2 and is not a substitute for it.

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

On macOS you can also use `brew install --cask codex`. On Windows there is a native prebuilt installer:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Keep the two installs separate by giving your own build a different name (`codex-dev`) and a different home:

```bash
CODEX_HOME=~/.codex-dev codex-dev
```

The directory in `CODEX_HOME` must already exist or the variable is ignored.

### 4.2 Install Dr. Claw

Dr. Claw is an open source research workbench built at Lehigh. It organizes a project across survey, ideation, experiment, publication, and promotion, and it drives CLI agents such as Codex as subprocesses. We will refer to it later in the course. Nothing in Section 2 depends on it.

Requires Node v20 or higher, v22 LTS recommended.

```bash
node --version
npx dr-claw
```

For a permanent install:

```bash
npm install -g dr-claw
dr-claw
```

If npm fails on `node-pty` or `better-sqlite3`:

```bash
sudo apt-get install -y build-essential python3
```

Install Codex first, otherwise Dr. Claw has no Codex backend to drive.

Repository: https://github.com/OpenLAIR/dr-claw
Documentation: https://openlair.github.io/dr-claw/

### 4.3 Add a project instructions file

`AGENTS.md` at the root of your repository is loaded automatically at the start of every session, so you write your conventions once instead of repeating them in every prompt. Create an empty one with `touch AGENTS.md`.

Keep it short. It is sent with every request, so a long file costs you context on every turn. For what belongs in it, see the official Codex documentation, or simply ask Codex what is worth putting there for your project.

## 5. Common Problems

| Symptom                          | Fix                                                                                                                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Disk full during the build       | `cargo clean` inside `codex-rs`                                                                                                                                         |
| Everything slow under WSL        | Repository is on`/mnt/c/`, move it to `~/code/`                                                                                                                         |
| Sandbox fails to start on Ubuntu | Load the AppArmor profile`bwrap-userns-restrict`                                                                                                                          |
| `CODEX_HOME` ignored           | The directory must exist first                                                                                                                                              |
| Provider change has no effect    | `model_provider` is ignored in project level config, put it in `~/.codex/config.toml` and check with `/debug-config`                                                  |
| Online tutorial fails            | `wire_api = "chat"` was removed, use `"responses"`. `--full-auto` is deprecated, use `--sandbox workspace-write`. `~/.codex/prompts/` no longer loads, use skills |
| Some skills ignored              | The initial skill list is capped at 8000 characters                                                                                                                         |
| TLS errors behind a proxy        | `export CODEX_CA_CERTIFICATE=/path/to/ca-bundle.pem`                                                                                                                      |

If you are stuck, ask the agent itself for help first, then contact the TA.
