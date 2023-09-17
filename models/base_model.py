#!/usr/bin/python3
"""this is the code snippet for the base model class
think of the base model as the foundation of all our future classes"""
import models
from datetime import datetime
from uuid import uuid4


class BaseModel:
	"""this is the base model class for my airbnb clone project"""

	def __init__(self, *args, **kwargs):
		"""intialises a new base model

		Arguments to pass:
			self: place holder for self attr
			args: placeholder for args
			kwargs : placeholder for kwargs attr
		"""
		Time_thing = "%Y-%m-%dT%H:%M:%S.%f"
		self.id = str(uuid4())
		self.created_at = datetime.today()
		self.updated_at = datetime.today()
		if len(kwargs) != 0:
			for a, b in kwargs.items():
				if a == "created_at" or a == "updated_at":
					self.__dict__[a] = datetime.strptime(b, Time_thing)
				else:
					self.__dict__[a] = b
		else:
			models.storage.new(self)

	def save(self):
		"""this will update the time att to the current time"""
		self.updated_at = datetime.today()
		models.storage.save()

	def to_dict(self):
		"""here we return the dictionary containing all the keys
		and its values of __dict__ of the insta

		using self.__dict___ and __class___
		"""
		my_dictt = self.__dict__.copy()
		my_dictt["created_at"] = self.created_at.isoformat()
		my_dictt["updated_at"] = self.updated_at.isoformat()
		my_dictt["__class__"] = self.__class__.__name__
		return my_dictt

	def __str__(self):
		"""returns a string for the class name id and dict"""
		klass_name = self.__class__.__name__
		return "[{}] ({}) {}".format(klass_name, self.id, self.__dict__)
