# Why Lean? The Cost, Carbon, and Complexity Lens

Agentic AI was supposed to be smarter than monolithic AI calls. Instead, many implementations are more wasteful: uncoordinated agents triggering redundant API calls, oversized memory states, heavyweight models for lightweight tasks.

## What "Lean" Means

Borrowed from lean manufacturing: eliminate waste, maximize value, continuously improve.

**Waste in agentic systems:**
- Tokens processed that don't improve output
- Agent calls that don't contribute to the goal
- Tool invocations returning unused results
- Memory stored that's never retrieved
- Models larger than necessary for the task
- Reflection cycles that don't change the output
- Carbon emitted for computation that could have been cached

## The Three Lenses

Every design decision should pass all three:

**Cost**: How many tokens? How many LLM calls? What's the dollar cost per request? Could a cheaper model work?

**Carbon**: How much energy? What's the grid carbon intensity? Could this be cached or time-shifted?

**Complexity**: How many agents? How many tools? How deep is the reasoning chain? How much memory?

## The Core Rule

> If removing a component from your agentic system would not measurably degrade the output, that component is waste. Remove it.

This applies to agents, tools, memory, reflection cycles, context documents, and even prompt sentences.
