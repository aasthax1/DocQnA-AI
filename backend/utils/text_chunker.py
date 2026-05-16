import nltk
from nltk.tokenize import sent_tokenize

def chunk_text(text, chunk_size=3):

    sentences = sent_tokenize(text)

    chunks = []

    current_chunk = []

    for sentence in sentences:

        current_chunk.append(sentence)

        if len(current_chunk) >= chunk_size:

            chunks.append(" ".join(current_chunk))

            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks