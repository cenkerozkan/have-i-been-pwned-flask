"""
PwnedPlatform Routes Module

This module implements RESTful API endpoints for pwned platform management.
The routes intentionally use empty path strings with the base URL prefix '/api/pwned-platforms'
following RESTful conventions:

- GET /api/pwned-platforms     - Retrieve all pwned platforms (collection)
- DELETE /api/pwned-platforms  - Delete all pwned platforms (clear collection)

Since data is added to the pwned platform table via tasks, users cannot add
pwned platforms voluntarily; they can only view them or delete them all.
"""

from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required

from model.response_model import ResponseModel
from service.pwned_platform_service import PwnedPlatformService
from util.logger import get_logger
from typing import Dict, Any

logger = get_logger(__name__)

pwned_platform_routes_blueprint = Blueprint(
    "pwned_platform_routes", __name__, url_prefix="/api/pwned_platforms"
)
pwned_platform_service = PwnedPlatformService()


@pwned_platform_routes_blueprint.route("", methods=["GET"])
@jwt_required()
def get_all_pwned_platforms() -> Response:
    """Get all pwned platforms"""
    logger.info("GET /api/pwned-platforms - Getting all pwned platforms")
    try:
        result: Dict[str, Any] = pwned_platform_service.get_all_pwned_platforms()

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


@pwned_platform_routes_blueprint.route("", methods=["DELETE"])
@jwt_required()
def delete_all_pwned_platforms() -> Response:
    """Delete all pwned platforms"""
    logger.info("DELETE /api/pwned-platforms - Deleting all pwned platforms")
    try:
        result: Dict[str, Any] = pwned_platform_service.delete_all_pwned_platforms()

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


@pwned_platform_routes_blueprint.route("/email/<int:email_id>", methods=["GET"])
@jwt_required()
def get_by_email_id(email_id: int) -> Response:
    """Get pwned platforms by email ID"""
    logger.info(
        f"GET /api/pwned-platforms/email/{email_id} - Getting pwned platforms for email"
    )
    try:
        result: Dict[str, Any] = pwned_platform_service.get_by_email_id(email_id)

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
