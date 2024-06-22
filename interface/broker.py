from abc import ABC, abstractmethod 

class Broker(ABC):

    @abstractmethod
    def set(id : str , expired : int) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def get(id : str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def increase(id : str) -> int:
        pass

    @abstractmethod
    def decrease(id : str) -> int:
        pass
    
    @abstractmethod
    def delete(id : str) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def publish(id : str , payload : str):
        pass

    @abstractmethod
    def subscribe(id : str) -> str:
        pass
    

