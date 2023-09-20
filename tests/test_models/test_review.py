#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.review import Review
import os


class test_review(test_basemodel):
    """ reviews the test class"""

    def __init__(self, *args, **kwargs):
        """ reviews the class init"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """ tests the review place_id attr"""
        new = self.value()
        self.assertEqual(type(new.place_id), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_user_id(self):
        """ tests the review user_id attr"""
        new = self.value()
        self.assertEqual(type(new.user_id), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_text(self):
        """ tests the review text attr"""
        new = self.value()
        self.assertEqual(type(new.text), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
