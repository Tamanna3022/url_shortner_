from flask import Flask, request, jsonify, redirect
import string
import random
import hashlib
app = Flask(__name__)

# In-memory database (for now)
url_mapping = {}

# Short domain
BASE_URL = "http://comp.ly/"

# Function to generate a short random code
def generate_hash_code(url, length=6):
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:length]


# Endpoint to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get("long_url")

    if not long_url:
        return jsonify({"error": "URL missing"}), 400

    # Generate unique short code
    while True:
        short_code = generate_hash_code()
        if short_code not in url_mapping:
            break

    url_mapping[short_code] = long_url
    short_url = BASE_URL + short_code

    return jsonify({"short_url": short_url})

# Endpoint to redirect from short to long URL
@app.route('/<short_code>')
def redirect_url(short_code):
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    else:
        return jsonify({"error": "Short URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
