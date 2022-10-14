"""

"""
"""

"""

from flask import Flask, render_template, request, redirect, Response, jsonify, abort
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'zDG65udTa7qt'

def predict_tracks(track):
	post_dict = {
		"track":track
	}
	post_json = json.dumps(post_dict)
	http = 'https://lucky-essence-360209.an.r.appspot.com'
	response = requests.post(http+'/predict?'+track, json=post_json)

	return response

@app.route('/')
def root():
    return Response("Hello")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
	# app.run(host='0.0.0.0', port=5000, debug=True)

