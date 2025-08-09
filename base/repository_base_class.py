from abc import ABC, abstractmethod

class RepositoryBaseClass(ABC):

    @abstractmethod
    def insert_one(self, model):
        raise NotImplementedError

    @abstractmethod
    def insert_many(self, models):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def update_one(self, model):
        raise NotImplementedError

    @abstractmethod
    def update_many(self, models):
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, model):
        raise NotImplementedError