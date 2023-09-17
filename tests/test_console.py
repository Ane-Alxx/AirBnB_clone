#!/usr/bin/python3
"""testing the console"""
import os
import sys
import unittest
from console import HBNBCommand
from io import StringIO
from models import storage
from models.engine.file_storage import FileStorage
from unittest.mock import patch
from models import BaseModel

class test_prompt(unittest.TestCase):
	"""testing prompts"""

	def test_str_prompt(self):
		self.assertEqual("(hbnb) ", HBNBCommand.prompt)

	def test_null_lines(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(""))
			self.assertEqual("", t_out.getvalue().strip())


class test_help(unittest.TestCase):
	"""testinh help and help related"""

	def test_help_quit(self):
		holder = "Quit test_cmd to exit the program."
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("help quit"))
			self.assertEqual(holder, t_out.getvalue().strip())

	def test_help_create(self):
		holder = ("Usage: create <class>\n        "
			 "Create a new class instance and print its id.")
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("help create"))
			self.assertEqual(holder, t_out.getvalue().strip())

	def test_help_EOF(self):
		holder = "EOF signal to exit the program."
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("help EOF"))
			self.assertEqual(holder, t_out.getvalue().strip())

	def test_help_show(self):
		holder = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
			 "Display the string representation of a class instance of"
			 " a given id.")
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("help show"))
			self.assertEqual(holder, t_out.getvalue().strip())

	def test_help_destroy(self):
		holder = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
			 "Delete a class instance of a given id.")
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("help destroy"))
			self.assertEqual(holder, t_out.getvalue().strip())

	def test_help_all(self):
		holder = ("Usage: all or all <class> or <class>.all()\n        "
			 "Display string representations of all instances of a given class"
			 ".\n        If no class is specified, displays all instantiated "
			 "objects.")
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("help all"))
			self.assertEqual(holder, t_out.getvalue().strip())

	def test_help_count(self):
		holder = ("Usage: count <class> or <class>.count()\n        "
			 "Retrieve the number of instances of a given class.")
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("help count"))
			self.assertEqual(holder, t_out.getvalue().strip())

	def test_help_update(self):
		holder = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
			 "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
			 ">) or\n       <class>.update(<id>, <dictionary>)\n        "
			 "Update a class instance of a given id by adding or updating\n   "
			 "     a given attribute key/value pair or dictionary.")
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("help update"))
			self.assertEqual(holder, t_out.getvalue().strip())

	def test_help(self):
		holder = ("Documented commands (type help <topic>):\n"
			 "========================================\n"
			 "EOF  all  count  create  destroy  help  quit  show  update")
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("help"))
			self.assertEqual(holder, t_out.getvalue().strip())


class test_exit(unittest.TestCase):
	"""testing exit func"""

	def test_quit_exits(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertTrue(HBNBCommand().onecmd("quit"))

	def test_EOF_exits(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertTrue(HBNBCommand().onecmd("EOF"))


class test_create(unittest.TestCase):
	"""test create"""

	@classmethod
	def opon(self):
		try:
			os.rename("file.json", "tmp")
		except IOError:
			pass
		FileStorage.__objects = {}

	@classmethod
	def dwn(self):
		try:
			os.remove("file.json")
		except IOError:
			pass
		try:
			os.rename("tmp", "file.json")
		except IOError:
			pass

	def test_create1(self):
		messg = "** class name missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_create2(self):
		messg = "** class doesn't exist **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create MyModel"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_create3(self):
		messg = "*** Unknown syntax: MyModel.create()"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		messg = "*** Unknown syntax: BaseModel.create()"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_create4(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			self.assertLess(0, len(t_out.getvalue().strip()))
			test_with = "BaseModel.{}".format(t_out.getvalue().strip())
			self.assertIn(test_with, storage.all().keys())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create User"))
			self.assertLess(0, len(t_out.getvalue().strip()))
			test_with = "User.{}".format(t_out.getvalue().strip())
			self.assertIn(test_with, storage.all().keys())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create State"))
			self.assertLess(0, len(t_out.getvalue().strip()))
			test_with = "State.{}".format(t_out.getvalue().strip())
			self.assertIn(test_with, storage.all().keys())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create City"))
			self.assertLess(0, len(t_out.getvalue().strip()))
			test_with = "City.{}".format(t_out.getvalue().strip())
			self.assertIn(test_with, storage.all().keys())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			self.assertLess(0, len(t_out.getvalue().strip()))
			test_with = "Amenity.{}".format(t_out.getvalue().strip())
			self.assertIn(test_with, storage.all().keys())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			self.assertLess(0, len(t_out.getvalue().strip()))
			test_with = "Place.{}".format(t_out.getvalue().strip())
			self.assertIn(test_with, storage.all().keys())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Review"))
			self.assertLess(0, len(t_out.getvalue().strip()))
			test_with = "Review.{}".format(t_out.getvalue().strip())
			self.assertIn(test_with, storage.all().keys())


class test_show(unittest.TestCase):
	"""test show"""

	@classmethod
	def opon(self):
		try:
			os.rename("file.json", "tmp")
		except IOError:
			pass
		FileStorage.__objects = {}

	@classmethod
	def dwn(self):
		try:
			os.remove("file.json")
		except IOError:
			pass
		try:
			os.rename("tmp", "file.json")
		except IOError:
			pass

	def test_show1(self):
		messg = "** class name missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(".show()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_show2(self):
		messg = "** class doesn't exist **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show MyModel"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_show3(self):
		messg = "** instance id missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show User"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show State"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show City"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show Amenity"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show Place"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show Review"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_show4(self):
		messg = "** instance id missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("User.show()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("State.show()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("City.show()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Place.show()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Review.show()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_show5(self):
		messg = "** no instance found **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show User 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show State 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show City 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show Place 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("show Review 1"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_show6(self):
		messg = "** no instance found **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_show7(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["BaseModel.{}".format(test_key)]
			test_cmd = "show BaseModel {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create User"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["User.{}".format(test_key)]
			test_cmd = "show User {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create State"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["State.{}".format(test_key)]
			test_cmd = "show State {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Place.{}".format(test_key)]
			test_cmd = "show Place {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create City"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["City.{}".format(test_key)]
			test_cmd = "show City {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Amenity.{}".format(test_key)]
			test_cmd = "show Amenity {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Review"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Review.{}".format(test_key)]
			test_cmd = "show Review {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())

	def test_show8(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["BaseModel.{}".format(test_key)]
			test_cmd = "BaseModel.show({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create User"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["User.{}".format(test_key)]
			test_cmd = "User.show({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create State"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["State.{}".format(test_key)]
			test_cmd = "State.show({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Place.{}".format(test_key)]
			test_cmd = "Place.show({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create City"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["City.{}".format(test_key)]
			test_cmd = "City.show({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Amenity.{}".format(test_key)]
			test_cmd = "Amenity.show({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Review"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Review.{}".format(test_key)]
			test_cmd = "Review.show({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertEqual(obj.__str__(), t_out.getvalue().strip())


class test_destroy(unittest.TestCase):
	"""testing destroy"""

	@classmethod
	def opon(self):
		try:
			os.rename("file.json", "tmp")
		except IOError:
			pass
		FileStorage.__objects = {}

	@classmethod
	def dwn(self):
		try:
			os.remove("file.json")
		except IOError:
			pass
		try:
			os.rename("tmp", "file.json")
		except IOError:
			pass
		storage.reload()

	def test_destroy1(self):
		messg = "** class name missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(".destroy()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_destroy2(self):
		messg = "** class doesn't exist **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_destroy3(self):
		messg = "** instance id missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy User"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy State"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy City"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy Place"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy Review"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_destroy4(self):
		messg = "** instance id missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_destroy5(self):
		messg = "** no instance found **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_destroy6(self):
		messg = "** no instance found **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_destroy7(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["BaseModel.{}".format(test_key)]
			test_cmd = "destroy BaseModel {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create User"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["User.{}".format(test_key)]
			test_cmd = "show User {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create State"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["State.{}".format(test_key)]
			test_cmd = "show State {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Place.{}".format(test_key)]
			test_cmd = "show Place {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create City"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["City.{}".format(test_key)]
			test_cmd = "show City {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Amenity.{}".format(test_key)]
			test_cmd = "show Amenity {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Review"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Review.{}".format(test_key)]
			test_cmd = "show Review {}".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())

	def test_destroy8(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["BaseModel.{}".format(test_key)]
			test_cmd = "BaseModel.destroy({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create User"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["User.{}".format(test_key)]
			test_cmd = "User.destroy({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create State"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["State.{}".format(test_key)]
			test_cmd = "State.destroy({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Place.{}".format(test_key)]
			test_cmd = "Place.destroy({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create City"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["City.{}".format(test_key)]
			test_cmd = "City.destroy({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Amenity.{}".format(test_key)]
			test_cmd = "Amenity.destroy({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Review"))
			test_key = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			obj = storage.all()["Review.{}".format(test_key)]
			test_cmd = "Review.destory({})".format(test_key)
			self.assertFalse(HBNBCommand().onecmd(test_cmd))
			self.assertNotIn(obj, storage.all())


class test_all(unittest.TestCase):
	"""testing all"""

	@classmethod
	def opon(self):
		try:
			os.rename("file.json", "tmp")
		except IOError:
			pass
		FileStorage.__objects = {}

	@classmethod
	def dwn(self):
		try:
			os.remove("file.json")
		except IOError:
			pass
		try:
			os.rename("tmp", "file.json")
		except IOError:
			pass

	def test_all1(self):
		messg = "** class doesn't exist **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("all MyModel"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_all2(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			self.assertFalse(HBNBCommand().onecmd("create User"))
			self.assertFalse(HBNBCommand().onecmd("create State"))
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			self.assertFalse(HBNBCommand().onecmd("create City"))
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			self.assertFalse(HBNBCommand().onecmd("create Review"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("all"))
			self.assertIn("BaseModel", t_out.getvalue().strip())
			self.assertIn("User", t_out.getvalue().strip())
			self.assertIn("State", t_out.getvalue().strip())
			self.assertIn("Place", t_out.getvalue().strip())
			self.assertIn("City", t_out.getvalue().strip())
			self.assertIn("Amenity", t_out.getvalue().strip())
			self.assertIn("Review", t_out.getvalue().strip())

	def test_all3(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			self.assertFalse(HBNBCommand().onecmd("create User"))
			self.assertFalse(HBNBCommand().onecmd("create State"))
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			self.assertFalse(HBNBCommand().onecmd("create City"))
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			self.assertFalse(HBNBCommand().onecmd("create Review"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(".all()"))
			self.assertIn("BaseModel", t_out.getvalue().strip())
			self.assertIn("User", t_out.getvalue().strip())
			self.assertIn("State", t_out.getvalue().strip())
			self.assertIn("Place", t_out.getvalue().strip())
			self.assertIn("City", t_out.getvalue().strip())
			self.assertIn("Amenity", t_out.getvalue().strip())
			self.assertIn("Review", t_out.getvalue().strip())

	def test_all4(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			self.assertFalse(HBNBCommand().onecmd("create User"))
			self.assertFalse(HBNBCommand().onecmd("create State"))
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			self.assertFalse(HBNBCommand().onecmd("create City"))
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			self.assertFalse(HBNBCommand().onecmd("create Review"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
			self.assertIn("BaseModel", t_out.getvalue().strip())
			self.assertNotIn("User", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("all User"))
			self.assertIn("User", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("all State"))
			self.assertIn("State", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("all City"))
			self.assertIn("City", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("all Amenity"))
			self.assertIn("Amenity", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("all Place"))
			self.assertIn("Place", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("all Review"))
			self.assertIn("Review", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())

	def test_all5(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			self.assertFalse(HBNBCommand().onecmd("create User"))
			self.assertFalse(HBNBCommand().onecmd("create State"))
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			self.assertFalse(HBNBCommand().onecmd("create City"))
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			self.assertFalse(HBNBCommand().onecmd("create Review"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
			self.assertIn("BaseModel", t_out.getvalue().strip())
			self.assertNotIn("User", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("User.all()"))
			self.assertIn("User", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("State.all()"))
			self.assertIn("State", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("City.all()"))
			self.assertIn("City", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
			self.assertIn("Amenity", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Place.all()"))
			self.assertIn("Place", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Review.all()"))
			self.assertIn("Review", t_out.getvalue().strip())
			self.assertNotIn("BaseModel", t_out.getvalue().strip())


class test_update(unittest.TestCase):
	"""testing update"""

	@classmethod
	def opon(self):
		try:
			os.rename("file.json", "tmp")
		except IOError:
			pass
		FileStorage.__objects = {}

	@classmethod
	def dwn(self):
		try:
			os.remove("file.json")
		except IOError:
			pass
		try:
			os.rename("tmp", "file.json")
		except IOError:
			pass

	def test_update1(self):
		messg = "** class name missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(".update()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_update2(self):
		messg = "** class doesn't exist **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update MyModel"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_update3(self):
		messg = "** instance id missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update User"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update State"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update City"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update Amenity"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update Place"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update Review"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_update4(self):
		messg = "** instance id missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("User.update()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("State.update()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("City.update()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Place.update()"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Review.update()"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_update5(self):
		messg = "** no instance found **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update User 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update State 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update City 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update Place 1"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("update Review 1"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_update6(self):
		messg = "** no instance found **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_update7(self):
		messg = "** attribute name missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			test_id = t_out.getvalue().strip()
			test_comm = "update BaseModel {}".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create User"))
			test_id = t_out.getvalue().strip()
			test_comm = "update User {}".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create State"))
			test_id = t_out.getvalue().strip()
			test_comm = "update State {}".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create City"))
			test_id = t_out.getvalue().strip()
			test_comm = "update City {}".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			test_id = t_out.getvalue().strip()
			test_comm = "update Amenity {}".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			test_id = t_out.getvalue().strip()
			test_comm = "update Place {}".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_update8(self):
		messg = "** attribute name missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
			test_id = t_out.getvalue().strip()
			test_comm = "BaseModel.update({})".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create User"))
			test_id = t_out.getvalue().strip()
			test_comm = "User.update({})".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create State"))
			test_id = t_out.getvalue().strip()
			test_comm = "State.update({})".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create City"))
			test_id = t_out.getvalue().strip()
			test_comm = "City.update({})".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
			test_id = t_out.getvalue().strip()
			test_comm = "Amenity.update({})".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Place"))
			test_id = t_out.getvalue().strip()
			test_comm = "Place.update({})".format(test_id)
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_update9(self):
		messg = "** value missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create BaseModel")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "update BaseModel {} attr_name".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create User")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "update User {} attr_name".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create State")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "update State {} attr_name".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create City")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "update City {} attr_name".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Amenity")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "update Amenity {} attr_name".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "update Place {} attr_name".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Review")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "update Review {} attr_name".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_update10(self):
		messg = "** value missing **"
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create BaseModel")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "BaseModel.update({}, attr_name)".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create User")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "User.update({}, attr_name)".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create State")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "State.update({}, attr_name)".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create City")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "City.update({}, attr_name)".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Amenity")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "Amenity.update({}, attr_name)".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "Place.update({}, attr_name)".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Review")
			test_id = t_out.getvalue().strip()
		with patch("sys.stdout", new=StringIO()) as t_out:
			test_comm = "Review.update({}, attr_name)".format(test_id)
			self.assertFalse(HBNBCommand().onecmd(test_comm))
			self.assertEqual(messg, t_out.getvalue().strip())

	def test_update11(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create BaseModel")
			test_id = t_out.getvalue().strip()
		test_comm = "update BaseModel {} attr_name 'attr_value'".format(test_id)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["BaseModel.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create User")
			test_id = t_out.getvalue().strip()
		test_comm = "update User {} attr_name 'attr_value'".format(test_id)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["User.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create State")
			test_id = t_out.getvalue().strip()
		test_comm = "update State {} attr_name 'attr_value'".format(test_id)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["State.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create City")
			test_id = t_out.getvalue().strip()
		test_comm = "update City {} attr_name 'attr_value'".format(test_id)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["City.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		test_comm = "update Place {} attr_name 'attr_value'".format(test_id)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["Place.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Amenity")
			test_id = t_out.getvalue().strip()
		test_comm = "update Amenity {} attr_name 'attr_value'".format(test_id)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["Amenity.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Review")
			test_id = t_out.getvalue().strip()
		test_comm = "update Review {} attr_name 'attr_value'".format(test_id)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["Review.{}".format(test_id)].__dict__
		self.assertTrue("attr_value", test_dict["attr_name"])

	def test_update12(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create BaseModel")
			test_dtifier = t_out.getvalue().strip()
		test_comm = "BaseModel.update({}, attr_name, 'attr_value')".format(test_dtifier)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["BaseModel.{}".format(test_dtifier)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create User")
			test_dtifier = t_out.getvalue().strip()
		test_comm = "User.update({}, attr_name, 'attr_value')".format(test_dtifier)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["User.{}".format(test_dtifier)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create State")
			test_dtifier = t_out.getvalue().strip()
		test_comm = "State.update({}, attr_name, 'attr_value')".format(test_dtifier)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["State.{}".format(test_dtifier)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create City")
			test_dtifier = t_out.getvalue().strip()
		test_comm = "City.update({}, attr_name, 'attr_value')".format(test_dtifier)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["City.{}".format(test_dtifier)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_dtifier = t_out.getvalue().strip()
		test_comm = "Place.update({}, attr_name, 'attr_value')".format(test_dtifier)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["Place.{}".format(test_dtifier)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Amenity")
			test_dtifier = t_out.getvalue().strip()
		test_comm = "Amenity.update({}, attr_name, 'attr_value')".format(test_dtifier)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["Amenity.{}".format(test_dtifier)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Review")
			test_dtifier = t_out.getvalue().strip()
		test_comm = "Review.update({}, attr_name, 'attr_value')".format(test_dtifier)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["Review.{}".format(test_dtifier)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

	def test_update_valid_int_attr_space_notation(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		test_comm = "update Place {} max_guest 98".format(test_id)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["Place.{}".format(test_id)].__dict__
		self.assertEqual(98, test_dict["max_guest"])

	def test_update13(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_dtifier = t_out.getvalue().strip()
		test_comm = "Place.update({}, max_guest, 98)".format(test_dtifier)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["Place.{}".format(test_dtifier)].__dict__
		self.assertEqual(98, test_dict["max_guest"])

	def test_update14(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		test_comm = "update Place {} latitude 7.2".format(test_id)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["Place.{}".format(test_id)].__dict__
		self.assertEqual(7.2, test_dict["latitude"])

	def test_update15(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_dtifier = t_out.getvalue().strip()
		test_comm = "Place.update({}, latitude, 7.2)".format(test_dtifier)
		self.assertFalse(HBNBCommand().onecmd(test_comm))
		test_dict = storage.all()["Place.{}".format(test_dtifier)].__dict__
		self.assertEqual(7.2, test_dict["latitude"])

	def test_update16(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create BaseModel")
			test_id = t_out.getvalue().strip()
		test_comm = "update BaseModel {} ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'}"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["BaseModel.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create User")
			test_id = t_out.getvalue().strip()
		test_comm = "update User {} ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'}"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["User.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create State")
			test_id = t_out.getvalue().strip()
		test_comm = "update State {} ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'}"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["State.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create City")
			test_id = t_out.getvalue().strip()
		test_comm = "update City {} ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'}"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["City.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		test_comm = "update Place {} ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'}"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["Place.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Amenity")
			test_id = t_out.getvalue().strip()
		test_comm = "update Amenity {} ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'}"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["Amenity.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Review")
			test_id = t_out.getvalue().strip()
		test_comm = "update Review {} ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'}"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["Review.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

	def test_update17(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create BaseModel")
			test_id = t_out.getvalue().strip()
		test_comm = "BaseModel.update({}".format(test_id)
		test_comm += "{'attr_name': 'attr_value'})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["BaseModel.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create User")
			test_id = t_out.getvalue().strip()
		test_comm = "User.update({}, ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["User.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create State")
			test_id = t_out.getvalue().strip()
		test_comm = "State.update({}, ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["State.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create City")
			test_id = t_out.getvalue().strip()
		test_comm = "City.update({}, ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["City.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		test_comm = "Place.update({}, ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["Place.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Amenity")
			test_id = t_out.getvalue().strip()
		test_comm = "Amenity.update({}, ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["Amenity.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Review")
			test_id = t_out.getvalue().strip()
		test_comm = "Review.update({}, ".format(test_id)
		test_comm += "{'attr_name': 'attr_value'})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["Review.{}".format(test_id)].__dict__
		self.assertEqual("attr_value", test_dict["attr_name"])

	def test_update_valid_dictionary_with_int_space_notation(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		test_comm = "update Place {} ".format(test_id)
		test_comm += "{'max_guest': 98})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["Place.{}".format(test_id)].__dict__
		self.assertEqual(98, test_dict["max_guest"])

	def test_update18(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		test_comm = "Place.update({}, ".format(test_id)
		test_comm += "{'max_guest': 98})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["Place.{}".format(test_id)].__dict__
		self.assertEqual(98, test_dict["max_guest"])

	def test_update19(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		test_comm = "update Place {} ".format(test_id)
		test_comm += "{'latitude': 9.8})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["Place.{}".format(test_id)].__dict__
		self.assertEqual(9.8, test_dict["latitude"])

	def test_update20(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			HBNBCommand().onecmd("create Place")
			test_id = t_out.getvalue().strip()
		test_comm = "Place.update({}, ".format(test_id)
		test_comm += "{'latitude': 9.8})"
		HBNBCommand().onecmd(test_comm)
		test_dict = storage.all()["Place.{}".format(test_id)].__dict__
		self.assertEqual(9.8, test_dict["latitude"])


class test_count(unittest.TestCase):
	"""testing count"""

	@classmethod
	def opon(self):
		try:
			os.rename("file.json", "tmp")
		except IOError:
			pass
		FileStorage._FileStorage__objects = {}

	@classmethod
	def dwn(self):
		try:
			os.remove("file.json")
		except IOError:
			pass
		try:
			os.rename("tmp", "file.json")
		except IOError:
			pass

	def test_count1(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
			self.assertEqual("0", t_out.getvalue().strip())

	def test_count2(self):
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
			self.assertEqual("1", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create User"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("User.count()"))
			self.assertEqual("1", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create State"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("State.count()"))
			self.assertEqual("1", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Place"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Place.count()"))
			self.assertEqual("1", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create City"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("City.count()"))
			self.assertEqual("1", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Amenity"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
			self.assertEqual("1", t_out.getvalue().strip())
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("create Review"))
		with patch("sys.stdout", new=StringIO()) as t_out:
			self.assertFalse(HBNBCommand().onecmd("Review.count()"))
			self.assertEqual("1", t_out.getvalue().strip())


if __name__ == "__main__":
	unittest.main()
