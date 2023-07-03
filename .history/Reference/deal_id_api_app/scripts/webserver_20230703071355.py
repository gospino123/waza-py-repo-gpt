import os
import requests
import socket
import threading
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from .embeddings import get_embedding_for_large_text, create_file_name, generate_response, chunk_text

app = Flask(__name__)

def extract_and_save_urls(html_content, file):
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('a'):
        url = link.get('href')
        if url:
            file.write(url + '\n')

def save_embeddings_to_file(embeddings_dict, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(embeddings_dict, file)

def load_embeddings_from_file(file_name):
    with open(file_name, 'rb') as file:
        return pickle.load(file)

embeddings_dict = {}

@app.route('/ask', methods=['GET'])
def ask_question():
    question = request.args.get('question')
    if question:
        responses = []
        for embeddings_file_name in embeddings_dict.keys():
            response = generate_response(question, embeddings_dict[embeddings_file_name])
            responses.append(response)
        return jsonify(responses)
    return jsonify({"error": "No question provided"})

def run_web_api(port):
    app.run(port=port)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
