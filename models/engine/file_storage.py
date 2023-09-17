#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
	"""this here is the class that handles the serialization
	and deserilisation of the user

	Attributes to use:
	file path:
	objects:
	"""
	__file_path = "file.json"
	__objects = {}

	def all(self):
		"""this is the function for """
		return FileStorage.__objects

	def new(self, obj):
		"""this is the function for """
		obj_id = obj.__class__.__name__
		FileStorage.__objects["{}.{}".format(obj_id, obj.id)] = obj

	def save(self):
		"""this is the function for """
		p_dict = FileStorage.__objects
		obj_dict = {obj: p_dict[obj].to_dict() for obj in p_dict.keys()}
		with open(FileStorage.__file_path, "w") as files:
			json.dump(obj_dict, files)

	def reload(self):
		"""this is the function for"""
		try:
			with open(FileStorage.__file_path) as files:
				obj_dict = json.load(files)
				for a in obj_dict.values():
					klass_name = a["__class__"]
					del a["__class__"]
					self.new(eval(klass_name)(**a))
		except FileNotFoundError:
			return
