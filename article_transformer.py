import re
import fitz
from chunker import chunk_text


def load_article(path):
    if path.endswith(".pdf"):
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    elif path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Only PDF or TXT allowed")


def preprocess(text):
    # Remove References section
    text = re.split(r'References', text, flags=re.IGNORECASE)[0]

    # Remove headings, tables, figures, keywords, abstract labels
    remove_patterns = [
        r'\bAbstract\b',
        r'\bIntroduction\b',
        r'\bConclusion\b',
        r'\bKeywords?:.*',
        r'\bTable\s*\d+.*',
        r'\bFigure\s*\d+.*',
        r'Pharmaceutical Care and SDG.*',
        r'Integrating SDG 3 and SDG 17.*',
        r'Challenges and Barriers.*',
        r'Overview of the Sustainable Development Goals.*'
    ]

    for pattern in remove_patterns:
        text = re.sub(pattern, ' ', text, flags=re.IGNORECASE)

    # Remove multiple spaces and line breaks
    text = re.sub(r'\s+', ' ', text)

    return text.strip()




def article_to_chunks(path):
    raw = load_article(path)
    clean = preprocess(raw)
    return chunk_text(clean)

def classify_chunks_by_section(chunks):
    """
    Very simple heuristic-based section classifier
    """

    intro, discussion, conclusion = [], [], []

    for c in chunks:
        c_low = c.lower()

        # Conclusion-like signals
        if any(x in c_low for x in [
            "in conclusion", "overall", "this review highlights",
            "in summary", "future directions", "therefore"
        ]):
            conclusion.append(c)

        # Introduction-like signals
        elif any(x in c_low for x in [
            "sustainable development goal", "sdg",
            "world health organization", "global health",
            "background", "overview", "framework"
        ]):
            intro.append(c)

        # Default → discussion
        else:
            discussion.append(c)

    return {
        "introduction": intro,
        "discussion": discussion,
        "conclusion": conclusion
    }
def extract_references(text):
    """
    Extract references section from the original article
    """
    parts = re.split(r'References', text, flags=re.IGNORECASE)
    if len(parts) > 1:
        refs = parts[1]
        lines = refs.split("\n")
        clean_refs = []

        for line in lines:
            line = line.strip()
            if len(line) > 10:
                clean_refs.append(line)

        return clean_refs

    return []
def format_references_vancouver(refs):
    """
    Simple Vancouver-style formatting:
    numbering + cleaned lines
    """
    formatted = []

    for i, ref in enumerate(refs, 1):
        ref = ref.strip()
        ref = ref.replace("  ", " ")
        formatted.append(f"{i}. {ref}")

    return formatted
