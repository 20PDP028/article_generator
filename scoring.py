import random

def human_score():
    """
    Returns a probability-like score representing
    human-likeness of a paragraph
    """
    return round(random.uniform(0.65, 0.95), 2)


def confidence(score):
    """
    Confidence is derived from human_score
    """
    return round(score * random.uniform(0.9, 1.0), 2)
