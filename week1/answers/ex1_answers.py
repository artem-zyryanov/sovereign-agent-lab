"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All three formatting conditions produced correct answers with the 70B model. The plain
format returned The Haymarket Vaults while both XML and sandwich formats returned The
Albanach. Both venues satisfy all constraints (capacity >= 160, vegan options, quiet
corner for webinar). The structured formats (XML and sandwich) converged on the same
answer, suggesting that explicit context boundaries helped the model focus on the same
reasoning path, while the unstructured plain format led to a different but equally valid
choice.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The near-miss distractor that almost meets all constraints but fails on one dimension
(e.g., a venue with 150 capacity and vegan options but no quiet corner) would be the
hardest, because the model must carefully cross-check each constraint rather than
rejecting on an obvious mismatch. However, the 70B model was robust enough that no
distractor changed the results in any formatting condition.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True

PART_C_PLAIN_ANSWER    = "Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C ran because Parts A and B were all correct, triggering the small-model test with
google/gemma-2-2b-it. Even the 2B parameter model got all three answers correct, always
selecting The Haymarket Vaults regardless of formatting. This was surprising because the
smaller model was expected to be more susceptible to distractor confusion. The fact that
all formats converged on the same venue (unlike the 70B model which split between
Albanach and Haymarket) suggests the smaller model may use a simpler heuristic that
happens to be correct here but might be less robust on harder problems.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the model is smaller, the context window is longer,
or the task involves distinguishing between near-miss candidates that differ on only one
constraint. In this exercise the 70B model was robust across all formats, but in production
you cannot assume ideal conditions. Structured formats like XML tags and sandwich framing
provide explicit boundaries that help models locate the relevant constraints, which becomes
critical as context length grows, distractor density increases, or model capability decreases.
The formatting is a form of prompt engineering that trades verbosity for reliability.
"""
