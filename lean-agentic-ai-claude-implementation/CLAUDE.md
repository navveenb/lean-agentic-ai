# Lean Agentic AI — Best Practice Framework

## Project Overview
A plug-and-play framework for building lean agentic AI systems. Based on the 10 principles from [Lean Agentic AI](https://leanagenticai.com/) by Navveen Balani.

Contributors add skills, agents, and commands by copying templates and submitting PRs. See CONTRIBUTING.md.

## Built-in Workflow: Cost Analyzer
- `/cost-analyzer`: Entry point — scans codebases for wasteful LLM usage
- `lean-auditor` agent: Scans code using haiku (Principle 2), preloads token-counter + model-recommender skills
- `cost-analyzer` skill: Generates cost report to `reports/cost-analysis.md`
- `/bloat-detector`: Standalone skill — detects 7 bloat types, scores 0-21
- `/carbon-estimator`: Standalone skill — estimates CO₂ from LLM usage

## Skill Patterns
- **Agent skills** (preloaded via `skills:` field): token-counter, model-recommender
- **Standalone skills** (invoked via Skill tool or `/command`): cost-analyzer, bloat-detector, carbon-estimator
- **Template**: `.claude/skills/_template/SKILL.md` — copy for new skills

## Key Rules
- Use Agent tool (not bash) to invoke subagents
- Use Skill tool to invoke standalone skills
- Write outputs to `reports/` directory
- Always use the smallest model that works (Principle 2)
- See `.claude/rules/lean-principles.md` for full rules

## Adding New Skills
```bash
./scripts/scaffold.sh skill your-skill-name
```
