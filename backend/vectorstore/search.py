import numpy as np

def search_similar_chunks(query_embedding, index, chunks, top_k=5):

    distances, indices = index.search(
        np.array([query_embedding]),
        top_k
    )

    results = []

    for idx in indices[0]:
        if idx < len(chunks):
            results.append(chunks[idx])

    return results