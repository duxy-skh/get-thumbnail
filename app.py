from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/get_thumbnail', methods=['POST'])
def get_thumbnail():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        # Get User ID from Username
        url = 'https://users.roblox.com/v1/usernames/users'
        payload = {
            "usernames": [username],
            "excludeBannedUsers": False
        }

        user_response = requests.post(url, json=payload)
        user_data = user_response.json()

        if user_data.get("data") and len(user_data["data"]) > 0:
            user_id = user_data["data"][0]['id']

            # Get User Thumbnail from User ID
            thumbnail_response = requests.get(
                f'https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=150x150&format=Png&isCircular=false'
            )
            thumbnail_data = thumbnail_response.json()

            if 'data' in thumbnail_data and len(thumbnail_data['data']) > 0:
                image_url = thumbnail_data['data'][0]['imageUrl']
                return jsonify({'thumbnailUrl': image_url})

        return jsonify({'error': 'Username not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
