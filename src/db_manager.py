# Database_Manager
from abc import ABC, abstractmethod

class DBManager(ABC):
    """
    Base class for all external database managers.
    Primarily manages GET calls to APIs
    Requires: requests library
    """

    def __init__(self, url, key, default_key):
        self._url = url
        self._key = key
        self._default_key = default_key 

    
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @property
    def url(self):
        return self._url
    
    @property
    def key(self):
        return self._key
    
    @property
    def default_key(self):
        return self._default_key

    @key.setter
    @abstractmethod
    def key(self, key):
        pass
    
    @abstractmethod
    def get_item(self):
        pass


    def prompt_key(self) -> str:
        """Prompts user for api key or returns default key"""
        test_key = input("Enter API key (Press enter to use default): ")
        if test_key !="":
            return test_key
        else:
            return self.default_key

#tests
#fc_db = db_manager.foodcentral()
#print(repr(fc_db))

#print(fc_db.url)
#print(fc_db.get_food_item(534358))

