#!/usr/bin/python3
"""this is the place class"""
from models.base_model import BaseModel


class Place(BaseModel):
	"""Represent a place.

	Attributes to use:
		city_id (str): initially empty, placeholder for city name
		user_id (str): initially empty, placeholder for
		name (str): initially empty, placeholder for
		description (str): initially empty, placeholder for
		number_rooms (int): initially empty, placeholder for
		number_bathrooms (int): initially 0, placeholder for
		max_guest (int): initially 0, placeholder for
		price_by_night (int): initially 0, placeholder for
		latitude (float): initially 0.0, placeholder for
		longitude (float): initially 0.0, placeholder for
		amenity_ids (list):initially empty, placeholder for
	"""

	city_id = ""
	user_id = ""
	name = ""
	description = ""
	number_rooms = 0
	number_bathrooms = 0
	max_guest = 0
	price_by_night = 0
	latitude = 0.0
	longitude = 0.0
	amenity_ids = []
