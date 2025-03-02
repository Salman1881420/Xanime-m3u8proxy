from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask app is running!"

@app.route('/get_video', methods=['GET'])
def get_video():
    video_url = request.args.get('url')  # Get the StreamTape video URL from the query string
    
    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    # StreamTape API URL to get direct video stream
    streamtape_api_url = f"https://api.streamtape.com/get_video?url={video_url}"
    
    # Make a GET request to StreamTape API
    response = requests.get(streamtape_api_url)
    
    # Handle API response
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            # Return the direct video URL or the file link for player
            return jsonify({"video_url": data['file']})
        else:
            return jsonify({"error": "Unable to fetch video."}), 400
    else:
        return jsonify({"error": "Failed to contact StreamTape API."}), 500

if __name__ == '__main__':
    app.run(debug=True)
