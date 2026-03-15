# How To Use This Framework

## Prerequisites
- **Claude Code** installed: `curl -fsSL https://claude.ai/install.sh | bash`
- **Paid plan**: Claude Pro ($20/mo), Max ($100/mo), or API key with credits
- **Terminal**: Mac Terminal, Windows PowerShell, or Linux terminal

## Setup (2 minutes)

```bash
# Clone
git clone https://github.com/YOUR-USERNAME/lean-agentic-ai-best-practice.git
cd lean-agentic-ai-best-practice

# Start Claude Code
claude
```

Claude reads `CLAUDE.md` and discovers `.claude/` folder automatically.

## Run Built-in Skills

```bash
/cost-analyzer              # Full workflow: agent scans code → generates cost report
/bloat-detector             # Score your system across 7 bloat types (0-21)
/carbon-estimator           # Estimate CO₂ from your LLM usage
```

## Add Your Own Skill

```bash
# Option A: Use the scaffold script
./scripts/scaffold.sh skill my-skill-name
# Then edit .claude/skills/my-skill-name/SKILL.md

# Option B: Manual
cp -r .claude/skills/_template .claude/skills/my-skill-name
# Edit .claude/skills/my-skill-name/SKILL.md
```

## Add Your Own Agent

```bash
./scripts/scaffold.sh agent my-agent-name
# Edit .claude/agents/my-agent-name.md
```

## Add Your Own Command

```bash
./scripts/scaffold.sh command my-command-name
# Edit .claude/commands/my-command-name.md
```

## See Hidden Files

Files starting with `.` are hidden by default:
- **Mac Finder**: Press `Cmd + Shift + .`
- **Terminal**: `ls -la`
- **Windows Explorer**: View → Hidden items
- **VS Code**: Shows them by default

## Test Your Contribution

```bash
claude
> what commands, agents, and skills do you see in this project?
/your-skill-name
```

## File Map

```
.claude/commands/cost-analyzer.md        ← /cost-analyzer (entry point)
.claude/agents/lean-auditor.md           ← Scanning agent (haiku, read-only)
.claude/skills/_template/SKILL.md        ← COPY THIS for new skills
.claude/skills/token-counter/SKILL.md    ← Preloaded into agent
.claude/skills/model-recommender/SKILL.md← Preloaded into agent
.claude/skills/cost-analyzer/SKILL.md    ← Standalone (generates report)
.claude/skills/bloat-detector/SKILL.md   ← Standalone (7-type bloat audit)
.claude/skills/carbon-estimator/SKILL.md ← Standalone (CO₂ estimation)
.claude/rules/lean-principles.md         ← Rules Claude always follows
.claude/settings.json                    ← Permissions
CLAUDE.md                                ← Project memory
scripts/scaffold.sh                      ← One-command scaffolding
CONTRIBUTING.md                          ← Full contributor guide
```
