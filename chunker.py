import nltk
from nltk.tokenize import sent_tokenize

# Download tokenizer once
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)


def chunk_text(text):
    sentences = sent_tokenize(text)
    chunks = []

    for sentence in sentences:
        if len(sentence.split()) > 3:
            chunks.append(sentence)

    return chunks
