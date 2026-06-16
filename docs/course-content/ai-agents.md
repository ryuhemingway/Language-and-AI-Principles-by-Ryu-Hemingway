# Agentic coding and AI agents Course Coverage

Total lessons: 11

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What Makes a Workflow Agentic

Objective: Understand the difference between a single model call and an agentic loop.

Context:
What Makes a Workflow Agentic sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Agentic workflows let the system plan, use tools, inspect results, and decide next steps. They are useful when tasks need state, branching, iteration, or external actions.

More autonomy increases the need for boundaries, logging, and evaluation. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Agentic workflows let the system plan, use tools, inspect results, and decide next steps.
- They are useful when tasks need state, branching, iteration, or external actions.
- More autonomy increases the need for boundaries, logging, and evaluation.

Quick check: What can an agentic workflow use besides the model?

Concept check: In one sentence, explain how this idea matters in a real AI system: What Makes a Workflow Agentic.


## Lesson 2: Tools, State, and Memory

Objective: Learn the building blocks that make agents useful and controllable.

Context:
Tools, State, and Memory sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Tools expose narrow actions such as search, file read, code run, database query, or API call. State records what has happened so the workflow can continue coherently.

Memory should be explicit and scoped; unbounded memory creates noise and privacy risk. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Tools expose narrow actions such as search, file read, code run, database query, or API call.
- State records what has happened so the workflow can continue coherently.
- Memory should be explicit and scoped; unbounded memory creates noise and privacy risk.

Quick check: What records what has happened in a workflow?

Concept check: In one sentence, explain how this idea matters in a real AI system: Tools, State, and Memory.


## Lesson 3: Planning and Control Flow

Objective: Understand linear chains, routers, loops, and supervisor patterns.

Context:
Planning and Control Flow sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Chains run fixed steps; routers choose a path; loops repeat until a condition is met. Supervisor patterns coordinate specialized workers but are harder to debug.

Use the simplest control flow that can solve the task reliably. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Chains run fixed steps; routers choose a path; loops repeat until a condition is met.
- Supervisor patterns coordinate specialized workers but are harder to debug.
- Use the simplest control flow that can solve the task reliably.

Quick check: Which pattern chooses between multiple paths?

Concept check: In one sentence, explain how this idea matters in a real AI system: Planning and Control Flow.


## Lesson 4: Guardrails and Observability

Objective: Learn how to make agentic systems safer and easier to debug.

Context:
Guardrails and Observability sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Guardrails constrain tools, budgets, permissions, and output formats. Observability means logging prompts, tool calls, observations, costs, and failures.

Human approval is useful for destructive actions or high-stakes decisions. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Guardrails constrain tools, budgets, permissions, and output formats.
- Observability means logging prompts, tool calls, observations, costs, and failures.
- Human approval is useful for destructive actions or high-stakes decisions.

Quick check: What should destructive actions often require?

Concept check: In one sentence, explain how this idea matters in a real AI system: Guardrails and Observability.


## Lesson 5: Building a Small Agent

Objective: Learn a practical first agent architecture.

Context:
Building a Small Agent sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Start with one goal, two or three tools, a max-steps limit, and clear success criteria. Keep tool schemas explicit so the model knows exactly what each tool can do.

Evaluate the whole workflow with a harness, not just the final answer. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Start with one goal, two or three tools, a max-steps limit, and clear success criteria.
- Keep tool schemas explicit so the model knows exactly what each tool can do.
- Evaluate the whole workflow with a harness, not just the final answer.

Quick check: What limit prevents an agent from looping forever?

Concept check: In one sentence, explain how this idea matters in a real AI system: Building a Small Agent.


## Lesson 6: What makes AI agentic

Objective: Understand the difference between a chatbot, a pipeline, and an agent.

Context:
What makes AI agentic sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

An agent reasons, plans, acts, and observes outcomes in a loop. ReAct interleaves reasoning and acting so the model can inspect results.

Agents are useful when task steps are open-ended, tool-heavy, or need adaptation. A simple prompt is still better when the workflow is small and predictable. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- An agent reasons, plans, acts, and observes outcomes in a loop.
- ReAct interleaves reasoning and acting so the model can inspect results.
- Agents are useful when task steps are open-ended, tool-heavy, or need adaptation.
- A simple prompt is still better when the workflow is small and predictable.

Quick check: What pattern interleaves reasoning and acting?

Concept check: In one sentence, explain how this idea matters in a real AI system: What makes AI agentic.


## Lesson 7: Tools and function calling

Objective: Use schemas so the model can invoke tools reliably.

Context:
Tools and function calling sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Tool definitions should include a name, a description, and a JSON schema for parameters. Function calling turns tool use into structured requests instead of free-form text guesses.

Sequential and parallel tool calls each fit different workflows. Tool errors need retries, fallbacks, and clear failure handling. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Tool definitions should include a name, a description, and a JSON schema for parameters.
- Function calling turns tool use into structured requests instead of free-form text guesses.
- Sequential and parallel tool calls each fit different workflows.
- Tool errors need retries, fallbacks, and clear failure handling.

Quick check: What makes tool invocation reliable?

Concept check: In one sentence, explain how this idea matters in a real AI system: Tools and function calling.


## Lesson 8: MCP architecture and servers

Objective: Connect AI systems to tools through the modern universal protocol.

Context:
MCP architecture and servers sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

MCP separates host, client, and server responsibilities over JSON-RPC 2.0. Tools, resources, prompts, and sampling are core MCP primitives.

STDIO and Streamable HTTP cover local and remote transports. Building both a server and a client is part of practical AI engineering now. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- MCP separates host, client, and server responsibilities over JSON-RPC 2.0.
- Tools, resources, prompts, and sampling are core MCP primitives.
- STDIO and Streamable HTTP cover local and remote transports.
- Building both a server and a client is part of practical AI engineering now.

Quick check: What does MCP standardize?

Concept check: In one sentence, explain how this idea matters in a real AI system: MCP architecture and servers.


## Lesson 9: LangChain and LangGraph

Objective: Use graph-based orchestration when an agent needs state and control flow.

Context:
LangChain and LangGraph sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

LangChain covers prompts, chains, wrappers, and parsers. LangGraph adds nodes, edges, conditional routing, and durable state.

Checkpointers, threads, and interrupt nodes make human-in-the-loop workflows possible. Subgraphs help you keep large workflows modular and debuggable. OpenAI Agents SDK, CrewAI, AutoGen, and smolagents are alternatives with different tradeoffs. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- LangChain covers prompts, chains, wrappers, and parsers.
- LangGraph adds nodes, edges, conditional routing, and durable state.
- Checkpointers, threads, and interrupt nodes make human-in-the-loop workflows possible.
- Subgraphs help you keep large workflows modular and debuggable.
- OpenAI Agents SDK, CrewAI, AutoGen, and smolagents are alternatives with different tradeoffs.

Quick check: What LangGraph concept represents stateful routing?

Concept check: In one sentence, explain how this idea matters in a real AI system: LangChain and LangGraph.


## Lesson 10: Memory and multi-agent systems

Objective: Manage short-term and long-term memory, then coordinate several specialist agents.

Context:
Memory and multi-agent systems sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Short-term memory holds the live conversation buffer and recent state. Long-term memory uses a vector store or database to recall past work.

Multi-agent systems split work into roles such as planner, researcher, critic, and executor. Supervisor agents and handoffs keep specialization from turning into chaos. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Short-term memory holds the live conversation buffer and recent state.
- Long-term memory uses a vector store or database to recall past work.
- Multi-agent systems split work into roles such as planner, researcher, critic, and executor.
- Supervisor agents and handoffs keep specialization from turning into chaos.

Quick check: Which memory store usually holds past interactions?

Concept check: In one sentence, explain how this idea matters in a real AI system: Memory and multi-agent systems.


## Lesson 11: Agentic design patterns and production

Objective: Ship agents that are observable, secure, and useful in real workflows.

Context:
Agentic design patterns and production sits inside Agentic coding and AI agents. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Reflection, planning, routing, and tool augmentation are core agentic design patterns. Research agent, code agent, data analysis agent, RAG agent, browser agent, and workflow agent patterns are common applications.

Observability tools such as LangSmith or LangFuse help debug loops and tool choices. Production agents need prompt-injection defense, permission scoping, retries, idempotency, and cost control. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Reflection, planning, routing, and tool augmentation are core agentic design patterns.
- Research agent, code agent, data analysis agent, RAG agent, browser agent, and workflow agent patterns are common applications.
- Observability tools such as LangSmith or LangFuse help debug loops and tool choices.
- Production agents need prompt-injection defense, permission scoping, retries, idempotency, and cost control.

Quick check: What is one production safeguard for an agent?

Concept check: In one sentence, explain how this idea matters in a real AI system: Agentic design patterns and production.
