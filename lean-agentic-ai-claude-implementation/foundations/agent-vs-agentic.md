# Agent vs. Agentic: Understanding the Difference

**An Agent** is a defined software component — a building block with a name, role, tools, and prompt. You create agents, configure them, deploy them.

**Agentic** describes a behavior — the ability to reason, plan, and act autonomously toward a goal. A system can be agentic without having explicitly defined "agents." A single LLM call with a reasoning loop and tool access is agentic behavior.

## Why This Matters for Lean Design

| | Cost Impact | Fix |
|---|---|---|
| Agent proliferation (many defined agents) | Orchestration overhead, inter-agent communication | Principle 3: Consolidate agents |
| Agentic behavior (reasoning loops) | Compute costs from iterative inference | Principle 4: Bound reflections |

**The lean question**: Do I need a *new agent*, or do I need *agentic behavior* in an existing component? Often, a single well-prompted agent with agentic behavior replaces three separate agents with rigid scripts.

## Autonomy Levels

| Level | Description | Cost | Risk |
|-------|-------------|------|------|
| L0: Scripted | Fixed steps, no reasoning | Low, predictable | Low |
| L1: Guided | Follows plan, chooses parameters | Moderate | Low-Medium |
| L2: Adaptive | Adjusts plan based on observations | Higher, variable | Medium |
| L3: Autonomous | Sets own goals, self-corrects | Highest, unpredictable | High |

Lean design matches autonomy level to task requirements — never higher than necessary.
