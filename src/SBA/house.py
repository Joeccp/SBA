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
from typing import Optional, Self

from .colour import Colour, column_colour, normal_colour, row_colour


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
	tickets_table: list[tuple[int, str, str, int, str, int, int]] = []
	total_tickets: int = 0
	
	def __init__(self, *, row_number: int, column_number: int) -> None:
		"""
		0 < row_number < 100
		0 < column_number < 27
		"""
		self.n_row: int = row_number
		self.n_column: int = column_number
		self.seating_plan: list[list[int]] = [[0 for _ in range(self.n_column)] for _ in range(self.n_row)]
		House.n_House += 1
		self.house_number: int = House.n_House
		House.houses_table[self.house_number] = self
		self.movie: str = ''
		self.n_seat: int = self.n_row * self.n_column
		logger: Logger = getLogger("House.__init__")
		logger.info(f"House {self.house_number} is created -- {self.n_row}x{self.n_column}")
	
	@property
	def n_available(self) -> int:
		count: int = 0
		for row in self.seating_plan:
			for seat in row:
				if seat == 0:
					count += 1
		return count
	
	def clearPlan(self) -> None:
		"""Clear the seating plan"""
		self.seating_plan: list[list[int]] = [[0 for _ in range(self.n_column)] for _ in range(self.n_row)]
		logger: Logger = getLogger("House.clearPlan")
		logger.info(f"House {self.house_number}'s seating plan has been cleared")
	
	def printPlan(self) -> None:
		"""Print the seating plan"""
		line_length: int = self.n_column * 2 + 1
		print(f"{'[Screen Here]':^{line_length + 8}}")
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
						symbol = Colour.GREEN_BG + 'O' + normal_colour
					case 1:
						symbol = Colour.RED_BG + 'X' + normal_colour
					case 2:
						symbol = Colour.YELLOW_BG + '!' + normal_colour
				print(symbol, end='|')  # NOQA
			print(f'  {row_colour}{row + 1:>2}{normal_colour}')
			print('    ' + '-' * line_length)
		print()
		print(Colour.GREEN_BG + "O -- Empty" + normal_colour)
		print(Colour.RED_BG + "X -- Sold" + normal_colour)
		print(Colour.YELLOW_BG + "! -- Reserved" + normal_colour)
		print()
	
	@classmethod
	def n_tickets(cls) -> int:
		"""Returns the number of tickets sold in ALL houses"""
		return len(cls.tickets_table)
	
	@classmethod
	def searchTicket(cls, target_ticket_index: int) -> Optional[tuple[int, str, str, int, str, int, int]]:
		"""
		Searches the ticket with the given ticket index, and returns it.
		Assumes the (format of the) ticket index is valid.
		If the ticket does not exist, returns None.
		
		It uses binary search.
		
		ASSUMES House.tickets_table IS ALREADY SORTED (As it should be sorted anytime).
		
		:param target_ticket_index: Ticket index with a valid format
		:type target_ticket_index: int
		:return: Ticket
		:rtype: Optional[tuple[int, str, str, int, str, int, int]]
		"""
		logger: Logger = getLogger("House.searchTicket")
		logger.info(f"Searching ticket: {target_ticket_index}")
		
		min_: int = 0
		max_: int = cls.n_tickets() - 1
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
