#!/usr/bin/python3
"""This defines the unnittests for the models/place.py."""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestPlace(unittest.TestCase):
    """The unittests for the testing of the Place class."""

    @classmethod
    def setUpClass(cls):
        """The place testing setup.

        Temporary renames any of the existing file.json.
        Reseting the FileStorage objects dictionary.
        Creating the FileStorage, DBStorage and the Place instances for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)
        cls.user = User(email="poppy@holberton.com", password="betty98")
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                          name="Betty")
        cls.review = Review(text="stellar", place_id=cls.place.id,
                            user_id=cls.user.id)
        cls.amenity = Amenity(name="water", place=cls.place.id)
        cls.filestorage = FileStorage()

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """The Place testing teardown.

        Restores the original file.json.
        Deletes the test instances.
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
        del cls.user
        del cls.place
        del cls.review
        del cls.amenity
        del cls.filestorage
        if type(models.storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_pep8(self):
        """Tests the pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/place.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Checks for the docstrings."""
        self.assertIsNotNone(Place.__doc__)

    def test_attributes(self):
        """Checks for the attributes."""
        us = Place()
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertTrue(hasattr(us, "__tablename__"))
        self.assertTrue(hasattr(us, "city_id"))
        self.assertTrue(hasattr(us, "name"))
        self.assertTrue(hasattr(us, "description"))
        self.assertTrue(hasattr(us, "number_rooms"))
        self.assertTrue(hasattr(us, "number_bathrooms"))
        self.assertTrue(hasattr(us, "max_guest"))
        self.assertTrue(hasattr(us, "price_by_night"))
        self.assertTrue(hasattr(us, "latitude"))
        self.assertTrue(hasattr(us, "longitude"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Tests the FileStorage")
    def test_nullable_attributes(self):
        """Testing whether the email attribute is non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Place(user_id=self.user.id,
                                                         name="Betty"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Place(city_id=self.city.id,
                                                         name="Betty"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Place(city_id=self.city.id,
                                                         user_id=self.user.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Tests the DBStorage")
    def test_reviews_filestorage(self):
        """Tests the reviews attribute."""
        key = "{}.{}".format(type(self.review).__name__, self.review.id)
        self.filestorage._FileStorage__objects[key] = self.review
        reviews = self.place.reviews
        self.assertTrue(list, type(reviews))
        self.assertIn(self.review, reviews)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Tests the DBStorage")
    def test_amenities(self):
        """Testing the amenities of attribute."""
        key = "{}.{}".format(type(self.amenity).__name__, self.amenity.id)
        self.filestorage._FileStorage__objects[key] = self.amenity
        self.place.amenities = self.amenity
        amenities = self.place.amenities
        self.assertTrue(list, type(amenities))
        self.assertIn(self.amenity, amenities)

    def test_is_subclass(self):
        """Checking if the Place is the subclass of the BaseModel."""
        self.assertTrue(issubclass(Place, BaseModel))

    def test_init(self):
        """Tests the initialization."""
        self.assertIsInstance(self.place, Place)

    def test_two_models_are_unique(self):
        """Testing whether the different Place instances are unique."""
        us = Place()
        self.assertNotEqual(self.place.id, us.id)
        self.assertLess(self.place.created_at, us.created_at)
        self.assertLess(self.place.updated_at, us.updated_at)

    def test_init_args_kwargs(self):
        """Tests the initialization with args and the kwargs."""
        dt = datetime.utcnow()
        st = Place("1", id="5", created_at=dt.isoformat())
        self.assertEqual(st.id, "5")
        self.assertEqual(st.created_at, dt)

    def test_str(self):
        """Tests the __str__ representation."""
        s = self.place.__str__()
        self.assertIn("[Place] ({})".format(self.place.id), s)
        self.assertIn("'id': '{}'".format(self.place.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.place.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.place.updated_at)), s)
        self.assertIn("'city_id': '{}'".format(self.place.city_id), s)
        self.assertIn("'user_id': '{}'".format(self.place.user_id), s)
        self.assertIn("'name': '{}'".format(self.place.name), s)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Tests the DBStorage")
    def test_save_filestorage(self):
        """Testing and save method with FileStorage."""
        old = self.place.updated_at
        self.place.save()
        self.assertLess(old, self.place.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Place." + self.place.id, f.read())

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Tests the FileStorage")
    def test_save_dbstorage(self):
        """Testing and save method with the DBStorage."""
        old = self.place.updated_at
        self.state.save()
        self.city.save()
        self.user.save()
        self.place.save()
        self.assertLess(old, self.place.updated_at)
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * \
                          FROM `places` \
                         WHERE BINARY name = '{}'".
                       format(self.place.name))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.place.id, query[0][0])
        cursor.close()

    def test_to_dict(self):
        """Testing the to_dict method."""
        place_dict = self.place.to_dict()
        self.assertEqual(dict, type(place_dict))
        self.assertEqual(self.place.id, place_dict["id"])
        self.assertEqual("Place", place_dict["__class__"])
        self.assertEqual(self.place.created_at.isoformat(),
                         place_dict["created_at"])
        self.assertEqual(self.place.updated_at.isoformat(),
                         place_dict["updated_at"])
        self.assertEqual(self.place.city_id, place_dict["city_id"])
        self.assertEqual(self.place.user_id, place_dict["user_id"])
        self.assertEqual(self.place.name, place_dict["name"])


if __name__ == "__main__":
    unittest.main()
