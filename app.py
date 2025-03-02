from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video_link', methods=['GET'])
def get_video_link():
    api_key = request.args.get('api_key')
    file_id = request.args.get('file_id')

    if not api_key or not file_id:
        return jsonify({'success': False, 'error': 'API key and file ID are required.'})

    # Make the API call to Streamtape
    api_url = f'https://streamtape.com/api/v1/get_video_link?api_key={api_key}&file_id={file_id}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if data['success']:
            return jsonify({'success': True, 'result': data['result']})
        else:
            return jsonify({'success': False, 'error': data['error']})
    else:
        return jsonify({'success': False, 'error': 'Failed to fetch data from Streamtape API.'})

if __name__ == '__main__':
    app.run(debug=True)
