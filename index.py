!pip install flask requests
from flask import Flask, jsonify, request
import requests
import re

app = Flask(__name__)

API_KEY = "0ccdf679d84ea59f72b1"

def extract_file_id(url):
    """Extract the file ID from a given StreamTape URL"""
    match = re.search(r'https://streamtape.com/v/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None

def get_streamtape_link(file_id):
    """Fetches a fresh direct link for the StreamTape file."""
    url = f"https://api.streamtape.com/file/dlticket?file={file_id}&key={API_KEY}"
    response = requests.get(url).json()

    if response["status"] == 200:
        ticket = response["result"]["ticket"]
        direct_link = f"https://api.streamtape.com/file/dl?file={file_id}&ticket={ticket}"
        return direct_link
    return None

@app.route('/get_video', methods=['GET'])
def get_video():
    """Returns a fresh StreamTape link based on the URL parameter."""
    streamtape_url = request.args.get('url')
    if not streamtape_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    
    file_id = extract_file_id(streamtape_url)
    if not file_id:
        return jsonify({"error": "Invalid StreamTape URL"}), 400

    link = get_streamtape_link(file_id)
    if link:
        return jsonify({"stream_link": link})
    return jsonify({"error": "Failed to get link"}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')  # Run on all IP addresses of the device
