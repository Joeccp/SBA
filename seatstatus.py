"""Defines Status class to represent the status of a seat"""

from enum import Enum


class Status(Enum):
	"""
	Enumeration type used for representing different status of a seat
	
	`Status.EMPTY` means that the seat is empty and can be brought
	
	`Status.SOLD` means that the seat is sold
	
	`Status.RESERVED` means that seat is reserved and is not for sale
	"""
	EMPTY = 0
	SOLD = 1
	RESERVED = 2
	
	
	