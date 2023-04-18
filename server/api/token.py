from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify

token = Blueprint('token', __name__)

@token.route("/token", methods=["POST"])
def create_token():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)