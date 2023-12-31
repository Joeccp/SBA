"""Defines House"""

# Copyright 2023 Joe Chau
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from logging import getLogger, Logger
from typing import NoReturn, Optional, Self, TypeAlias

from .colour import Colour, column_colour, row_colour
from .language import printLang

Row: TypeAlias = list[int]
Seating_plan: TypeAlias = list[Row]

Ticket_index: TypeAlias = int
Ticket_number: TypeAlias = str
Time: TypeAlias = str
House_number: TypeAlias = int
Movie: TypeAlias = str
Row_number: TypeAlias = int  # Not to be confused with Row
Column_number: TypeAlias = int
Price: TypeAlias = int
Ticket: TypeAlias = tuple[Ticket_index, Ticket_number, Time, House_number, Movie, Row_number, Column_number, Price]


class House:
	"""
	A rectangular house of a cinema
	
	In the seating plan,
	0 = Empty (O)
	1 = Sold (X)
	2 = Reserved (!)
	"""
	
	n_House: int = 0
	houses_table: dict[int, Self] = {}
	tickets_table: list[Ticket] = []
	total_revenue: int = 0
	total_tickets: int = 0
	
	def __init__(self, *, row_number: int, column_number: int) -> None:
		"""
		0 < row_number < 100
		0 < column_number < 27
		"""
		self.n_row: int = row_number
		self.n_column: int = column_number
		self.seating_plan: Seating_plan = [[0 for _ in range(self.n_column)] for _ in range(self.n_row)]
		House.n_House += 1
		self.house_number: int = House.n_House
		House.houses_table[self.house_number] = self
		self.movie: str = ''
		self.n_seat: int = self.n_row * self.n_column
		self.house_revenue: int = 0
		self.adult_price: Price = 0
		self.child_price: Price = 0
		logger: Logger = getLogger("House.__init__")
		logger.info(f"House {self.house_number} is created -- {self.n_row}x{self.n_column}")
	
	@property
	def n_available(self) -> int:
		"""
		Returns the number of available seats
		"""
		count: int = 0
		for row in self.seating_plan:
			for seat in row:
				if seat == 0:
					count += 1
		return count
	
	def clearPlan(self) -> None:
		"""Clear the seating plan"""
		self.seating_plan: Seating_plan = [[0 for _ in range(self.n_column)] for _ in range(self.n_row)]
		logger: Logger = getLogger("House.clearPlan")
		logger.info(f"House {self.house_number}'s seating plan has been cleared")
	
	def printSeatingPlan(self) -> None:  # pragma: no cover # skip coverage report -- IDK how to mock output
		"""Print the seating plan"""
		from .colour import normal_colour
		
		line_length: int = self.n_column * 2 + 1
		printLang(f"{'[Screen Here]':^{line_length + 8}}",
		          f"{'[銀幕在此]':^{line_length + 6}}")
		print('    ' + '_' * line_length)
		print('    |', end='')
		for i in range(self.n_column):
			print(column_colour + chr(i + 65) + normal_colour, end='|')
		print()
		print('    ' + '-' * line_length)
		for row in range(self.n_row):
			print(f'{row_colour}{row + 1:<2}{normal_colour}  |', end='')
			for column in range(self.n_column):
				match self.seating_plan[row][column]:
					case 0:
						symbol = Colour.GREEN_BG + Colour.BLACK + ' ' + normal_colour
					case 1:
						symbol = Colour.RED_BG + Colour.BLACK + 'X' + normal_colour
					case 2:
						symbol = Colour.YELLOW_BG + Colour.BLACK + '!' + normal_colour
				print(symbol, end='|')  # NOQA
			print(f'  {row_colour}{row + 1:>2}{normal_colour}')
			print('    ' + '-' * line_length)
		print()
		printLang(Colour.GREEN_BG + Colour.BLACK + "  -- Empty   " + normal_colour,
		          Colour.GREEN_BG + Colour.BLACK + "  -- 可選座位" + normal_colour)
		printLang(Colour.RED_BG + Colour.BLACK + "X -- Sold    " + normal_colour,
		          Colour.RED_BG + Colour.BLACK + "X -- 已售座位" + normal_colour)
		printLang(Colour.YELLOW_BG + Colour.BLACK + "! -- Reserved" + normal_colour,
		          Colour.YELLOW_BG + Colour.BLACK + "! -- 保留座位" + normal_colour)
		print()
	
	def printSeatingPlanWithSelectedSeat(self, selected_seat_list: list[tuple[int, int]]) -> None:  # pragma: no cover # skip coverage report -- IDK how to mock output # NOQA # line too long
		"""Print the seating plan with the selected seats shown in different colour"""
		from .colour import normal_colour
		
		line_length: int = self.n_column * 2 + 1
		printLang(f"{'[Screen Here]':^{line_length + 8}}",
		          f"{'[銀幕在此]':^{line_length + 6}}")
		print('    ' + '_' * line_length)
		print('    |', end='')
		for i in range(self.n_column):
			print(column_colour + chr(i + 65) + normal_colour, end='|')
		print()
		print('    ' + '-' * line_length)
		for row in range(self.n_row):
			print(f'{row_colour}{row + 1:<2}{normal_colour}  |', end='')
			for column in range(self.n_column):
				if (row, column) in selected_seat_list:
					print(Colour.CYAN_BG + Colour.BLACK + '?' + normal_colour, end='|')
					continue
				match self.seating_plan[row][column]:
					case 0:
						symbol = Colour.GREEN_BG + Colour.BLACK + ' ' + normal_colour
					case 1:
						symbol = Colour.RED_BG + Colour.BLACK + 'X' + normal_colour
					case 2:
						symbol = Colour.YELLOW_BG + Colour.BLACK + '!' + normal_colour
				print(symbol, end='|')  # NOQA
			print(f'  {row_colour}{row + 1:>2}{normal_colour}')
			print('    ' + '-' * line_length)
		print()
		printLang(Colour.GREEN_BG + Colour.BLACK + "  -- Empty   " + normal_colour,
		          Colour.GREEN_BG + Colour.BLACK + "  -- 可選座位" + normal_colour)
		printLang(Colour.RED_BG + Colour.BLACK + "X -- Sold    " + normal_colour,
		          Colour.RED_BG + Colour.BLACK + "X -- 已售座位" + normal_colour)
		printLang(Colour.YELLOW_BG + Colour.BLACK + "! -- Reserved" + normal_colour,
		          Colour.YELLOW_BG + Colour.BLACK + "! -- 保留座位" + normal_colour)
		printLang(Colour.CYAN_BG + Colour.BLACK + "? -- Selected" + normal_colour,
		          Colour.CYAN_BG + Colour.BLACK + "? -- 已選座位" + normal_colour)
		print()
	
	@classmethod
	def get_n_tickets(cls) -> int:
		"""Returns the number of tickets sold in ALL houses"""
		return len(cls.tickets_table)
	
	@classmethod
	def searchTicket(cls, target_ticket_index: int) -> Optional[Ticket]:
		"""
		Searches the ticket with the given ticket index, and returns it.
		Assumes the (format of the) ticket index is valid.
		If the ticket does not exist, returns None.
		
		It uses binary search.
		
		ASSUMES House.tickets_table IS ALREADY SORTED (As it should be sorted anytime).
		
		:param target_ticket_index: Ticket index with a valid format
		:type target_ticket_index: int
		:return: Ticket
		:rtype: Optional[tuple[int, str, str, int, str, int, int, int]]
		"""
		logger: Logger = getLogger("House.searchTicket")
		logger.info(f"Searching ticket: {target_ticket_index}")
		
		if not cls.tickets_table:
			logger.info("No any tickets, just return None")
			return None
		
		min_: int = 0
		max_: int = cls.get_n_tickets() - 1
		logger.debug(f"Min: {min_}  & Max: {max_}")
		
		while True:
			logger.debug(f"Min: {min_}  & Max: {max_}")
			if min_ == max_:
				if cls.tickets_table[min_][0] == target_ticket_index:
					logger.debug(f"cls.tickets_table[min_][0] = {cls.tickets_table[min_][0]}")
					logger.info(f"Return ticket: {cls.tickets_table[min_]}")
					return cls.tickets_table[min_]
				else:
					logger.info("No such ticket")
					return None
			
			if max_ - min_ == 1:
				if cls.tickets_table[max_][0] == target_ticket_index:
					return cls.tickets_table[max_]
				elif cls.tickets_table[min_][0] == target_ticket_index:
					return cls.tickets_table[min_]
				else:
					return None
			
			half: int = int((max_ + min_) / 2)  # int() = floor()
			guess_ticket_index: int = cls.tickets_table[half][0]
			
			logger.debug(f"half: {half}  guess_ticket_index: {guess_ticket_index}")
			
			if guess_ticket_index == target_ticket_index:
				logger.info(f"Return ticket: cls.tickets_table[half] = {cls.tickets_table[half]}")
				return cls.tickets_table[half]
			elif guess_ticket_index > target_ticket_index:
				max_: int = half
				logger.debug("max_ <- half")
				logger.debug(f"max is now {max_}")
			else:
				min_: int = half
				logger.debug("min_ <- half")
				logger.debug(f"min is now {min_}")
	
	# THE BELOW DUNDER METHODS ARE DEFINED FOR FUTURE USAGE ONLY, NOT IN USED
	
	def __str__(self) -> str:
		return f"House {self.house_number}"

	def __getitem__(self, key: int) -> Row:
		"""
		Returns self.seating_plan[key]
		
		So `house[key]` will return the corresponding row of the seating plan where `house` is a `House` instance.
		It should only be used ONLY when you want to READ the seating plan, not changing it.
		It provides more simple iteration.
		
		E.g.
			for seat in house[row_number]:
				...
		
		:param key: Row number
		:type key: int
		:return: The corresponding row of the seating plan
		:rtype: list[int]
		"""
		return self.seating_plan[key]
	
	def __setitem__(self, key: int, value: Row) -> NoReturn:
		"""
		Do self.seating_plan[key] = value
		
		NOTE: value should be a ROW, not a seat.
		
		In most of the cases, you would NOT like to use this method.
		I can't think of any reason for implementing this method.
		You should do `self.seating_plan[key] = value` instead.
		However, I have already defined the __getitem__ method,
		which may cause confusion where programmers (i.e. me) think there is an error.
		
		It raises MethodShouldNotBeUsed
		
		:param key: Row number
		:type key: int
		:param value: New row
		:type value: list[int]
		"""
		class MethodShouldNotBeUsed(Exception):
			"""House.__setitem__ method should NEVER be used, do self.seating_plan[row_number] = row instead"""
			def __str__(self) -> str:
				self.__doc__: str
				return self.__doc__
		raise MethodShouldNotBeUsed
