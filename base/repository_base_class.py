from abc import ABC, abstractmethod

class RepositoryBaseClass(ABC):

    @abstractmethod
    def insert_one(self, document):
        raise NotImplementedError

    @abstractmethod
    def insert_many(self, documents):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def update_one(self, document):
        raise NotImplementedError

    @abstractmethod
    def update_many(self, document):
        raise NotImplementedError