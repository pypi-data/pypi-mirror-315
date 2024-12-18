import sqlite3
import openai
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from datasets import load_dataset
from transformers import pipeline

# Initialize SentenceTransformer
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Intent Classifier
intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Initialize Database
def initialize_database(db_name="qa_database.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qa_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()

# Insert Question-Answer Pair
def insert_question_answer(question, answer, db_name="qa_database.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO qa_pairs (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

# Fetch Last Question-Answer Pair
def fetch_last_qa(db_name="qa_database.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM qa_pairs ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0], result[1]
    return None, None

# Generate Standalone Question Using OpenAI LLM
def generate_standalone_question_with_llm(api_key, endpoint_url, api_version, deployment_name, new_question, db_name="qa_database.db"):
    last_question, last_answer = fetch_last_qa(db_name)

    if last_question and last_answer:
        prompt = (
            f"You are a helpful assistant. "
            f"Here is the previous question and its answer:\n"
            f"Q: {last_question}\n"
            f"A: {last_answer}\n\n"
            f"Now, here is the new question: {new_question}\n\n"
            f"Generate a standalone question that incorporates the context of the previous question and answer."
        )
    else:
        return new_question

    try:
        openai.api_key = api_key
        openai.api_base = endpoint_url
        openai.api_type = "azure"
        openai.api_version = api_version

        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.5
        )

        standalone_question = response['choices'][0]['message']['content'].strip()
        return standalone_question

    except Exception as e:
        print(f"Error generating standalone question: {e}")
        return new_question

# Embed Text
def embed_text(text):
    return np.array(embed_model.encode(text)).astype('float32')

# Function to Setup FAISS Index
def setup_faiss(documents, embed_func):
    embeddings = [embed_func(doc) for doc in documents]
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index

# Retrieve Relevant Context
def retrieve_context(query, index, documents, embed_func, top_k=2):
    query_vector = embed_func(query).reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)
    retrieved_docs = [documents[i] for i in indices[0]]
    return " ".join(retrieved_docs)

# Call OpenAI Model for Answer
def call_openai_model(api_key, endpoint_url, api_version, deployment_name, question, context):
    prompt = (
        f"You are a helpful assistant. Use the context below to answer the question:\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}\n\n"
        f"Provide a detailed answer."
    )

    try:
        openai.api_key = api_key
        openai.api_base = endpoint_url
        openai.api_type = "azure"
        openai.api_version = api_version

        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )

        answer = response['choices'][0]['message']['content'].strip()
        return answer

    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."

# Load Dataset
def load_dataset_and_prepare_faiss():
    ds = load_dataset("LangChainDatasets/question-answering-state-of-the-union")
    questions = ds["train"]['question']
    answers = ds["train"]["answer"]
    documents = [f"Q: {q} A: {a}" for q, a in zip(questions, answers)]
    index = setup_faiss(documents, embed_text)
    return documents, index

# Intent Classification
def classify_intent(query, candidate_labels):
    result = intent_classifier(query, candidate_labels)
    return result

# Check Intent Score for Blocked Categories
def check_intent_score(intent_result, threshold=0.4):
    for label, score in zip(intent_result['labels'], intent_result['scores']):
        if score > threshold:
            return True
    return False

# RAG Pipeline
def rag_pipeline_with_db_and_standalone_llm(api_key, endpoint_url, api_version, deployment_name, user_query, documents, index, db_name="qa_database.db"):
    # Intent Classification
    candidate_labels = ['weapons','crime','sexual','finance','medical']
    intent_result = classify_intent(user_query, candidate_labels)
    #print("Intent Classification Result:", intent_result)

    # Check Intent Score for Blocked Categories
    if check_intent_score(intent_result):
        return "User query belongs to the blocked category"

    # Use main question (user_query) to retrieve context
    retrieved_context = retrieve_context(user_query, index, documents, embed_text)

    # Generate a standalone question using the context of the last Q&A
    standalone_question = generate_standalone_question_with_llm(api_key, endpoint_url, api_version, deployment_name, user_query, db_name)

    # Call the OpenAI model with the standalone question and the retrieved context
    response = call_openai_model(api_key, endpoint_url, api_version, deployment_name, standalone_question, retrieved_context)

    # Store the Q&A pair in the database
    insert_question_answer(user_query, response, db_name)

    return response

# Main Function
if __name__ == "__main__":
    # Initialize Database
    initialize_database()

    # Configuration
    api_key = "86d74b097800428b92e4d8ca402e069d"
    endpoint_url = "https://azureopenaiblogo.openai.azure.com/"
    api_version = "2024-08-01-preview"
    deployment_name = "gpt-35-turbo"

    # Load Dataset and Prepare FAISS
    documents, index = load_dataset_and_prepare_faiss()

    # User Query
    user_query = "What is the weapon user is speaking about?"

    # Run RAG Pipeline
    result = rag_pipeline_with_db_and_standalone_llm(api_key, endpoint_url, api_version, deployment_name, user_query, documents, index)
    print("RAG Response:")
    print(result)