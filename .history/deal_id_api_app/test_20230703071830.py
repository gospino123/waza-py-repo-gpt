Certainly! To refactor this script into an application that you can easily spin up on an EC2 instance, you need to modify the script a little bit. Below is a version of your script that has been refactored for running as an app on an EC2 instance:

```python
import os
import requests
import openai
import datetime
import numpy as np
import pickle
import socket
import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify

app = Flask(__name__)

os.environ['USER_PROMPT'] = 'Here is the info from the text: {content}. Based on this, what is the answer to "{question}"?'

# Use environment variable for API key
openai_api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = openai_api_key


# ... [Rest of the functions can remain the same] ...


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


@app.route('/refresh', methods=['GET'])
def refresh_data():
    global embeddings_dict
    url = 'https://www.rssground.com/services/rss-converter/64a0a74cd5ee7/RSS-Payload'
    response = requests.get(url)
    text = response.text
    file_name = create_file_name(url)

    with open(file_name, 'w') as file:
        file.write(text)
        extract_and_save_urls(text, file)

    embeddings = get_embedding_for_large_text(text)
    chunks = chunk_text(text)
    embeddings_file_name = create_file_name(url, extension='pkl')
    embeddings_dict[embeddings_file_name] = {'text_chunks': chunks, 'embeddings': embeddings}
    save_embeddings_to_file(embeddings_dict, embeddings_file_name)

    return jsonify({"message": "Daily data refreshed. Now browsing 75+ deal feeds."})


# Launch the Flask server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

This refactored version still includes all of the functionality of the original script, but it's organized as a Flask app that can be deployed on an EC2 instance.

Please ensure you have followed these steps:

1. Set the environment variable for your API key on the EC2 instance: `export OPENAI_API_KEY=your_api_key_here`.

2. Install the required packages: Flask, requests, openai, numpy, beautifulsoup4, scikit-learn.

3. Run the script on the EC2 instance with: `python script_name.py`.

4. Make sure your EC2 security group allows inbound traffic on port 5000.

Now, this Flask app will be accessible via the public IP address of your EC2 instance on port 5000. For example, you can use `http://EC2_IP_ADDRESS:5000/ask?question=your_question_here` to ask a question and `http://EC2_IP_ADDRESS:5000/refresh` to refresh the data.