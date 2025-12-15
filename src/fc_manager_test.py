from db_manager import DBManager

from foodcentral_manager import FCManager
import unittest

class invalid_test_db(DBManager):
    """do not use. Only to demonstate absrract class enforcement"""
    def __init__(self, url, key, default_key):
        super().__init__(url, key, default_key)
    
    def __repr__(self) -> str:
        return f"invalid database manager {self.url}"

    # def get_item(self):
    #     return "test"

    @property
    def key(self):
        return self._key
    
    @key.setter
    def key(self,key):
        self.__key = key

class testsTT(unittest.TestCase): 
    def test_invalid_db(self):
        with self.assertRaises(TypeError):
            invalid_test_db("asdsa","asdsad"," gdadgadsg")

    def test_fc_db(self):
        fc_db = FCManager()
        self.assertIsInstance(fc_db, DBManager)

    
if __name__ == '__main__':
    unittest.main()
