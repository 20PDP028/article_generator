from word_exporter import export_to_word
from article_transformer import article_to_chunks, classify_chunks_by_section
from paragraph_engine import generate_paragraph
from scoring import human_score, confidence
from article_transformer import extract_references, format_references_vancouver



print("Program started")

INPUT_ARTICLE = "Untitled document.pdf"
THRESHOLD = 0.75

chunks = article_to_chunks(INPUT_ARTICLE)
# Load full raw article text for references
from article_transformer import load_article
raw_text = load_article(INPUT_ARTICLE)

raw_refs = extract_references(raw_text)
references = format_references_vancouver(raw_refs)


sections = classify_chunks_by_section(chunks)

intro_chunks = sections["introduction"]
discussion_chunks = sections["discussion"]
conclusion_chunks = sections["conclusion"]


article = []
prev_state = None

TARGET_WORDS = 3500  # you can change this later
AVG_WORDS_PER_PARAGRAPH = 140

TARGET_PARAGRAPHS = TARGET_WORDS // AVG_WORDS_PER_PARAGRAPH

article = []
prev_state = None

INTRO_PARA = int(TARGET_PARAGRAPHS * 0.2)
DISC_PARA = int(TARGET_PARAGRAPHS * 0.6)
CONC_PARA = TARGET_PARAGRAPHS - INTRO_PARA - DISC_PARA

# --- INTRODUCTION ---
for _ in range(INTRO_PARA):
    paragraph, prev_state = generate_paragraph(
        intro_chunks,
        prev_state,
        max_ref=len(references)
    )

    score = human_score()
    while score < THRESHOLD:
        paragraph, _ = generate_paragraph(intro_chunks, prev_state)
        score = human_score()
    article.append((paragraph, confidence(score)))

# --- DISCUSSION ---
for _ in range(DISC_PARA):
    paragraph, prev_state = generate_paragraph(
        intro_chunks,
        prev_state,
        max_ref=len(references)
    )
    score = human_score()
    while score < THRESHOLD:
        paragraph, _ = generate_paragraph(discussion_chunks, prev_state)
        score = human_score()
    article.append((paragraph, confidence(score)))

# --- CONCLUSION ---
for _ in range(CONC_PARA):
    paragraph, prev_state = generate_paragraph(
        intro_chunks,
        prev_state,
        max_ref=len(references)
    )
    score = human_score()
    while score < THRESHOLD:
        paragraph, _ = generate_paragraph(conclusion_chunks, prev_state)
        score = human_score()
    article.append((paragraph, confidence(score)))


for i, (para, conf) in enumerate(article, 1):
    print(f"\nParagraph {i} (confidence={conf})")
    for s in para:
        print("-", s)
export_to_word(
    article,
    intro_count=INTRO_PARA,
    discussion_count=DISC_PARA,
    conclusion_count=CONC_PARA,
    references=references
)

print("\nArticle exported successfully with References as final_article.docx")
