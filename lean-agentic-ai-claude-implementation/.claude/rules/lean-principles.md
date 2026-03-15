# Lean Agentic AI Rules

## Always

- Use the smallest model that achieves acceptable quality for any task.
- When creating new agents, default to `model: haiku` and upgrade only if quality is insufficient.
- When listing tools for agents, include only what's strictly needed.
- Write all reports and analysis outputs to the `reports/` directory.
- Reference specific principle numbers when making optimization recommendations.

## Never

- Never use bash commands to invoke subagents. Always use the Agent tool.
- Never give agents access to tools they don't need.
- Never create an agent when a skill would suffice.
- Never add reflection loops without explicit exit conditions.
- Never store full conversation transcripts — always summarize first.
