#!/usr/bin/python3
<<<<<<< HEAD
"""This defines FileStorage class."""
=======
"""A module that defines class to manage file storage for hbnb clone"""
>>>>>>> e13e1676002a7f0a7df1b524e04c001ce483291b
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
<<<<<<< HEAD
    """Representing abstracted storage engine.

    Attributes:
        __file_path (str): Name of a file to save objects to.
        __objects (dict): The dictionary of the instantiated objects.
    """
=======
    """represent a storage engine for hbnb models"""
>>>>>>> e13e1676002a7f0a7df1b524e04c001ce483291b

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
<<<<<<< HEAD
        """Returning the dictionary of the instantiated objects in __objects.

        When the class is specified, returns the dictionary of the objects of that type.
        Otherwise, return the __objects dictionary.
        """
=======
        """return dict of instantiated objects in storage"""
>>>>>>> e13e1676002a7f0a7df1b524e04c001ce483291b
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}
            for k, v in self.__objects.items():
                if type(v) == cls:
                    cls_dict[k] = v
            return cls_dict
        return self.__objects

    def new(self, obj):
<<<<<<< HEAD
        """Sets in __objects obj with the key <obj_class_name>.id."""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """This serializes __objects to a JSON file __file_path."""
=======
        """adds new object to a storage dict"""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """saves storage dict to file"""
>>>>>>> e13e1676002a7f0a7df1b524e04c001ce483291b
        odict = {o: self.__objects[o].to_dict() for o in self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(odict, f)

    def reload(self):
<<<<<<< HEAD
        """This deserializes a JSON file __file_path to __objects, if it does exist."""
=======
        """deserialize JSON file if it exists"""
>>>>>>> e13e1676002a7f0a7df1b524e04c001ce483291b
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for o in json.load(f).values():
                    name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(name)(**o))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
<<<<<<< HEAD
        """Deleting the given object from __objects, if it does exists."""
=======
        """delete given obj from __objects, if it exists"""
>>>>>>> e13e1676002a7f0a7df1b524e04c001ce483291b
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
<<<<<<< HEAD
        """Calling a reload method."""
=======
        """Call the reload method"""
>>>>>>> e13e1676002a7f0a7df1b524e04c001ce483291b
        self.reload()
