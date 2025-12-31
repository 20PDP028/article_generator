from article_transformer import (
    load_article,
    extract_structured_sections,
    chunk_sections,
    extract_references,
    format_references_vancouver
)
from paragraph_engine import generate_paragraph
from planner import infer_intent_from_heading
from word_exporter import export_to_word

INPUT_PDF = "Untitled document.pdf"

raw_text = load_article(INPUT_PDF)
sections = chunk_sections(extract_structured_sections(raw_text))
references = format_references_vancouver(extract_references(raw_text))

article = []

for sec in sections:
    paragraph = generate_paragraph(sec["chunks"])
    if paragraph:
        article.append((sec["title"], paragraph, 1.0))

export_to_word(article, references, filename="final_article.docx")
print("✅ Final article generated (PDF-agnostic, cognitive, strict)")