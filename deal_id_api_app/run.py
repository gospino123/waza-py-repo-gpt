import threading
from scripts.webserver import run_web_api, is_port_in_use, embeddings_dict, save_embeddings_to_file, load_embeddings_from_file, create_file_name
from scripts.embeddings import get_embedding_for_large_text, chunk_text

api_thread = None

while True:
    user_input = input("Enter URL or question or 'deal-id up' or 'deal-id down' (or 'exit' to quit): ")

    if user_input.lower() == 'exit':
        break
    elif user_input.lower() == 'deal-id up':
        if api_thread is None or not api_thread.is_alive():
            port = 5000
            while is_port_in_use(port):
                port = int(input(f"Port {port} is in use. Please enter a different port: "))
            api_thread = threading.Thread(target=run_web_api, args=(port,))
            api_thread.daemon = True
            api_thread.start()
