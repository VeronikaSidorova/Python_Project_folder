from abc import ABC, abstractmethod

class JobAPI(ABC):

    @abstractmethod
    def connect(self):
        pass