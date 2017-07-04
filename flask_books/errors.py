import json
from flask import make_response, jsonify

class HTMLError():
    noBookName = "Please enter book name"
    noGenreName = "Please enter genre name"
    genreExists = "Genre already exist"
    notSignedIn = "Please sign in and try again"
