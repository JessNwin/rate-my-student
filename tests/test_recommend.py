import pytest
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
 
import unittest
 
#from app import app, db
 
from app.models import Recommendation
 
class TestRecommendation(unittest.TestCase):
#test data
 
    def test_new_recommendation(self):
        professor_id = 'gandulamaster'
        student_id = 'Vin'
        description = 'cool'
# creating an instance to test
        new_recommendation = Recommendation(professor_id=professor_id, student_id=student_id, description=description)
 
        self.assertEqual(new_recommendation.professor_id, professor_id)
        self.assertEqual(new_recommendation.student_id, student_id)
        self.assertEqual(new_recommendation.description, description)
 
if __name__ == '__main__':
    unittest.main()