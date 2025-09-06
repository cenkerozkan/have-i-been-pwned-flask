from decorators.singleton import singleton
from util.logger import get_logger
from db.db import db
from db.model.pwned_platform import PwnedPlatform
from base.repository_base_class import RepositoryBaseClass

@singleton
class PwnedPlatformRepository(RepositoryBaseClass):
    def __init__(self):
        self._logger = get_logger(self.__class__.__name__)
        self._logger.info("Creating pwned platform repository")

    def insert_one(self, model) -> bool:
        try:
            db.session.add(model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"pwned_platform_repository.insert_one failed: {e}")
            return False

    def insert_many(self, models: list[PwnedPlatform]) -> bool:
        try:
            for model in models:
                db.session.add(model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"pwned_platform_repository.insert_many failed: {e}")
            return False

    def get_all(self) -> list[PwnedPlatform]:
        return PwnedPlatform.query.all()

    def update_one(self, model) -> bool:
        try:
            db.session.merge(model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"pwned_platform_repository.update_one failed: {e}")
            return False

    def update_many(self, models):
        try:
            for model in models:
                db.session.merge(model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"pwned_platform_repository.update_many failed: {e}")
            return False

    def delete_one(self, model) -> bool:
        try:
            db.session.delete(model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self._logger.exception(f"pwned_platform_repository.delete_one failed: {e}")
            return False