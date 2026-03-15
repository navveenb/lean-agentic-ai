---
description: One-line description shown in autocomplete when user types /
argument-hint: [optional-argument]
model: sonnet
# Commands typically need moderate reasoning for orchestration.
# Use haiku for simple commands, sonnet for orchestration, opus for complex planning.
allowed-tools: Read, Write, Agent, Skill
# Include Agent if this command invokes subagents.
# Include Skill if this command invokes standalone skills.
---

# Command Name

You are the orchestrator for [workflow description].

## Lean Principle

This command demonstrates Principle [N]: "[principle name]"

## Step 1: Gather Input

[Ask the user what you need, or use the argument provided via $0]

## Step 2: [Invoke Agent / Do Work]

Use the Agent tool to invoke the [agent-name] subagent:
- subagent_type: agent-name
- description: [what the agent should do]
- prompt: [specific instructions including user's input]
- model: haiku

Wait for the agent to complete and capture its results.

## Step 3: [Generate Output / Invoke Skill]

Use the Skill tool to invoke the [skill-name] skill:
- skill: skill-name
- [The skill will use the findings from Step 2]

## Step 4: Present Results

Summarize the key findings to the user.

## Critical Requirements

1. **Use Agent tool**: DO NOT use bash commands to invoke agents.
2. **Use Skill tool**: DO NOT use Agent tool for standalone skills.
3. **Keep it lean**: This workflow should demonstrate the principles it implements.
