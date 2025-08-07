from db.db import db
from base.repository_base_class import RepositoryBaseClass
from db.custom_data_model.hibp_breached_account_model import HibpBreachedAccountModel

class PwnedPlatformRepository(RepositoryBaseClass):
    def insert_one(self, model) -> bool:
        pass

    def insert_many(self, models) -> bool:
        pass

    def get_all(self) -> list[HibpBreachedAccountModel]:
        pass

    def update_one(self, model) -> bool:
        pass

    def update_many(self, models):
        return super().update_many(models)