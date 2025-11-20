from db_manager import DBManager

from foodcentral_manager import FCManager

class invalid_test_db(DBManager):

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

#uncomment line below to test invalid subclass
#bad_idea = invalid_test_db("asdaadsdsa.com", "errrrr", "kyucxz")


#working fc test
fc_db = FCManager("DEMO_KEY")
print(repr(fc_db))
print(fc_db.get_item(534358))


