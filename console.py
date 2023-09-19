#!/usr/bin/python3
"""this defines the class for our console"""
import cmd
import re
import json
import os
import sys
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
	cb_rep = re.search(r"\{(.*?)\}", arg)
	braces = re.search(r"\[(.*?)\]", arg)
	if cb_rep is None:
		if braces is None:
			return [a.strip(",") for a in split(arg)]
		else:
			lex_con = split(arg[:braces.span()[0]])
			cont = [a.strip(",") for a in lex_con]
			cont.append(braces.group())
			return cont
	else:
		lex_con = split(arg[:cb_rep.span()[0]])
		cont = [a.strip(",") for a in lex_con]
		cont.append(cb_rep.group())
		return cont


class HBNBCommand(cmd.Cmd):
	"""this is the hbnb commabd

	Attributes to use:
	--
	--
	"""

	prompt = "(hbnb) "
	__classes = {
		"BaseModel": BaseModel,
		"User": User,
		"State": State,
		"City": City,
		"Place": Place,
		"Amenity": Amenity,
		"Review": Review
	}

	def emptyline(self):
		"""this is the function for """
		pass

	def default(self, arg):
		"""this is the function for """
		argu_repo = {
			"all": self.do_all,
			"show": self.do_show,
			"destroy": self.do_destroy,
			"counter": self.do_count,
			"update": self.do_update
		}
		fix_m = re.search(r"\.", arg)
		if fix_m is not None:
			argl = [arg[:fix_m.span()[0]], arg[fix_m.span()[1]:]]
			fix_m = re.search(r"\((.*?)\)", argl[1])
			if fix_m is not None:
				command = [argl[1][:fix_m.span()[0]], fix_m.group()[1:-1]]
				if command[0] in argu_repo.keys():
					func_call = "{} {}".format(argl[0], command[1])
					return argu_repo[command[0]](func_call)
		print("*** Unknown syntax: {}".format(arg))
		return False

	def do_quit(self, arg):
		"""this is the function for quit"""
		return True

	def do_EOF(self, arg):
		"""this is the function for end of file"""
		print("")
		return True

	def do_create(self, arg):
		"""this is the function for
		"""
		argl = parse(arg)
		if len(argl) == 0:
			print("** class name missing **")
		elif argl[0] not in HBNBCommand.__classes:
			print("** class doesn't exist **")
		else:
			print(eval(argl[0])().id)
			storage.save()

	def do_show(self, arg):
		"""this is the function for"""
		argl = parse(arg)
		obj_dict = storage.all()
		if len(argl) == 0:
			print("** class name missing **")
		elif argl[0] not in HBNBCommand.__classes:
			print("** class doesn't exist **")
		elif len(argl) == 1:
			print("** instance id missing **")
		elif "{}.{}".format(argl[0], argl[1]) not in obj_dict:
			print("** no instance found **")
		else:
			print(obj_dict["{}.{}".format(argl[0], argl[1])])

	def do_destroy(self, arg):
		"""this is the function for"""
		argl = parse(arg)
		obj_dict = storage.all()
		if len(argl) == 0:
			print("** class name missing **")
		elif argl[0] not in HBNBCommand.__classes:
			print("** class doesn't exist **")
		elif len(argl) == 1:
			print("** instance id missing **")
		elif "{}.{}".format(argl[0], argl[1]) not in obj_dict.keys():
			print("** no instance found **")
		else:
			del obj_dict["{}.{}".format(argl[0], argl[1])]
			storage.save()

	def do_all(self, arg):
		"""this is the function for"""
		argl = parse(arg)
		if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
			print("** class doesn't exist **")
		else:
			objl = []
			for obj in storage.all().values():
				if len(argl) > 0 and argl[0] == obj.__class__.__name__:
					objl.append(obj.__str__())
				elif len(argl) == 0:
					objl.append(obj.__str__())
			print(objl)

	def do_count(self, arg):
		"""this is the function for"""
		argl = parse(arg)
		counter = 0
		for obj in storage.all().values():
			if argl[0] == obj.__class__.__name__:
				counter += 1
		print(counter)

	def do_update(self, arg):
		"""this is the function for"""
		argl = parse(arg)
		obj_dict = storage.all()

		if len(argl) == 0:
			print("** class name missing **")
			return False
		if argl[0] not in HBNBCommand.__classes:
			print("** class doesn't exist **")
			return False
		if len(argl) == 1:
			print("** instance id missing **")
			return False
		if "{}.{}".format(argl[0], argl[1]) not in obj_dict.keys():
			print("** no instance found **")
			return False
		if len(argl) == 2:
			print("** attribute name missing **")
			return False
		if len(argl) == 3:
			try:
				type(eval(argl[2])) != dict
			except NameError:
				print("** value missing **")
				return False

		if len(argl) == 4:
			obj = obj_dict["{}.{}".format(argl[0], argl[1])]
			if argl[2] in obj.__class__.__dict__.keys():
				valtype = type(obj.__class__.__dict__[argl[2]])
				obj.__dict__[argl[2]] = valtype(argl[3])
			else:
				obj.__dict__[argl[2]] = argl[3]
		elif type(eval(argl[2])) == dict:
			obj = obj_dict["{}.{}".format(argl[0], argl[1])]
			for a, b in eval(argl[2]).items():
				if (a in obj.__class__.__dict__.keys() and
						type(obj.__class__.__dict__[a]) in {str, int, float}):
					valtype = type(obj.__class__.__dict__[a])
					obj.__dict__[a] = valtype(b)
				else:
					obj.__dict__[a] = b
		storage.save()


if __name__ == '__main__':
	HBNBCommand().cmdloop()
