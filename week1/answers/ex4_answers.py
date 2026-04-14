"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No venues match the requirements for 300 guests."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Changed The Albanach's status from "available" to "full" in mcp_venue_server.py. Re-ran the
client. search_venues returned only 1 match (The Haymarket Vaults) instead of 2, because
The Albanach no longer met the availability constraint. Only mcp_venue_server.py was modified —
exercise4_mcp_client.py was NOT changed at all. The client automatically saw different results
because it discovers tools and their data dynamically from the server at runtime. After
verifying the changed behaviour, the modification was reverted to restore the original state.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 0
LINES_OF_TOOL_CODE_EX4 = 0

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP provides runtime tool discovery: the client learns what tools exist, their schemas, and
their capabilities at connection time, not at code time. This means you can add, remove, or
modify tools on the server without touching any client code. In Exercise 2, the tools are
imported as Python functions — changing a tool signature requires updating every file that
imports it. In Exercise 4, the client calls whatever the server exposes.

More importantly for PyNanoClaw, MCP is the shared layer that lets BOTH halves of the hybrid
system (the LangGraph autonomous loop and the Rasa structured agent) access the same tools
through the same protocol. Neither half needs to know about the other's implementation. The
server is the single source of truth for what capabilities exist, and both halves discover
them independently. This is what makes a hybrid architecture composable rather than tangled.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner (pynanoclaw/agents/planner.py) is a strong-reasoning model that decomposes Rod's WhatsApp message into an ordered list of subgoals (find venue, check weather, calculate catering, generate flyer, confirm booking with pub manager). It lives upstream of the ReAct loop in the autonomous-loop half, ensuring the Executor receives clear, sequenced tasks rather than an ambiguous natural language blob.

- The Executor (pynanoclaw/agents/executor.py) is the evolution of Week 1's research_agent.py — a fast ReAct loop using Qwen3-32B that works through the Planner's subgoals one at a time, calling tools from the shared MCP server. It lives in the autonomous-loop half and handles all open-ended research: venue search, weather checks, catering calculations, and flyer generation. When it hits a subgoal requiring human conversation (e.g., "confirm booking with pub manager"), it delegates via the Handoff Bridge instead of attempting it itself.

- The Handoff Bridge (pynanoclaw/bridge/handoff.py) is the routing layer between the two halves. When the Executor encounters a task that requires structured, auditable human interaction (booking confirmation), it passes context (chosen venue, guest count, constraints) to the Rasa CALM agent. When the CALM agent needs research (e.g., looking up live venue data mid-conversation), it delegates back to the Executor. The bridge lives in the shared layer between both halves, carrying structured context in both directions.

- The Shared MCP Tool Server (evolved from Week 1's mcp_venue_server.py) is the single tool registry that both halves discover at runtime. It grows from 2 tools (search_venues, get_venue_details) to cover web search, booking confirmation, calendar access, email, and file operations. It lives in the shared layer — neither the autonomous loop nor the structured agent imports tools directly; both discover them via MCP protocol, which is why changing a tool on the server requires zero client-side changes.

- The Structured Confirmation Agent (evolved from Week 1's exercise3_rasa/ CALM agent) handles the pub manager phone call with deterministic flows, business-rule guards in Python (capacity, deposit, vegan ratio, time cutoff), and an optional RAG knowledge base for questions outside flows.yml. It lives in the structured-agent half of PyNanoClaw, connected to the shared MCP server for live venue data and to the Handoff Bridge for delegating research back to the autonomous loop.

- The Persistent Memory Store (pynanoclaw/memory/persistent_store.py) is a filesystem-backed store that tracks the state of Rod's request across both halves — which venues were checked, which was selected, what the weather was, whether the booking was confirmed. It lives in the shared layer so both the Executor and the CALM agent can read and write to it, ensuring neither half loses context when control passes through the Handoff Bridge.

- The Observability Layer (pynanoclaw/observability/) provides tracing, cost tracking, and guardrail monitoring across both halves. It records every tool call, every LLM invocation, every handoff, and every business-rule decision, producing an end-to-end audit trail from Rod's WhatsApp message to the confirmed booking. It lives in the shared layer, wrapping both halves uniformly.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The LangGraph autonomous loop is the right agent for the research phase. In Exercise 2
Task A, it chose its own tool order (check_pub_availability, then calculate_catering_cost,
then get_edinburgh_weather, then generate_event_flyer), pivoted when The Bow Bar was full
in Scenario 1, and honestly admitted failure for 300 guests in Scenario 2. That flexibility
is essential for open-ended research where the path depends on intermediate results.

The Rasa CALM structured agent is the right agent for the pub manager call. In Exercise 3,
it collected slots in a fixed order, applied deterministic business rules in Python (the
cutoff guard, the deposit cap), deflected out-of-scope parking questions with a pre-written
message, and offered to resume the interrupted flow. Every path is explicit in flows.yml
and auditable.

Swapping them feels wrong because each would fail at the other's job. If Rasa CALM did the
research, you would need to pre-define a flow for every possible venue combination, weather
outcome, and fallback path — the combinatorial explosion makes it impractical. If LangGraph
handled the pub manager call, the model could improvise around the £300 deposit limit, skip
the time cutoff check, or hallucinate a confirmation. In Scenario 3, LangGraph composed its
own free-form response about trains — harmless for research, but unacceptable when committing
Rod's money. The core lesson is that flexibility and auditability are in tension, and
PyNanoClaw resolves this by using each technology where it belongs.
"""
