from abc import ABC, abstractmethod

class ExtensionHandler(ABC):
    
    @abstractmethod
    def handle(self, character, wfm):
        pass
