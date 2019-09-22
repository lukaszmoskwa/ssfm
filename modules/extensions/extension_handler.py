from abc import ABC, abstractmethod

class ExtensionHandler(ABC):
    
    options = []

    @abstractmethod
    def handle(self, character, wfm):
        pass


    def get_options(self):
        return self.options
