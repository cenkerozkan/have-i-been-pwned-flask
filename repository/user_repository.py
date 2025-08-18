from db.db import db
from db.model import User
from base.repository_base_class import RepositoryBaseClass
from decorators.sinlgeton import singleton
from util.logger import get_logger


@singleton
class UserRepository(RepositoryBaseClass):
    def __init__(self):
        self._logger = get_logger(__name__)
        self._logger.info("Creating user repository")

    def is_table_empty(self):
        return db.session.query(User.id).first() is None

    def insert_one(self, model: User) -> bool:
        try:
            db.session.add(model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"user_repository.insert_one failed: {e}")
            return False

    def insert_many(self, models: list[User]) -> bool:
        try:
            db.session.add_all(models)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"user_repository.insert_many failed: {e}")
            return False

    def get_one_by_email(self, email: str) -> User | None:
        try:
            user = db.session.query(User).filter(User.email == email).first()
            print(type(user))
            return user
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"user_repository.get_one_by_id failed: {e}")
            return None

    def get_all(self) -> list[User]:
        users = User.query.all()
        return users

    def update_one(self, model: User) -> bool:
        try:
            db.session.merge(model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"user_repository.update_one failed: {e}")
            return False

    def update_many(self, models: list[User]) -> bool:
        try:
            for model in models:
                db.session.merge(model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"user_repository.update_many failed: {e}")
            return False

    def delete_one(self, model: User) -> bool:
        try:
            db.session.delete(model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"user_repository.delete_one failed: {e}")
            return False