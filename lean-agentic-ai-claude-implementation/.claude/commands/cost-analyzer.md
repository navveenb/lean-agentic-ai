---
description: Analyze LLM API usage in a codebase and recommend model right-sizing to reduce cost, carbon, and complexity
argument-hint: [file-or-directory-path]
model: sonnet
allowed-tools: Read, Grep, Glob, Write, Agent, Skill
---

# Cost Analyzer — Lean Agentic AI

You are the orchestrator for a lean cost analysis workflow based on Principle 2: "Not every prompt deserves a 70B response."

## Your Job

Analyze a codebase (or the current project) for LLM API usage patterns and produce a report recommending where smaller, cheaper models could be used without quality loss.

## Step 1: Ask the User

Use the AskUser tool to ask:
- What path should I analyze? (default: current project root)
- What LLM provider are they using? (OpenAI, Anthropic, Google, or Mixed)

## Step 2: Invoke the lean-auditor Agent

Use the Agent tool to invoke the `lean-auditor` subagent:
- subagent_type: lean-auditor
- description: Scan codebase for LLM API calls and classify each by task type
- prompt: Scan the path `$0` (or project root if not specified). Find all LLM API calls. For each call, identify: the model being used, the task being performed (classify, summarize, generate, reason, etc.), the approximate input/output token sizes, and whether the call could use a smaller model. The agent has preloaded skills (token-counter and model-recommender) that provide detailed instructions.
- model: haiku

Wait for the agent to complete and capture its findings.

## Step 3: Generate Cost Report

Use the Skill tool to invoke the `cost-analyzer` skill:
- skill: cost-analyzer
- The skill will use the findings from Step 2 (available in context) to generate a detailed cost report with savings estimates.
- The report should be written to `reports/cost-analysis.md`

## Step 4: Present Results

Summarize the key findings to the user:
- Total LLM calls found
- Calls that could be downgraded to a smaller model
- Estimated monthly cost savings
- Estimated carbon reduction

## Critical Requirements

1. **Use Agent tool for lean-auditor**: DO NOT use bash commands to invoke the agent.
2. **Use Skill tool for cost-analyzer**: Invoke the report generator via the Skill tool.
3. **Use haiku for the scanning agent**: The scanning task is simple pattern matching — it doesn't need a frontier model. This is Principle 2 in action.
4. **Keep it lean**: Do not add extra agents or reflection cycles. This workflow should demonstrate the principles it's analyzing.
