"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = False

# Optional — anything unexpected.
# If you used a non-default model via RESEARCH_MODEL env var, note it here.
# Example: "Used nvidia/nemotron-3-super-120b-a12b for the agent loop."
TASK_A_NOTES = "Used default Qwen/Qwen3-32B model. Weather showed 11.3C, code 53 (drizzle), precipitation 0.2mm."

# ── Task B ─────────────────────────────────────────────────────────────────

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "placeholder"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://placehold.co/1200x628/1a1a2e/eaeaea?text=The+Haymarket+Vaults+%7C+160+guests&id=2ef939fbbaf6"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
The tool always returns success=True with a structured result regardless of whether the image provider is available — the agent's control flow is decoupled from the provider's availability, so the ReAct loop continues unaffected whether the tool uses a live model or a placeholder fallback.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
After checking The Bow Bar and finding meets_all_constraints=false (capacity 80, status full), the agent pivoted by calling check_pub_availability for The Albanach, which returned meets_all_constraints=true, and confirmed it as the fallback venue.
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
Unfortunately, none of the known venues in Edinburgh meet the requirements for 300 people with vegan options.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = "The agent explained it doesn't have tools for train schedules and suggested checking National Rail or Trainline websites for Edinburgh Waverley departure times."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Yes, this behaviour is acceptable and desirable. The agent correctly identified that train
schedules are outside its tool capabilities and declined to fabricate an answer. Instead it
directed the user to authoritative sources (National Rail, Trainline). In a real booking
assistant, admitting scope boundaries and suggesting alternatives is far safer than
hallucinating a departure time that could cause someone to miss their train. The only
improvement would be if the agent had a web search tool to look up the answer in real time.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TD;
	__start__([<p>__start__</p>]):::first
	agent(agent)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> agent;
	tools --> agent;
	agent -.-> tools;
	agent -.-> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill:#DAE8FC,stroke:#6C8EBF
	classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph Mermaid graph shows a single generic loop: start -> agent -> tools -> agent
-> end. There are no named tasks, no named tools, no explicit paths. The agent decides at
runtime which tool to call and when to stop. In contrast, flows.yml explicitly names every
flow (confirm_booking, handle_out_of_scope), lists every step (collect guest_count, collect
vegan_count, collect deposit_amount_gbp, then action_validate_booking), and defines exactly
when each flow triggers via its description. LangGraph is a blank canvas where the model
paints the path; Rasa CALM is a railroad where the model only picks which track to ride.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most surprising behaviour was in Scenario 2 (300 guests). After checking all four
venues and finding none met the capacity requirement, the agent cleanly admitted failure
without hallucinating a fictional venue. Many LLMs under pressure to be helpful would
invent a plausible-sounding Edinburgh pub name. The Qwen3-32B model instead gave a direct
"none of the known venues meet the requirements" response. This is exactly the behaviour
you need in a production agent — failing honestly is more valuable than confidently making
things up, especially when a wrong answer could lead to booking a venue that cannot
actually accommodate the group.
"""
