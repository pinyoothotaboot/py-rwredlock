from abc import ABC, abstractmethod


class BrokerInterface(ABC):

    @abstractmethod
    def set(self, id: str, value: str, expired: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def increase(self, id: str) -> int:
        pass

    @abstractmethod
    def decrease(self, id: str) -> int:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def publish(self, id: str, payload: str) -> bool:
        pass

    @abstractmethod
    def subscribe(self, id: str) -> str:
        pass
