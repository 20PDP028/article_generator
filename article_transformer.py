import re
import fitz  # PyMuPDF

# -------------------------------------------------
# LOAD PDF (single source of truth)
# -------------------------------------------------
def load_article(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

# -------------------------------------------------
# STRUCTURE EXTRACTION (NO KEYWORDS)
# -------------------------------------------------
def extract_structured_sections(raw_text):
    sections = []
    current = {"title": "UNLABELED", "lines": []}
    sections.append(current)

    for line in raw_text.split("\n"):
        clean = line.strip()
        if not clean:
            continue

        # Structural heading detection
        if clean.isupper() and len(clean.split()) <= 12:
            current = {"title": clean, "lines": []}
            sections.append(current)
            continue

        if clean.istitle() and len(clean.split()) <= 12:
            current = {"title": clean, "lines": []}
            sections.append(current)
            continue

        current["lines"].append(clean)

    return sections

# -------------------------------------------------
# SENTENCE CHUNKING
# -------------------------------------------------
def chunk_sections(sections):
    output = []
    for sec in sections:
        text = " ".join(sec["lines"])
        sentences = re.split(r"(?<=[.!?])\s+", text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 40]
        output.append({"title": sec["title"], "chunks": sentences})
    return output

# -------------------------------------------------
# REFERENCES
# -------------------------------------------------
def extract_references(raw_text):
    refs = []
    started = False
    for line in raw_text.split("\n"):
        l = line.strip()
        if "references" in l.lower():
            started = True
            continue
        if started and len(l) > 20:
            refs.append(l)
    return refs

def format_references_vancouver(refs):
    return [re.sub(r"\s+", " ", r).strip() for r in refs]