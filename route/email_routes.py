"""
Email Routes Module

This module implements RESTful API endpoints for email management.
The routes intentionally use empty path strings with the base URL prefix '/api/email'
following RESTful conventions:

- GET /api/email    - Retrieve all emails (collection)
- POST /api/email   - Create a new email (add to collection)
- DELETE /api/email - Delete all emails (clear collection)

This approach follows REST principles where:
1. The resource name is in the URL prefix
2. HTTP methods determine the action (GET, POST, DELETE)
3. Operations apply to the entire resource collection
"""

from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required
from pydantic import ValidationError

from model.response_model import ResponseModel
from model.email_service_models import NewEmailModel
from service.email_service import EmailService
from util.logger import get_logger
from typing import Dict, Any

logger = get_logger(__name__)

email_routes_blueprint = Blueprint("email_routes", __name__, url_prefix="/api/email")
email_service = EmailService()


@email_routes_blueprint.route("", methods=["GET"])
@jwt_required()
def get_all_emails() -> Response:
    logger.info("GET /api/email - Getting all emails")
    try:
        result: Dict[str, Any] = email_service.get_all_emails()

        return Response(
            response=str(
                ResponseModel(
                    success=result.get("success"),
                    message=result.get("message"),
                    data=result.get("data"),
                    error=result.get("error"),
                ).model_dump()
            ),
            status=200,
            mimetype="application/json",
        )

    except Exception as e:
        return Response(
            response=str(
                ResponseModel(
                    success=False,
                    message="An unknown error occurred.",
                    data=None,
                    error=str(e),
                ).model_dump()
            ),
            status=500,
            mimetype="application/json",
        )


@email_routes_blueprint.route("", methods=["DELETE"])
@jwt_required()
def delete_all_emails() -> Response:
    logger.info("DELETE /api/email - Deleting all emails")
    try:
        result: Dict[str, Any] = email_service.delete_all_emails()

        return Response(
            response=str(
                ResponseModel(
                    success=result.get("success"),
                    message=result.get("message"),
                    data=result.get("data"),
                    error=result.get("error"),
                ).model_dump()
            ),
            status=200 if result.get("success") else 400,
            mimetype="application/json",
        )

    except Exception as e:
        return Response(
            response=str(
                ResponseModel(
                    success=False,
                    message="An unknown error occurred.",
                    data=None,
                    error=str(e),
                ).model_dump()
            ),
            status=500,
            mimetype="application/json",
        )


@email_routes_blueprint.route("", methods=["POST"])
@jwt_required()
def create_email() -> Response:
    logger.info("POST /api/email - Creating new email")
    try:
        new_email = NewEmailModel(**request.get_json())
        result: Dict[str, Any] = email_service.create_email(new_email)

        return Response(
            response=str(
                ResponseModel(
                    success=result.get("success"),
                    message=result.get("message"),
                    data=result.get("data"),
                    error=result.get("error"),
                ).model_dump()
            ),
            status=200 if result.get("success") else 400,
            mimetype="application/json",
        )

    except ValidationError as e:
        return Response(
            response=str(
                ResponseModel(
                    success=False, message="Wrong JSON Format!", data=None, error=str(e)
                ).model_dump()
            ),
            status=422,
            mimetype="application/json",
        )

    except Exception as e:
        return Response(
            response=str(
                ResponseModel(
                    success=False,
                    message="An unknown error occurred.",
                    data=None,
                    error=str(e),
                ).model_dump()
            ),
            status=500,
            mimetype="application/json",
        )
