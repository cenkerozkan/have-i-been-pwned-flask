from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

user_routes_blueprint = Blueprint('user_routes', __name__)

@user_routes_blueprint.route('/simple_test', methods=['GET'])
def simple_test():
    pass

@user_routes_blueprint.route('/register', methods=['POST'])
def register():
    pass