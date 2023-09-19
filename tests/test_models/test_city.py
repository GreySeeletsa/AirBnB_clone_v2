#!/usr/bin/python3
"""unnittests for city.py."""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestCity(unittest.TestCase):
    """unittests for testing City class"""

    @classmethod
    def setUpClass(cls):
        """city tests setup
        creates filestorage, dbstorage, city and state instances for testing
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """City testing teardown
        del filestorage, dbStorage, city state test instances
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.state
        del cls.city
        del cls.filestorage
        if type(models.storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_pep8(self):
        """tests the pep8 styling"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/city.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """tests for the docstrings"""
        self.assertIsNotNone(City.__doc__)

    def test_attributes(self):
        """tests for the attr"""
        ct = City()
        self.assertEqual(str, type(ct.id))
        self.assertEqual(datetime, type(ct.created_at))
        self.assertEqual(datetime, type(ct.updated_at))
        self.assertTrue(hasattr(ct, "__tablename__"))
        self.assertTrue(hasattr(ct, "name"))
        self.assertTrue(hasattr(ct, "state_id"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_nullable_attributes(self):
        """tests if relevant dbStorage attr are non-nullable"""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(City(
                state_id=self.state.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(City(name="San Jose"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_state_relationship_deletes(self):
        """tests del cascade in City-State relationship"""
        st = State(name="Georgia")
        self.dbstorage._DBStorage__session.add(st)
        self.dbstorage._DBStorage__session.commit()
        ct = City(name="Atlanta", state_id=st.id)
        self.dbstorage._DBStorage__session.add(ct)
        self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.delete(st)
        self.dbstorage._DBStorage__session.commit()
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM cities WHERE BINARY name = 'Atlanta'")
        query = cursor.fetchall()
        cursor.close()
        self.assertEqual(0, len(query))

    def test_is_subclass(self):
        """tests if City is a subclass of BaseModel"""
        self.assertTrue(issubclass(City, BaseModel))

    def test_init(self):
        """test the initialization"""
        self.assertIsInstance(self.city, City)

    def test_two_models_are_unique(self):
        """test if diff city instances are unique"""
        ct = City()
        self.assertNotEqual(self.city.id, ct.id)
        self.assertLess(self.city.created_at, ct.created_at)
        self.assertLess(self.city.updated_at, ct.updated_at)

    def test_init_args_kwargs(self):
        """test the initialization with args/kwargs"""
        dt = datetime.utcnow()
        ct = City("1", id="5", created_at=dt.isoformat())
        self.assertEqual(ct.id, "5")
        self.assertEqual(ct.created_at, dt)

    def test_str(self):
        """test string representation"""
        s = self.city.__str__()
        self.assertIn("[City] ({})".format(self.city.id), s)
        self.assertIn("'id': '{}'".format(self.city.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.city.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.city.updated_at)), s)
        self.assertIn("'name': '{}'".format(self.city.name), s)
        self.assertIn("'state_id': '{}'".format(self.city.state_id), s)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_save_filestorage(self):
        """test the save method with filestorage"""
        old = self.city.updated_at
        self.city.save()
        self.assertLess(old, self.city.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("City." + self.city.id, f.read())

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save_dbstorage(self):
        """test the save method with dbstorage"""
        old = self.city.updated_at
        self.state.save()
        self.city.save()
        self.assertLess(old, self.city.updated_at)
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * \
                          FROM `cities` \
                         WHERE BINARY name = '{}'".
                       format(self.city.name))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.city.id, query[0][0])
        cursor.close()

    def test_to_dict(self):
        """test the to_dict method"""
        city_dict = self.city.to_dict()
        self.assertEqual(dict, type(city_dict))
        self.assertEqual(self.city.id, city_dict["id"])
        self.assertEqual("City", city_dict["__class__"])
        self.assertEqual(self.city.created_at.isoformat(),
                         city_dict["created_at"])
        self.assertEqual(self.city.updated_at.isoformat(),
                         city_dict["updated_at"])
        self.assertEqual(self.city.name, city_dict["name"])
        self.assertEqual(self.city.state_id, city_dict["state_id"])


if __name__ == "__main__":
    unittest.main()
