from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video', methods=['POST'])
def get_video():
    # Retrieve the API key and file ID from the form
    api_key = request.form.get('api_key')
    file_id = request.form.get('file_id')
    
    # Check if both API key and file ID are provided
    if not api_key or not file_id:
        return jsonify({"error": "API Key and File ID are required"}), 400

    # Construct the URL to get the direct link to the file
    streamtape_api_url = f"https://api.streamtape.com/get_video?api_key={api_key}&file_id={file_id}"

    # Make the API request to Streamtape
    response = requests.get(streamtape_api_url)

    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok' and 'file' in data:
            # If the response is successful, return the direct video URL
            return jsonify({"video_url": data['file']})
        else:
            return jsonify({"error": "Failed to retrieve video."}), 400
    else:
        return jsonify({"error": "Failed to contact Streamtape API."}), 500

if __name__ == '__main__':
    app.run(debug=True)
