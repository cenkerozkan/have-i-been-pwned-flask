from logging import Logger

from repository.user_repository import UserRepository
from decorators.sinlgeton import singleton
from db.db_models.user import User
from util.logger import get_logger

@singleton
class UserService:
    def __init__(self):
        self._db: UserRepository = UserRepository()
        self._logger: Logger = get_logger(self.__class__.__name__)

    def create_dummy_user(self):
        self._logger.info("Creating dummy user")
        dum_user = User(email="<EMAIL>", password="<PASSWORD>")
        self._db.insert_one(dum_user)
        self._logger.info("Created dummy user")

    def create_user(
            self
    ) -> bool:
        new_user = User()