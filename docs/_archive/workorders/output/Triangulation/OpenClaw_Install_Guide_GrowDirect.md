---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# OpenClaw Install Guide — GrowDirect Local Setup
*For Jeffe — standalone reference, no ALX project context needed*

**Date:** February 25, 2026
**Target machine:** Mac (Apple Silicon — Mac Mini, MacBook Pro, etc.)
**What this is:** OpenClaw is an open-source AI agent gateway that runs locally on your hardware. It connects to LLMs (Claude, GPT, etc.) via API and lets you interact through messaging apps, a browser dashboard, or CLI. It's MIT-licensed, local-first (your data stays on your machine), and supports multi-agent routing.
**Why we care:** Future candidate for GrowDirect's agent infrastructure layer — containerized alongside Canary and Bolt.diy in a unified deployment package. For now, this is just getting it running so you can poke at it.

---

## Prerequisites

You need three things installed before OpenClaw:

### 1. Xcode Command Line Tools
```bash
xcode-select --install
```
Follow the prompts. If already installed, it'll tell you.

### 2. Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 3. Node.js 22+
OpenClaw requires Node 22 or newer. Check what you have:
```bash
node --version
```
If it's below 22 (or not installed):
```bash
brew install node@22
```
Verify:
```bash
node --version  # Should show v22.x.x or higher
```

---

## Install OpenClaw

### Option A: One-liner installer (easiest)
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```
This handles everything and drops you into the onboarding wizard.

### Option B: npm global install (more control)
```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

### Option C: pnpm (if you prefer pnpm)
```bash
pnpm add -g openclaw@latest
pnpm approve-builds -g    # approve openclaw, node-llama-cpp, sharp, etc.
openclaw onboard --install-daemon
```

### If you hit the `sharp` / `libvips` error (common on macOS with Homebrew):
```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

### If `openclaw` command not found after install:
Your npm global bin directory probably isn't in PATH. Fix:
```bash
# Find where npm puts global binaries
npm prefix -g
# Add that path + /bin to your shell config
echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Onboarding Wizard

After install, the wizard runs automatically (or run `openclaw onboard` manually). It walks you through:

1. **AI Provider** — Choose **Anthropic**. You'll need your API key from console.anthropic.com.
   - Recommended model: **Claude Opus 4.6** for primary orchestration (best long-context + prompt injection resistance)
   - Cheaper models (Sonnet, Haiku) can handle heartbeats and sub-agent tasks
2. **Gateway settings** — Defaults are fine for local use. Gateway runs on `ws://127.0.0.1:18789`
3. **Channel setup** — Pick one to start. Options:
   - **WebChat / Control UI** (easiest — browser-based, no external account needed)
   - **Slack** (if we stand up B-013 workspace)
   - **Discord** (needs a bot via Discord Developer Portal)
   - **Telegram** (needs a bot via @BotFather)
   - **WhatsApp** (needs QR scan — use a DEDICATED number, not personal)
4. **Skills** — You can skip for now or pick from the bundled list. Skills can be added anytime later.
5. **Daemon install** — Say yes. This registers OpenClaw as a launchd service so it survives reboots.

---

## Verify It's Running

### Open the Control UI (browser dashboard):
```bash
openclaw ui
```
This copies the dashboard URL and opens your browser. Default: `http://localhost:18789`

If it asks for auth, get the token:
```bash
openclaw gateway token
```

### Quick CLI test:
```bash
openclaw agent --message "Hello, are you running?"
```

### Check health:
```bash
openclaw doctor
```
This surfaces any misconfigurations or risky settings.

### View logs:
```bash
openclaw logs --follow
```

---

## Docker Install (for future containerized deployment)

This is the path Jeremy will use when we wire OpenClaw into the GrowDirect compose stack:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
docker compose up -d
```

Docker mounts two volumes:
- `~/.openclaw` — configuration and credentials
- `~/openclaw/workspace` — agent's sandbox (SOUL.md, skills, memory)

If you hit permission errors:
```bash
sudo chown -R $(whoami) ~/.openclaw ~/openclaw
```

---

## Key Concepts to Know

| Concept | What It Is |
|---|---|
| **Gateway** | The always-on daemon that routes messages between channels, LLMs, and tools |
| **Workspace** | Directory where agent personality (SOUL.md), memory, and skills live. Default: `~/.openclaw/workspace` |
| **SOUL.md** | The agent's personality/instructions file — like our agent profiles |
| **Skills** | Portable capability packages. Community-shared or custom-built. Live in `workspace/skills/` |
| **Channels** | Messaging platforms (Slack, Discord, WhatsApp, Telegram, WebChat, etc.) |
| **Multi-agent routing** | Multiple isolated agents, each with own workspace + sessions. Route by channel/sender. |
| **Control UI** | Browser-based admin dashboard. Chat, config, execution approvals. **Never expose publicly.** |
| **Heartbeat** | Scheduled wake-up — agent can run proactively on a timer without being prompted |

---

## Security Notes (Important)

- **This is experimental software.** The security surface is large — shell access, browser control, file system access.
- **Bind to localhost only** — In `openclaw.json`, make sure gateway is `127.0.0.1`, not `0.0.0.0`
- **Enable exec_approval** — Require manual approval for shell commands, file deletions, git pushes
- **Run `openclaw doctor`** regularly — it flags risky DM policies and misconfigurations
- **Don't connect personal WhatsApp** — Use a dedicated number if you set up WhatsApp
- **Don't install on a machine with sensitive data** until you understand the permission model
- **Syd needs to review** before this touches anything near merchant data or Canary_IP

---

## What's Next (Parked — Post Demo Week)

These are logged in ALX's queue for Sprint 6+:

1. **ADR-OC-001** — Architecture decision: OpenClaw as GrowDirect agent infrastructure layer
2. **Jeremy work order** — Containerize alongside Canary stack, validate no port conflicts
3. **Condor work order** — First SOUL.md + skills scaffold for a Canary-aware agent
4. **Tom review** — Where does OpenClaw sit in the service graph? Security boundaries?
5. **Syd review** — Prompt injection surface, data exposure risk, compliance posture
6. **Unified deploy target** — `growdirect_deploy.sh --full` spins up Canary + Bolt.diy + OpenClaw together

---

## Useful Links

- **GitHub:** https://github.com/openclaw/openclaw
- **Docs:** https://docs.openclaw.ai
- **npm:** https://www.npmjs.com/package/openclaw
- **Getting Started:** https://docs.openclaw.ai/start/getting-started
- **Multi-Agent Routing:** https://docs.openclaw.ai/concepts/multi-agent

---

*Written by ALX. For use outside the ALX project context — hand this to any Claude session and say "help me install OpenClaw on my Mac."*
