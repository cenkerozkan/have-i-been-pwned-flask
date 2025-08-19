from pydantic import ValidationError
from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from model.user_route_models import(
    CreateNewUserModel,
    UserCredentials
)

from model.response_model import ResponseModel
from service.user_service import UserService
from util.logger import get_logger

logger = get_logger(__name__)

user_routes_blueprint = Blueprint('user_routes', __name__)

@user_routes_blueprint.route('/user_routes/register', methods=['POST'])
def register() -> Response:
    try:
        new_user = CreateNewUserModel(**request.get_json())
        service = UserService()
        result: dict = service.create_user(new_user)
        return Response(
            response=str(ResponseModel(
                success=result.get("success"),
                message=result.get("message"),
                data=result.get("data"),
                error=result.get("error"),
            ).model_dump()),
            status=200,
            mimetype='application/json',
        )

    except ValidationError as e:
        return Response(
            response=str(ResponseModel(
                success=False,
                message="Wrong JSON Format!",
                data=None,
                error=str(e)
            ).model_dump()),
            status=422,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=str(ResponseModel(
                success=False,
                message="An unknown error occurred.",
                data=None,
                error=str(e)
            ).model_dump()),
            status=500,
            mimetype='application/json'
        )

@user_routes_blueprint.route('/user_routes/login', methods=['POST'])
def login() -> Response:
    try:
        user_credentials = UserCredentials(**request.get_json())
        service = UserService()
        result: dict = service.login(user_credentials)
        return Response(
            response=str(ResponseModel(
                success=result.get("success"),
                message=result.get("message"),
                data=result.get("data"),
                error=result.get("error"),
            )),
            status=200,
            mimetype='application/json',
        )

    except ValidationError as e:
        return Response(
            response=str(ResponseModel(
                success=False,
                message="Wrong JSON Format!",
                data=None,
                error=str(e)
            ).model_dump()),
            status=422,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=str(ResponseModel(
                success=False,
                message="An unknown error occurred.",
                data=None,
                error=str(e)
            ).model_dump()),
            status=500,
            mimetype='application/json'
        )