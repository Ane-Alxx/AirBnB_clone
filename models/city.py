#!/usr/bin/python3
"""this is the class for the city details."""
from models.base_model import BaseModel


class City(BaseModel):
	"""this is the city class

	Attributes to use:
		state_id (str): This is the placeholder for the state
		the city is found in
		name (str): This is the one for the city name
	"""

	state_id = ""
	name = ""
