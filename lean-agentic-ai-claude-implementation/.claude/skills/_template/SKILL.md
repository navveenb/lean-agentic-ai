---
name: your-skill-name
description: One-line description of what this skill does and when to invoke it
user-invocable: true
# Set to false if this skill should only be preloaded into agents (background knowledge)
# Set to true if users should be able to type /your-skill-name directly

# Optional fields:
# argument-hint: [file-path]
# allowed-tools: Read, Write, Grep, Glob
# model: haiku
# context: fork
---

# Skill Name

> One sentence: what does this skill do?

## Lean Principle

Which of the 10 principles does this skill implement?
- [ ] #1 Context is a liability
- [ ] #2 Right-size your model
- [ ] #3 Orchestration is not a playground
- [ ] #4 Reflections cost compute
- [ ] #5 RAG isn't always right
- [ ] #6 Emissions are invisible
- [ ] #7 Reuse over recompute
- [ ] #8 More tools, more problems
- [ ] #9 Memory is a judgment call
- [ ] #10 Governance over autonomy

## Instructions

[Write clear instructions for Claude to follow when this skill is active.
Be specific. Use step-by-step format.
If this is a preloaded skill (background knowledge), write the rules/data the agent should internalize.]

## Input

What information does this skill expect to receive?
- From the user: [what the user provides]
- From context: [what should already be in the conversation]

## Output

What does this skill produce?
- [Description of output]
- [Where it gets saved, if applicable]

## Example

[Show a concrete example of input → output so contributors understand the intended behavior]
