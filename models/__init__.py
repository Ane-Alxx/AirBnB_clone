#!/usr/bin/python3
"""this is the __init code that allows for a link to
the file storage"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()

#=-----user.py

#!/usr/bin/python3
"""this is the class that defines the user
email, password, first_name and last_name."""

from models.base_model import BaseModel


class User(BaseModel):
	"""this is like a user form

	Attributes to use:
		email (str): users email attri place holder
		password (str): users password attri place holder
		first_name (str): users first name attri place holder
		last_name (str): users last name attri place holder
	"""

	email = ""
	password = ""
	first_name = ""
	last_name = ""
