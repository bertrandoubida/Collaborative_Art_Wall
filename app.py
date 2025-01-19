import os
import random
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask, render_template, request, jsonify
from momento import CacheClient, Configurations, CredentialProvider
from momento.responses import CacheGet, CacheSet


load_dotenv()
app = Flask(__name__)

api_key = os.getenv("MOMENTO_API_KEY")
if not api_key:
    raise ValueError("Momento API key not found")

cache_client = CacheClient(
    Configurations.Laptop.v1(),
    CredentialProvider.from_string(api_key),
    default_ttl=timedelta(seconds=21600)
)
CACHE_NAME = os.getenv('cache_name')
if not CACHE_NAME:
    raise ValueError("Cache name not found dude")

KEY_LIST = "key_list"

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/add-message', methods=['POST'])
def add_message():
    """Endpoint to add a new message."""
    data = request.json
    message = data.get('message')

    if not message:
        return jsonify({'error': 'Message is required!'}), 400

    message_id = f"message-{random.randint(1000, 9999)}"

    # Store the message in the cache
    response = cache_client.set(CACHE_NAME, message_id, message)
    if isinstance(response, CacheSet.Success):
        key_list_response = cache_client.get(CACHE_NAME, KEY_LIST)
        keys = []

        match key_list_response:
            case CacheGet.Hit() as hit:
                keys = hit.value_string.split(",")
            case CacheGet.Miss():
                keys = []
            case CacheGet.Error() as error:
                return jsonify({'error': f"An error occurred: {error.message}"}), 500

        keys.append(message_id)
        cache_client.set(CACHE_NAME, KEY_LIST, ",".join(keys))

        return jsonify({'message': 'Message added successfully!'})
    else:
        return jsonify({'error': 'Failed to add message!'}), 500


@app.route('/get-messages', methods=['GET'])
def get_messages():
    """Endpoint to retrieve all messages."""
    # Fetch the list of keys from the cache
    key_list_response = cache_client.get(CACHE_NAME, KEY_LIST)
    keys = []

    match key_list_response:
        case CacheGet.Hit() as hit:
            keys = hit.value_string.split(",")
        case CacheGet.Miss():
            keys = []
        case CacheGet.Error() as error:
            return jsonify({'error': f"An error occurred: {error.message}"}), 500

    messages = []
    for key in keys:
        message_response = cache_client.get(CACHE_NAME, key)
        match message_response:
            case CacheGet.Hit() as hit:
                messages.append(hit.value_string)
            case CacheGet.Miss():
                continue
            case CacheGet.Error() as error:
                return jsonify({'error': f"An error occurred: {error.message}"}), 500

    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)