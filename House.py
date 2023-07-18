"""Defines the House class"""


class House:
	"""A 2D rectangular house in a cinema"""
	
	house_count: int = 0
	
	def __init__(self, name: str, n_row: int, n_column: int) -> None:
		"""
		Create a House instance.
		
		:param name: Name of the house
		:type name: str
		:param n_row: Number of rows in the house, must be an int >= 1
		:type n_row: int
		:param n_column: Number of columns in the house, must be an int >= 1
		:type n_column: int
		"""
