---
name: your-agent-name
description: One-line description. Add PROACTIVELY if Claude should auto-invoke this agent.
tools: Read, Grep, Glob
# Only list the MINIMUM tools this agent needs. Fewer tools = less confusion = less cost.
# Common tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
model: haiku
# Use the smallest model that works for this agent's task (Principle 2):
#   haiku    → classification, scanning, extraction, formatting
#   sonnet   → summarization, moderate reasoning, code generation
#   opus     → complex reasoning, planning, creative tasks
color: green
# Visual color in terminal: green, magenta, cyan, yellow, blue, red
skills:
  - skill-name-1
  - skill-name-2
# Skills listed here are PRELOADED into the agent's context at startup.
# Their full SKILL.md content is injected as background knowledge.
# Only preload skills the agent actually needs — each one costs context tokens.

# Optional fields:
# maxTurns: 10
# permissionMode: acceptEdits
# disallowedTools: Bash(rm *), Bash(curl *)
# background: true
---

# Agent Name

You are [role description]. Your goal is [specific goal].

## What You Do

[Clear description of this agent's single responsibility]

## Steps

1. [First step — be explicit about which tool to use]
2. [Second step]
3. [Third step]

## Use Your Preloaded Skills

- **skill-name-1**: [How the agent should use this skill's knowledge]
- **skill-name-2**: [How the agent should use this skill's knowledge]

## Rules

- DO NOT use bash commands to invoke other agents. Use the Agent tool.
- DO NOT [other restrictions specific to this agent]
- [Keep it focused — agents should do ONE thing well]

## Output Format

[Specify exactly what the agent should return when it's done]
