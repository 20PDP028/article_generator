from collections import Counter
from model_interface import generate_candidates

USED_SENTENCES = set()
STARTER_MEMORY = Counter()

# ---------------------------------------------
# INFORMATION DENSITY (vagueness detector)
# ---------------------------------------------
def information_density(sentence):
    words = sentence.split()
    if not words:
        return 0
    return len(set(words)) / len(words)

# ---------------------------------------------
# SENTENCE FUNCTION (STRUCTURAL)
# ---------------------------------------------
def sentence_function(sentence):
    if sentence.endswith("?"):
        return "question"
    if "," in sentence and len(sentence.split()) > 20:
        return "explanatory"
    if len(sentence.split()) < 12:
        return "assertive"
    return "descriptive"

# ---------------------------------------------
# HARD LOGIC GATE — OPTION A (STRICT)
# ---------------------------------------------
def passes_all_logics(sentence):
    s = sentence.lower().strip()

    # Starter repetition
    starter = " ".join(s.split()[:2])
    if STARTER_MEMORY[starter] >= 3:
        return False

    # Exact repetition
    if s in USED_SENTENCES:
        return False

    # Low information density
    if information_density(s) < 0.45:
        return False

    # Encyclopedic structure
    if ":" in s[:15] or s.startswith("("):
        return False

    return True

# ---------------------------------------------
# SENTENCE GENERATION (NO FALLBACK)
# ---------------------------------------------
def generate_sentence(chunk):
    candidates = generate_candidates(chunk)

    for sent in candidates:
        if passes_all_logics(sent):
            final = sent.strip()
            if not final.endswith("."):
                final += "."

            USED_SENTENCES.add(final.lower())
            STARTER_MEMORY[" ".join(final.lower().split()[:2])] += 1
            return final

    return None  # STRICT MODE

# ---------------------------------------------
# PARAGRAPH GENERATION
# ---------------------------------------------
def generate_paragraph(chunks):
    paragraph = []
    attempts = 0

    while len(paragraph) < 6 and attempts < 30:
        attempts += 1
        sent = generate_sentence(chunks[attempts % len(chunks)])
        if sent:
            paragraph.append(sent)

    if len(paragraph) < 3:
        return None

    return paragraph