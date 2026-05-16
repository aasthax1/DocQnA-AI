from flask import Flask, render_template, request
import os

from utils.pdf_reader import extract_text_from_pdf
from utils.text_chunker import chunk_text
from utils.embeddings import create_embeddings

from vectorstore.faiss_store import store_embeddings
from vectorstore.search import search_similar_chunks

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

UPLOAD_FOLDER = "../uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Global storage
stored_chunks = []
stored_index = None


# Home
@app.route("/")
def home():
    return render_template("index.html")


# Upload PDF
@app.route("/upload", methods=["POST"])
def upload_file():

    global stored_chunks, stored_index

    if "pdf_file" not in request.files:
        return "No file uploaded"

    file = request.files["pdf_file"]

    if file.filename == "":
        return "No selected file"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Extract text
    pdf_text = extract_text_from_pdf(filepath)

    # Chunk text
    chunks = chunk_text(pdf_text)

    # Embeddings
    embeddings = create_embeddings(chunks)

    # FAISS index
    index = store_embeddings(embeddings)

    # Store globally
    stored_chunks = chunks
    stored_index = index

    return f"""
    <h1>PDF Uploaded Successfully!</h1>
    <h2>Total Chunks: {len(chunks)}</h2>
    <h2>Vector Store Created Successfully!</h2>
    <br>
    <a href="/">Go Back</a>
    """


# Ask Question (FINAL CLEAN VERSION)
@app.route("/ask", methods=["POST"])
def ask_question():

    global stored_chunks, stored_index

    if stored_index is None:
        return """
        <h1>Please upload a PDF first!</h1>
        <a href="/">Go Back</a>
        """

    question = request.form["question"]

    # Create embedding
    query_embedding = create_embeddings([question])[0]

    # Retrieve ONLY top 1 result
    results = search_similar_chunks(
        query_embedding,
        stored_index,
        stored_chunks
    )

    best_result = results[0] if results else "No relevant information found."

    return f"""
    <h1>Question Asked:</h1>
    <h2>{question}</h2>

    <br>

    <h1>Best Matching Answer:</h1>

    <div style="
        background-color:#f4f4f4;
        padding:20px;
        border-radius:10px;
    ">
        <p>{best_result}</p>
    </div>

    <br>

    <a href="/">Ask Another Question</a>
    """


if __name__ == "__main__":
    app.run(debug=True)