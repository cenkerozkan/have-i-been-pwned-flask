from flask import Blueprint, request, Response
from pydantic import ValidationError
from flask_jwt_extended import jwt_required
from service.scheduler_settings_service import SchedulerSettingsService
from model.response_model import ResponseModel
from model.scheduler_setting_route_models import SchedulerSettingsModel
from typing import Dict, Any

scheduler_settings_blueprint = Blueprint("scheduler_settings", __name__, url_prefix="/api/scheduler")
settings_service = SchedulerSettingsService()

@scheduler_settings_blueprint.route("/settings", methods=["GET"])
@jwt_required()
def get_settings() -> Response:
    result: Dict[str, Any] = settings_service.get_pwn_check_settings()
    
    return Response(
        response=ResponseModel(
            success=result["success"],
            message=result["message"],
            data=result["data"],
            error=result["error"]
        ).model_dump(),
        status=200 if result["success"] else 400,
        mimetype="application/json"
    )
    
@scheduler_settings_blueprint.route("/status", methods=["GET"])
@jwt_required()
def get_status() -> Response:
    result: Dict[str, Any] = settings_service.get_scheduler_status()
    
    return Response(
        response=ResponseModel(
            success=result["success"],
            message=result["message"],
            data=result["data"],
            error=result["error"]
        ).model_dump(),
        status=200 if result["success"] else 400,
        mimetype="application/json"
    )
    
@scheduler_settings_blueprint.route("/settings", methods=["PUT"])
@jwt_required()
def update_settings() -> Response:
    try:
        new_settings = SchedulerSettingsModel(**request.get_json())
        
        result: Dict[str, Any] = settings_service.update_pwn_check_settings(
            interval_unit=new_settings.interval_unit,
            interval_value=new_settings.interval_value
        )
        
        return Response(
            response=ResponseModel(
                success=result["success"],
                message=result["message"],
                data=result["data"],
                error=result["error"]
            ).model_dump(),
            status=200 if result["success"] else 400,
            mimetype="application/json"
        )
            
    except ValidationError as e:
        return Response(
            response=ResponseModel(
                success=False,
                message="Wrong JSON Format!",
                data=None,
                error=str(e)
            ).model_dump(),
            status=422,
            mimetype="application/json"
        )
        
    except Exception as e:
        return Response(
            response=ResponseModel(
                success=False,
                message="An unknown error occurred.",
                data=None,
                error=str(e)
            ).model_dump(),
            status=500,
            mimetype="application/json"
        )