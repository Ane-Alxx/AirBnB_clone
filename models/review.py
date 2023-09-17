#!/usr/bin/python3
"""this is the review class"""
from models.base_model import BaseModel


class Review(BaseModel):
	"""this is the class to for a customer 
	review form ish thingy

	Attributes to use :
		place_id (str): empty initially, for place
		user_id (str): empty initially, for users id
		text (str): empty initially, for text(review)
	"""

	place_id = ""
	user_id = ""
	text = ""
