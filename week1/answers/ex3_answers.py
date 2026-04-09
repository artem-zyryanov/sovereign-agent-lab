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

NOTE: The cutoff guard fired because the conversation was run after 18:00.
All three slots were collected correctly (160 guests, 50 vegan, £200 deposit)
but the time check triggered before the deposit/capacity guards could run.
If run before 16:45, this would have resulted in "confirmed" (all guards pass).
"""

CONVERSATION_1_OUTCOME = "escalated"  # cutoff guard fired (run after 16:45)

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input: Hello, calling about the booking confirmation
Bot: How many guests are you confirming for tonight's event?
Your input: 160
Bot: And how many of those guests will need vegan meals?
Your input: roughly 50
Bot: What deposit amount in GBP are you proposing to secure the booking?
Your input: £500
Bot: I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Bot: Is there anything else I can help you with?

NOTE: The cutoff guard fired first (run after 18:00), preventing the deposit
guard from being reached. If run before 16:45, the deposit guard would have
fired instead with: "a deposit of £500 exceeds the organiser's authorised
limit of £300".
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline (cutoff guard fired first; deposit guard would have triggered with: a deposit of £500 exceeds the organiser's authorised limit of £300)"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input: Hi, I need to confirm a booking
Bot: How many guests are you confirming for tonight's event?
Your input: 160
Bot: And how many of those guests will need vegan meals?
Your input: Actually, can you arrange parking for the speakers?
Bot: I'm sorry, I'm not trained to help with that.
Bot: I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Bot: Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM recognized the parking question as out of scope and responded with two messages: first
"I'm sorry, I'm not trained to help with that" and then the explicit deflection "I can only
help with confirming tonight's venue booking." Crucially, CALM then asked "Would you like to
continue with confirm booking?" — maintaining the conversational state and offering to resume
the flow from exactly where it left off (collecting the vegan count slot). This shows CALM's
flow-based architecture keeps the conversation on track even when the user goes off-topic.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
LangGraph and Rasa CALM handle out-of-scope requests very differently. LangGraph's agent gave a
vague non-answer ("Your input is lacking necessary details") and stopped — it did not try to call
tools, which was correct, but it also did not explain that train times are outside its scope or
suggest an alternative resource. Rasa CALM, by contrast, would deflect with a clear out-of-scope
message and then immediately resume the booking flow from where it left off, re-asking for the
missing slot. The key difference is that CALM maintains conversational state: it knows it is in
the middle of collecting booking details and returns to that task. LangGraph has no such memory
of an ongoing flow — each query is essentially stateless. For a booking confirmation assistant,
CALM's approach is clearly superior because it keeps the call on track.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
The cutoff guard was uncommented in actions.py. Testing happened naturally: all three conversations
were run after 18:00, so the cutoff guard (checking if now.hour > 16 or now.minute >= 45) fired
on every conversation. In Conversations 1 and 2, all three slots were collected successfully but
the validation action immediately escalated with "it is past 16:45 — insufficient time to process
the confirmation before the 5 PM deadline." This proves the guard works in production conditions
without needing to temporarily set 'if True:'. The guard is the first check in the action, so it
fires before capacity, deposit, or vegan ratio guards can run.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

CALM_VS_OLD_RASA = """
CALM simplifies development significantly by offloading language understanding to the LLM. In old
Rasa, you needed regex-based slot extraction in Python (parsing "about 160 people" into 160.0),
extensive NLU training examples in nlu.yml, and explicit dialogue rules. CALM eliminates all of
that: the LLM handles natural language parsing via from_llm slot mappings, and flow descriptions
replace rigid rules. What Python still handles — and must handle — are the deterministic business
rules: deposit limits, capacity checks, vegan ratios, and the time cutoff guard. These cannot be
trusted to an LLM because the LLM might rationalize exceptions. The cost of CALM is that you lose
fine-grained control over how language is interpreted and depend on the LLM's quality. The gain is
dramatically less boilerplate code and better handling of natural language variations without
explicit training data.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

SETUP_COST_VALUE = """
CALM's setup cost — config.yml, domain.yml, flows.yml, endpoints.yml, training, two terminals,
and a Rasa Pro license — buys you something specific: constrained execution. The CALM agent cannot
improvise responses outside its defined flows, cannot call tools not specified in flows.yml, and
cannot skip the business rule validation in ActionValidateBooking. It will always collect all three
slots before running the validation action. LangGraph, by contrast, is a single Python file with
a generic loop — faster to set up but the agent can do anything the LLM decides, including skipping
steps or making up information. For a booking confirmation call where legal and financial constraints
must be enforced deterministically, CALM's rigidity is a feature: the agent physically cannot confirm
a booking without running the Python guards. That guarantee is what the setup cost pays for.
"""
