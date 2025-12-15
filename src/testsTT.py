from nutrition_app import NutritionApp
from db_manager import DBManager
from foodcentral_manager import FCManager
import food_item
from nutrition_analyzer import NutritionAnalyzer
from profile import Profile
import unittest

#theo
class testsTT(unittest.TestCase):
    def test_app_has_profile(self):
        app = NutritionApp()
        pro = Profile(1,1)
        app.profile = pro
        self.assertIs(pro, app.profile)

    def test_app_has_fc_db(self):
        app = NutritionApp()
        fc_db = FCManager()
        app.fc_db = fc_db
        self.assertIs(fc_db, app.fc_db)


    def test_app_has_analyzer(self):
        app = NutritionApp()
        analyzer = NutritionAnalyzer()
        app.analyzer = analyzer
        self.assertIs(analyzer, app.analyzer)

    def test_fc_db_inherit(self):
        fc_db = FCManager()
        self.assertTrue(callable(fc_db.prompt_key))
        self.assertTrue(callable(fc_db.get_item))
        
    def test_db_abstract(self):
        with self.assertRaises(TypeError):
            DBManager("asda", "adsdasd")
    

if __name__ == '__main__':
    unittest.main()
        