import re

def generate_candidates(text, n=5):
    """
    Generate candidate sentences using ONLY structural variation.
    No new words. No keywords. No domain assumptions.
    """

    base = text.strip()

    # Remove trailing punctuation for safe manipulation
    base = re.sub(r"[.]+$", "", base)

    words = base.split()
    candidates = []

    # -------------------------------------------------
    # 1. Original sentence (baseline)
    # -------------------------------------------------
    candidates.append(base)

    # -------------------------------------------------
    # 2. Truncated version (removes tail only)
    # -------------------------------------------------
    if len(words) > 12:
        candidates.append(" ".join(words[:-4]))

    # -------------------------------------------------
    # 3. Clause split (if punctuation exists)
    # -------------------------------------------------
    for sep in [",", ";"]:
        if sep in base:
            left, right = base.split(sep, 1)
            if len(left.split()) > 6:
                candidates.append(left.strip())
            if len(right.split()) > 6:
                candidates.append(right.strip())

    # -------------------------------------------------
    # 4. Reordered sentence (positional shift only)
    # -------------------------------------------------
    if len(words) > 10:
        mid = len(words) // 2
        reordered = " ".join(words[mid:] + words[:mid])
        candidates.append(reordered)

    # -------------------------------------------------
    # 5. Minimal emphasis shift (punctuation only)
    # -------------------------------------------------
    if len(words) > 8:
        candidates.append(base + " —")

    # -------------------------------------------------
    # Cleanup: remove duplicates and junk
    # -------------------------------------------------
    final = []
    seen = set()

    for c in candidates:
        c = c.strip()
        if not c:
            continue
        if c in seen:
            continue
        if len(c.split()) < 6:
            continue
        final.append(c)
        seen.add(c)

    return final[:n]