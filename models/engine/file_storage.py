#!/usr/bin/python3
"""This defines FileStorage class."""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Representing abstracted storage engine.

    Attributes:
        __file_path (str): Name of a file to save objects to.
        __objects (dict): The dictionary of the instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returning the dictionary of the instantiated objects in __objects.

        When the class is specified, returns the dictionary of the objects of that type.
        Otherwise, return the __objects dictionary.
        """
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
        """Sets in __objects obj with the key <obj_class_name>.id."""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """This serializes __objects to a JSON file __file_path."""
        odict = {o: self.__objects[o].to_dict() for o in self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(odict, f)

    def reload(self):
        """This deserializes a JSON file __file_path to __objects, if it does exist."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for o in json.load(f).values():
                    name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(name)(**o))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deleting the given object from __objects, if it does exists."""
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """Calling a reload method."""
        self.reload()
