import os

from flask import Flask, request, Response
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from db.db import db
from scheduler.scheduler import Scheduler
from util.logger import get_logger
from route.credential_list_routes import credential_list_blueprint
from route.user_routes import user_routes_blueprint
from route.scheduler_settings_routes import scheduler_settings_blueprint
from service.user_service import UserService
from model.response_model import ResponseModel
from repository.user_repository import UserRepository
from repository.email_repository import EmailRepository
from repository.pwned_platform_repository import PwnedPlatformRepository
from util.hibp_client import HibpClient
from util.email_sender import EmailSender

load_dotenv()
logger = get_logger(__name__)

def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    jwt = JWTManager(app)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config.update(
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(basedir, 'db', 'hibp.sqlite3')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    )
    if config:
        app.config.update(config)

    # Extensions
    logger.info("Initializing app with config")
    db.init_app(app)
    jwt.init_app(app)
    EmailSender().init_app(app)

    # Blueprints
    logger.info("Registering blueprint")
    app.register_blueprint(user_routes_blueprint)
    app.register_blueprint(credential_list_blueprint)
    app.register_blueprint(scheduler_settings_blueprint)

    with app.app_context():
        # Extensions.
        db.create_all()
        Scheduler().init_app(app)

        # Repositories
        UserRepository()
        EmailRepository()
        PwnedPlatformRepository()

        # Utilities
        HibpClient()


    @app.before_request
    def block_until_user_exists():
        is_users_empty: bool = UserRepository().is_table_empty()
        if request.endpoint == "create_dummy_user" and is_users_empty:
            return None

        if request.endpoint == "user_routes.register" and is_users_empty:
            return None

        if is_users_empty:
            return Response(
                response=str(ResponseModel(
                    success=False,
                    message="You have to create an account first!",
                    data=None,
                    error="",).model_dump()),
                status=401,
                mimetype="application/json")

        if request.endpoint == "user_routes.register" and not is_users_empty:
            return Response(
                response=str(ResponseModel(
                    success=False,
                    message="There is already a user.",
                    data=None,
                    error=""
                ).model_dump()),
                status=409,
                mimetype="application/json")

    @app.before_request
    def log_request_info():
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        logger.info(f"Request: {request.method} {request.path} from IP: {ip}")

    # Routes
    @app.get("/")
    def hello_world():
        return "<p>Hello World!</p>"

    @app.get("/<name>")
    def hello_name(name: str):
        return name

    @app.get("/create_dummy_user")
    def create_dummy_user():
        user_service = UserService()
        user_service.create_dummy_user()
        return {"message": "dummy user created"}

    @app.get("/get_dummy_user")
    def get_dummy_user():
        user_service = UserService()
        dum_user = user_service.get_dummy_user()
        return {"message": str(dum_user)}

    @app.get("/all_users")
    def get_all_users():
        user_service = UserService()
        all_users = user_service.get_all_users()
        print(type(all_users))
        return {"message": str(all_users)}

    return app


app = create_app()

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
