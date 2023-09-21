#!/usr/bin/python3
"""Module that tests file_storage.py"""
import unittest
from models.base_model import BaseModel
from models import storage
import os

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'fileStorage test not supported')
class test_fileStorage(unittest.TestCase):
    """class to test filestorage method"""

    def setUp(self):
        """filestorage testing setup"""
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """filestorage class testing teardown"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_obj_list_empty(self):
        """tests if objects is empty"""
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """tests if new method correctly added"""
        new = BaseModel()
        new.save()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """test all methods"""
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """tests model insta"""
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """test if data is saved to a file"""
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """tests the save method"""
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """test reload method"""
        new = BaseModel()
        new.save()
        storage.reload()
        loaded = None
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """tests reload from empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """tests the reload method with no existing file.json"""
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """tests BaseModel save method"""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """tests if __file_path is a str"""
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """tests if objects type is a dict"""
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """tests if key is the correct format"""
        new = BaseModel()
        new.save()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """tests FileStorage obj storage created"""
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)
