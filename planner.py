def infer_intent_from_heading(heading):
    """
    Intent is inferred by structure only.
    No domain or keyword logic.
    """
    if heading.isupper():
        return "expand"

    if len(heading.split()) <= 3:
        return "expand"

    return "expand"