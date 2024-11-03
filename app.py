from flask import Flask, jsonify, request
import requests
import redis
import os
from requests.exceptions import RequestException
from redis.exceptions import ConnectionError

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)
api_key = "jHig4Qhb20449rpquO9IrA==4BodWrg6EZSyg75O" 

@app.route("/define/<word>", methods=["GET"])
def get_definition(word):
    if not word.isalpha():
        return jsonify({"error": "Invalid word format. Only alphabetic characters are allowed."}), 400

    try:
        cached_definition = r.get(word)
        if cached_definition:
            return jsonify({"word": word, "definition": cached_definition.decode("utf-8")})
    except ConnectionError:
        pass
    
    try:
        headers = {"X-Api-Key": api_key}
        response = requests.get(f"https://api.api-ninjas.com/v1/dictionary?word={word}", headers=headers, timeout=5)
        response.raise_for_status()
        if response.status_code == 200:
            definition = response.json().get("definition", "Definition not found")
            r.setex(word, 300, definition)
            return jsonify({"word": word, "definition": definition})
    except RequestException as e:
        return jsonify({"error": "Failed to reach the dictionary API", "details": str(e)}), 502

    return jsonify({"error": "Definition not found"}), 404

@app.route("/random_word", methods=["GET"])
def get_random_word():
    word_type = request.args.get("type")  
    limit = request.args.get("limit", 1)  

    try:
        headers = {"X-Api-Key": api_key}
        params = {"type": word_type, "limit": limit}
        response = requests.get("https://api.api-ninjas.com/v1/randomword", headers=headers, params=params, timeout=5)
        response.raise_for_status()
        if response.status_code == 200:
            word = response.json().get("word", "Random word not found")
            return jsonify({"word": word})
    except RequestException as e:
        return jsonify({"error": "Failed to reach the random word API", "details": str(e)}), 502

    return jsonify({"error": "Random word not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

