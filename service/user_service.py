from logging import Logger

from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from exceptions.no_user_found_exception import NoUserFoundException
from model.user_route_models import (
    CreateNewUserModel,
    UserCredentials,
    ChangePasswordModel,
)
from repository.user_repository import UserRepository
from decorators.singleton import singleton
from db.model.user import User
from util.logger import get_logger


@singleton
class UserService:
    def __init__(self):
        self._db: UserRepository = UserRepository()
        self._logger: Logger = get_logger(self.__class__.__name__)

    def create_dummy_user(self):
        self._logger.info("Creating dummy user")
        dum_user = User(
            user_name="example", email="example@example.com", password="example"
        )
        self._db.insert_one(dum_user)
        self._logger.info("Created dummy user")

    def get_dummy_user(self):
        self._logger.info("Getting dummy user")
        dum_user = self._db.get_one_by_email(email="example@example.com")
        return dum_user

    def get_all_users(self):
        self._logger.info("Getting all users")
        all_users = self._db.get_all()
        return all_users

    def create_user(
        self,
        new_user_data: CreateNewUserModel,
    ) -> dict:
        result: dict = {"success": False, "message": "", "data": {}, "error": ""}
        """
        I am not assuming any user would provide a false email.
        So I am not planning to implement an email verification system
        for registration process.
        """
        new_user = User(**new_user_data.model_dump())
        try:
            is_created: bool = self._db.insert_one(new_user)
            if is_created:
                result["success"] = True
                result["message"] = "Successfully created user"

        except IntegrityError as e:
            result["success"] = False
            result["message"] = "User already exists"
            result["error"] = str(e)

        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to create user"
            result["error"] = str(e)

        return result

    def login(
        self,
        user_credentials: UserCredentials,
    ) -> dict:
        result: dict = {"success": False, "message": "", "data": {}, "error": ""}
        try:
            repository_result: User | None = self._db.get_one_by_email_and_password(
                **user_credentials.model_dump()
            )
            if repository_result:
                access_token = create_access_token(identity=repository_result.user_name)
                result["success"] = True
                result["message"] = "Successfully logged in"
                result["data"] = {"access_token": access_token}

        except NoUserFoundException as e:
            result["success"] = False
            result["message"] = "No user found with this credentials"
            result["error"] = str(e)

        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to login"
            result["error"] = str(e)

        return result

    def change_password(
        self,
        user_name: str,
        password_data: ChangePasswordModel,
    ) -> dict:
        result: dict = {"success": False, "message": "", "data": {}, "error": ""}
        try:
            # Get user by username
            user: User = self._db.get_one_by_username(user_name)

            # Update password
            user.password = password_data.password

            # Save changes
            is_updated: bool = self._db.update_one(user)

            if is_updated:
                result["success"] = True
                result["message"] = "Password successfully changed"
            else:
                result["success"] = False
                result["message"] = "Failed to change password"

        except NoUserFoundException as e:
            result["success"] = False
            result["message"] = "No user found with this username"
            result["error"] = str(e)

        except Exception as e:
            result["success"] = False
            result["message"] = "Failed to change password"
            result["error"] = str(e)

        return result
