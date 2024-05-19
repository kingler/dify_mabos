from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

T = TypeVar('T')

class RepositoryBase(ABC, Generic[T]):
    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def read(self, entity_id: str) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> None:
        pass

    @abstractmethod
    def list(self) -> List[T]:
        pass

    @abstractmethod
    def query(self, query: dict) -> List[T]:
        pass
