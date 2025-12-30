import random
USED_IDEAS = set()


RARE_WORDS = {
    "important": ["salient", "noteworthy"],
    "improve": ["enhance", "strengthen"],
    "use": ["employ", "utilize"],
    "help": ["facilitate", "support"],
    "role": ["function", "contribution"],
    "show": ["demonstrate", "indicate"],
    "many": ["numerous", "several"]
}


WRITING_STATES = ["analytical", "exploratory", "reflective", "assertive"]

def apply_rare_words(sentence, max_replacements=1):
    words = sentence.split()
    replaced = 0

    for i, w in enumerate(words):
        key = w.lower().strip(",.;")
        if key in RARE_WORDS and replaced < max_replacements:
            words[i] = RARE_WORDS[key][0]
            replaced += 1

    return " ".join(words)
def maybe_split_sentence(sentence):
    if " and " in sentence and len(sentence.split()) > 25:
        parts = sentence.split(" and ", 1)
        return [parts[0] + ".", "And " + parts[1]]
    return [sentence]


def select_state(previous_state):
    states = [s for s in WRITING_STATES if s != previous_state]
    return random.choice(states)


def generate_sentence(chunk):
    """
    Human-like light rewrite:
    - preserve sentence meaning
    - keep grammar intact
    - apply minimal variation
    """

    sentence = chunk.strip()

    # Ensure proper punctuation
    if not sentence.endswith("."):
        sentence += "."

    # Apply rare vocabulary (very limited)
    sentence = apply_rare_words(sentence, max_replacements=1)

    return sentence




def generate_paragraph(chunks, previous_state=None, max_ref=0):
    paragraph = []
    state = select_state(previous_state)

    sentence_count = random.randint(5, 7)
    used_local = set()

    attempts = 0
    max_attempts = sentence_count * 3

    while len(paragraph) < sentence_count and attempts < max_attempts:
        chunk = random.choice(chunks)
        attempts += 1

        # avoid repeating same idea in same paragraph
        if chunk in used_local:
            continue

        sentence = generate_sentence(chunk)
        sentence = maybe_add_citation(sentence, max_ref)
        paragraph.append(sentence)


        used_local.add(chunk)

        # allow very limited global reuse
        if random.random() < 0.25:
            USED_IDEAS.add(chunk)

    return paragraph, state
def maybe_add_citation(sentence, max_ref):
    """
    Add Vancouver-style in-text citation occasionally
    """
    if random.random() < 0.3 and max_ref > 0:
        ref_num = random.randint(1, max_ref)
        if not sentence.endswith("."):
            sentence += "."
        sentence = sentence.replace(".", f" [{ref_num}].", 1)
    return sentence
