"""Defines the House class"""

from seatstatus import Status
from typing import Self


class House:
	"""A 2D rectangular house in a cinema"""
	
	house_count: int = 0
	house_table: dict[int, Self] = {}
	
	def __init__(self, name: str, n_row: int, n_column: int) -> None:
		"""
		Create a House instance.
		
		:param name: Name of the house. Leading, and trailing whitespaces will be removed automatically.
		:type name: str
		:param n_row: Number of rows in the house, must be an int >= 1
		:type n_row: int
		:param n_column: Number of columns in the house, must be an int >= 1
		:type n_column: int
		"""
		
		# Check arguments
		if type(name) is not str:
			err_msg: str = f"House name must be a string, not {type(name).__name__}"
			raise TypeError(err_msg)
		name: str = name.strip()
		if type(n_row) is not int:
			err_msg: str = f"Number of rows must be a string, not {type(name).__name__}"
			raise TypeError(err_msg)
		if type(n_column) is not int:
			err_msg: str = f"HNumber of columns must be a string, not {type(name).__name__}"
			raise TypeError(err_msg)
		if n_row < 1:
			err_msg: str = f"Number of rows must be larger than 0"
			raise ValueError(err_msg)
		if n_column < 1:
			err_msg: str = f"Number of columns must be larger than 0"
			raise ValueError(err_msg)
		# A-Z & AA-ZZ represents (26 + 26*26) = 702 possibilities,
		# it is believed that this is very enough for any normal use case
		if n_row > 702:
			err_msg: str = f"Number of row too big (>702)"
			raise ValueError(err_msg)
		
		
		# Update information of inside the House class
		House.house_count += 1
		House.house_table[House.house_count] = self
		
		# Initialize properties
		self.name: str = name
		self.n_row: int = n_row
		self.n_column: int = n_column
		self.max: int = n_row * n_column
		self.plan: list = [[Status.EMPTY for i in range(n_column)] for j in range(n_row)]
		self.id: int = House.house_count
		self.available: int = self.max  # Number of empty seats
	
	def __str__(self) -> str:
		...
	
	def buy(self, row_number: int, column_number: int) -> None:
		"""
		Buy the seat with the corresponding row and column number.
		Column number is an integer instead of an alphabet.
		Row and column number starts from 0.
		
		Specifically it changes the seat status to `Status.SOLD`.
		It does not check whether the seat is already sold or not.
		(However it does check whether row and column number of the seat is valid or not.)
		
		:param row_number: Row number of the seat, starts from 0
		:type row_number: int
		:param column_number: Column number of the seat, is an integer instead of an alphabet, starts from 1
		:type column_number: int
		"""
		if type(row_number) is not int:
			err_msg: str = f"Row number must be a string, not {type(row_number).__name__}"
			raise TypeError(err_msg)
		if type(column_number) is not int:
			err_msg: str = f"Column number must be a string, not {type(column_number).__name__}"
			raise TypeError(err_msg)
		if row_number < 0:
			err_msg: str = f"Row number must be larger than 0"
			raise ValueError(err_msg)
		if column_number < 0:
			err_msg: str = f"Column number must be larger than 0"
			raise ValueError(err_msg)
		if row_number == self.n_row:
			err_msg: str = f"No such row (row number too big) (row number starts from 0)"
			raise ValueError(err_msg)
		if column_number == self.n_column:
			err_msg: str = f"No such column (column number too big) (column number starts from 0)"
			raise ValueError(err_msg)
		if row_number >= self.n_row:
			err_msg: str = f"No such row (row number too big)"
			raise ValueError(err_msg)
		if column_number >= self.n_column:
			err_msg: str = f"No such column (column number too big)"
			raise ValueError(err_msg)
		
		
		self.plan[row_number][column_number]: Status = Status.SOLD
		self.available: int = self.available - 1
		
		
	
	def reserve(self, row_number, column_number) -> None:
		"""
		Reserve the seat with the corresponding row and column number.
		Column number is an integer instead of an alphabet.
		Row and column number starts from 0.
		
		Specifically it changes the seat status to `Status.RESERVED`.
		It does check whether the seat is already reserved or not,
		but the checking will not affect anything other than `self.available`.
		(Also it does check whether row and column number of the seat is valid or not.)
		
		:param row_number: Row number of the seat, starts from 0
		:type row_number: int
		:param column_number: Column number of the seat, is an integer instead of an alphabet, starts from 1
		:type column_number: int
		"""
		if type(row_number) is not int:
			err_msg: str = f"Row number must be a string, not {type(row_number).__name__}"
			raise TypeError(err_msg)
		if type(column_number) is not int:
			err_msg: str = f"Column number must be a string, not {type(column_number).__name__}"
			raise TypeError(err_msg)
		if row_number < 0:
			err_msg: str = f"Row number must be larger than 0"
			raise ValueError(err_msg)
		if column_number < 0:
			err_msg: str = f"Column number must be larger than 0"
			raise ValueError(err_msg)
		if row_number == self.n_row:
			err_msg: str = f"No such row (row number too big) (row number starts from 0)"
			raise ValueError(err_msg)
		if column_number == self.n_column:
			err_msg: str = f"No such column (column number too big) (column number starts from 0)"
			raise ValueError(err_msg)
		if row_number >= self.n_row:
			err_msg: str = f"No such row (row number too big)"
			raise ValueError(err_msg)
		if column_number >= self.n_column:
			err_msg: str = f"No such column (column number too big)"
			raise ValueError(err_msg)
		
		if self.plan[row_number][column_number] == Status.SOLD:
			self.available: int = self.available + 1
		self.plan[row_number][column_number]: Status = Status.RESERVED
	
	def getSeatStatus(self, row_number, column_number) -> Status:
		...
	
	def setSeatEmpty(self, row_number, column, number) -> None:
		...
	
	# RFC 2119 --
	# The phrase "NOT RECOMMENDED" means that
	# there may exist valid reasons in particular circumstances when the
	# particular behavior is acceptable or even useful, but the full
	# implications should be understood and the case carefully weighed
	# before implementing any behavior described with this label.
	#
	# Human language: Just don't!
	
	def __getitem__(self, item: int) -> list[Status]:
		"""
		(Equals to `house[item]` where `house` is a `House` instance)
		It is ***NOT RECOMMENDED*** to use this method or do `House[item]`.
		
		
		Please use `House.getSeatStatus()` to check the status of the seat,
		and use `House.plan` for iteration and loops instead.
		
		It does not do any checking.
		
		:param item: Row number
		:type item: int
		:return: list[Status]
		"""
		
	
	def __setitem__(self, key, value) -> None:
		"""
		
		...
		
		Please use `House.buy()`, `House.reserve()`, `House.setSeatEmpty()` to set the status of the seat instead.
		
		...
		
		
		:param key:
		:param value:
		:return:
		"""
	
	
	def __class_getitem__(cls, item) -> Self:
		"""
		Equals to `House[item]`
		
		:param item:
		:return:
		"""
	
	
	
	

if __name__ == '__main__':
	...
