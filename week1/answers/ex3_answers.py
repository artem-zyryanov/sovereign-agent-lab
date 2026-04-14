"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input: Hi, I'm calling to confirm a booking for tonight
Bot: How many guests are you confirming for tonight's event?
Your input: 160 guests
Bot: And how many of those guests will need vegan meals?
Your input: about 50 need vegan meals
Bot: What deposit amount in GBP are you proposing to secure the booking?
Your input: £200 deposit
Bot: I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Bot: Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input: Calling about the booking
Bot: How many guests are you confirming for tonight's event?
Your input: 160
Bot: And how many of those guests will need vegan meals?
Your input: 50
Bot: What deposit amount in GBP are you proposing to secure the booking?
Your input: £500
Bot: I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Bot: Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline (cutoff guard fired first; deposit guard would have fired independently since £500 exceeds the £300 authorised limit)"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input: Hi, confirming a booking
Bot: How many guests are you confirming for tonight's event?
Your input: 160
Bot: And how many of those guests will need vegan meals?
Your input: Can you arrange parking for the speakers?
Bot: I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Bot: Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM detected that "can you arrange parking for the speakers?" was outside the confirm_booking
flow scope. It triggered the handle_out_of_scope flow, which uttered the deflection message
telling the user to contact the event organiser directly. Then it offered to resume the
confirm_booking flow where it left off, asking if the user wanted to continue with the booking
confirmation. The flow state (guest_count already collected) was preserved across the interruption.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa CALM handled the out-of-scope request structurally: the LLM matched the parking question
to the handle_out_of_scope flow, which delivered a scripted deflection message and then offered
to resume the interrupted confirm_booking flow. The conversation state was preserved — the agent
remembered that guest_count was already collected and only needed to re-ask for vegan_count.

LangGraph's agent in Scenario 3 (train times) handled it purely through model reasoning: it
recognised the question was outside its tool capabilities and generated a free-form response
suggesting external resources. There was no explicit "out of scope" flow — the model simply
chose not to call any tool and composed its own answer.

The CALM approach is more predictable and auditable: the deflection message is written in
advance, the resume behaviour is deterministic, and you can guarantee the exact wording.
The LangGraph approach is more flexible but less controllable — the model might give a
different response each time, and there is no mechanism to resume a prior conversation flow.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Ran all three conversations after 18:00 local time, so the cutoff guard (now.hour > 16 or
now.hour == 16 and now.minute >= 45) fired on every conversation that reached the
action_validate_booking step. Both conversations 1 and 2 escalated with the cutoff message
confirming the guard works. The cutoff guard fires before the deposit and capacity guards
because it is checked first in the action's run method.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

CALM_VS_OLD_RASA = """
The LLM now handles natural language understanding that Python handled before: parsing "about
160 people" into 160.0, recognising "calling to confirm a booking" as a booking intent, and
detecting out-of-scope requests — all without regex, intent training examples, or rules.yml.

Python STILL handles the business rules (capacity limits, deposit caps, vegan ratio checks,
time cutoffs) because these must be deterministic and auditable. A prompt that says "reject
deposits over £300" can be reasoned around by a clever model; a Python comparison cannot.

The cost is opacity: in the old approach you could read nlu.yml training examples and know
exactly which phrases mapped to which intent. With CALM, the LLM's understanding is a black
box — you trust it parses "one-sixty" to 160 but cannot inspect the mapping. The gain is
dramatic reduction in maintenance: no regex to update, no training examples to curate, and
new phrasings work automatically.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

SETUP_COST_VALUE = """
CALM still requires config.yml, domain.yml, flows.yml, endpoints.yml, rasa train, two
terminal processes (rasa server + action server), and a Rasa Pro licence. That is substantially
more infrastructure than LangGraph, which needs one Python file and one process.

What this setup bought is confinement. The CALM agent CANNOT improvise a response that was not
anticipated in flows.yml. It CANNOT call a tool that was not defined as a step. It CANNOT skip
the deposit check or invent a new flow at runtime. When the parking question came in, it fired
a pre-written deflection and offered to resume — it could not decide to helpfully Google parking
garages on its own.

For the confirmation use case, this confinement is a feature, not a limitation. A booking
confirmation is a financial commitment on Rod's behalf. You want the agent to follow an exact
script, apply exact rules, and escalate on exact conditions. The LangGraph agent's flexibility —
choosing its own tools, composing its own responses — is exactly what you do NOT want when
someone is committing money. The setup cost buys auditability and predictability, which are
non-negotiable for high-stakes conversational workflows.
"""
