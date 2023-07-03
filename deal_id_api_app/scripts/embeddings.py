import os
import openai
import datetime
import numpy as np
import pickle
from urllib.parse import urlparse
from sklearn.metrics.pairwise import cosine_similarity

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
os.environ['USER_PROMPT'] = 'Here is the info from the text: {content}. Based on this, what is the answer to "{question}"?'

def chunk_text(text, max_tokens=8000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(word)
        current_length += len(word) + 1
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def get_embedding_for_large_text(text):
    chunks = chunk_text(text)
    embeddings = []
    for chunk in chunks:
        response = openai.Embedding.create(input=chunk, model="text-embedding-ada-002")
        embedding = response['data'][0]['embedding']
        embeddings.append(embedding)
    return embeddings

def create_file_name(url, extension='txt'):
    parsed_url = urlparse(url)
    url_path_parts = parsed_url.path.strip('/').split('/')
    last_part = url_path_parts[-1] if url_path_parts else parsed_url.netloc
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"{last_part}-{current_date}.{extension}"

def get_most_similar_text_chunk(question, embeddings_dict):
    question_embedding = get_embedding_for_large_text
)[0]
    similarity_scores = []
    for text_chunk_embedding in embeddings_dict['embeddings']:
        similarity_scores.append(cosine_similarity([question_embedding], [text_chunk_embedding])[0][0])
    most_similar_index = np.argmax(similarity_scores)
    return embeddings_dict['text_chunks'][most_similar_index]

def generate_response(question, embeddings_dict):
    similar_text_chunk = get_most_similar_text_chunk(question, embeddings_dict)
    user_prompt = os.environ['USER_PROMPT'].format(content=similar_text_chunk, question=question)
    messages = [
        {"role": "system", "content": "You are a knowledgeable assistant."},
        {"role": "user", "content": user_prompt}
    ]
    try:
        response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
        assistant_reply = response['choices'][0]['message']['content']
        return assistant_reply
    except Exception as e:
        return str(e)
