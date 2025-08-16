from decorators.sinlgeton import singleton
from repository.user_repository import UserRepository
from util.logger import get_logger


@singleton
class EmailRepository:
    def __init__(self):
        self._logger = get_logger(self.__class__.__name__)
        self._logger.info("Creating email repository")