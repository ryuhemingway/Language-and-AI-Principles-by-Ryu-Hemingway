# Agentic coding and AI agents Course Coverage

Total lessons: 11

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What Makes a Workflow Agentic

Objective: Understand the difference between a single model call and an agentic loop.

Concepts taught:
- Agentic workflows let the system plan, use tools, inspect results, and decide next steps.
- They are useful when tasks need state, branching, iteration, or external actions.
- More autonomy increases the need for boundaries, logging, and evaluation.

Practice: Draw a loop: goal -> plan -> tool call -> observation -> decide -> final answer.

Quick check: What can an agentic workflow use besides the model?

## Lesson 2: Tools, State, and Memory

Objective: Learn the building blocks that make agents useful and controllable.

Concepts taught:
- Tools expose narrow actions such as search, file read, code run, database query, or API call.
- State records what has happened so the workflow can continue coherently.
- Memory should be explicit and scoped; unbounded memory creates noise and privacy risk.

Practice: Define three tools for a research agent: search, open source, and summarize evidence.

Quick check: What records what has happened in a workflow?

## Lesson 3: Planning and Control Flow

Objective: Understand linear chains, routers, loops, and supervisor patterns.

Concepts taught:
- Chains run fixed steps; routers choose a path; loops repeat until a condition is met.
- Supervisor patterns coordinate specialized workers but are harder to debug.
- Use the simplest control flow that can solve the task reliably.

Practice: Design a support workflow: classify issue -> retrieve docs -> draft answer -> verify citations.

Quick check: Which pattern chooses between multiple paths?

## Lesson 4: Guardrails and Observability

Objective: Learn how to make agentic systems safer and easier to debug.

Concepts taught:
- Guardrails constrain tools, budgets, permissions, and output formats.
- Observability means logging prompts, tool calls, observations, costs, and failures.
- Human approval is useful for destructive actions or high-stakes decisions.

Practice: Add a rule that file writes require approval and every tool call is logged with inputs/outputs.

Quick check: What should destructive actions often require?

## Lesson 5: Building a Small Agent

Objective: Learn a practical first agent architecture.

Concepts taught:
- Start with one goal, two or three tools, a max-steps limit, and clear success criteria.
- Keep tool schemas explicit so the model knows exactly what each tool can do.
- Evaluate the whole workflow with a harness, not just the final answer.

Practice: Build a CLI research agent with search/open/summarize tools and a five-step limit.

Quick check: What limit prevents an agent from looping forever?

## Lesson 6: What makes AI agentic

Objective: Understand the difference between a chatbot, a pipeline, and an agent.

Concepts taught:
- An agent reasons, plans, acts, and observes outcomes in a loop.
- ReAct interleaves reasoning and acting so the model can inspect results.
- Agents are useful when task steps are open-ended, tool-heavy, or need adaptation.
- A simple prompt is still better when the workflow is small and predictable.

Example:
```text
while not done:
    thought = plan(state)
    action = choose_tool(thought)
```

Practice: Decide whether a task should be a prompt, pipeline, or agent.

Quick check: What pattern interleaves reasoning and acting?

## Lesson 7: Tools and function calling

Objective: Use schemas so the model can invoke tools reliably.

Concepts taught:
- Tool definitions should include a name, a description, and a JSON schema for parameters.
- Function calling turns tool use into structured requests instead of free-form text guesses.
- Sequential and parallel tool calls each fit different workflows.
- Tool errors need retries, fallbacks, and clear failure handling.

Example:
```text
tool = {"name": "search", "parameters": {"query": "..."}}
result = call_tool(tool)
```

Practice: Design one tool schema for search and one for a database lookup.

Quick check: What makes tool invocation reliable?

## Lesson 8: MCP architecture and servers

Objective: Connect AI systems to tools through the modern universal protocol.

Concepts taught:
- MCP separates host, client, and server responsibilities over JSON-RPC 2.0.
- Tools, resources, prompts, and sampling are core MCP primitives.
- STDIO and Streamable HTTP cover local and remote transports.
- Building both a server and a client is part of practical AI engineering now.

Example:
```text
host -> client -> server
tools = discover_tools(server)
call(tool_name, args)
```

Practice: Explain how MCP differs from ad hoc tool wiring in one sentence.

Quick check: What does MCP standardize?

## Lesson 9: LangChain and LangGraph

Objective: Use graph-based orchestration when an agent needs state and control flow.

Concepts taught:
- LangChain covers prompts, chains, wrappers, and parsers.
- LangGraph adds nodes, edges, conditional routing, and durable state.
- Checkpointers, threads, and interrupt nodes make human-in-the-loop workflows possible.
- Subgraphs help you keep large workflows modular and debuggable.
- OpenAI Agents SDK, CrewAI, AutoGen, and smolagents are alternatives with different tradeoffs.

Example:
```text
graph.add_node("plan", plan)
graph.add_edge("plan", "tool")
graph.add_conditional_edge("tool", router)
```

Practice: Sketch one workflow that would be easier in LangGraph than in a single linear chain.

Quick check: What LangGraph concept represents stateful routing?

## Lesson 10: Memory and multi-agent systems

Objective: Manage short-term and long-term memory, then coordinate several specialist agents.

Concepts taught:
- Short-term memory holds the live conversation buffer and recent state.
- Long-term memory uses a vector store or database to recall past work.
- Multi-agent systems split work into roles such as planner, researcher, critic, and executor.
- Supervisor agents and handoffs keep specialization from turning into chaos.

Example:
```text
short_term.append(message)
long_term = retrieve(query)
next_agent = supervisor.route(task)
```

Practice: Describe one memory strategy and one role split for a research workflow.

Quick check: Which memory store usually holds past interactions?

## Lesson 11: Agentic design patterns and production

Objective: Ship agents that are observable, secure, and useful in real workflows.

Concepts taught:
- Reflection, planning, routing, and tool augmentation are core agentic design patterns.
- Research agent, code agent, data analysis agent, RAG agent, browser agent, and workflow agent patterns are common applications.
- Observability tools such as LangSmith or LangFuse help debug loops and tool choices.
- Production agents need prompt-injection defense, permission scoping, retries, idempotency, and cost control.

Example:
```text
planner -> researcher -> critic -> executor
trace = langsmith.run(agent)
enforce_permissions(tools)
```

Practice: Pick one end-to-end agent project and list the tools, failure modes, and monitoring you would need.

Quick check: What is one production safeguard for an agent?
