from decorators.singleton import singleton
from db.model.email import Email
from db.db import db
from base.repository_base_class import RepositoryBaseClass
from util.logger import get_logger


@singleton
class EmailRepository(RepositoryBaseClass):
    def __init__(self):
        self._logger = get_logger(self.__class__.__name__)
        self._logger.info("Creating email repository")

    def insert_one(self, email: Email) -> bool:
        try:
            db.session.add(email)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"email_repository.insert_one() falied: {e}")
            return False

    def insert_many(self, emails: list[Email]) -> bool:
        try:
            db.session.add_all(emails)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"email_repository.insert_many() falied: {e}")
            return False

    def get_all(self) -> list[Email]:
        return Email.query.all()

    def update_one(self, email: Email) -> bool:
        try:
            db.session.merge(email)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"email_repository.update_one() falied: {e}")
            return False

    def update_many(self, models: list[Email]) -> bool:
        try:
            for model in models:
                db.session.merge(model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"email_repository.update_many() falied: {e}")
            return False

    def delete_one(self, email: Email) -> bool:
        try:
            db.session.delete(email)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"email_repository.delete_one() falied: {e}")
            return False