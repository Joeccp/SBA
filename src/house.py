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
from typing import Self

from .colour import *


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
	tickets_table: list[tuple[str, str, int, str, int, int]] = []
	total_tickets: int = 0
	
	def __init__(self, *,  row_number: int, column_number: int) -> None:
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
		logger: Logger = getLogger("House.clearPlan_")
		logger.info(f"House {self.house_number}'s seating plan has been cleared")
	
	
	def printPlan(self) -> None:
		"""Print the seating plan"""
		line_length: int = self.n_column * 2 + 1
		print(f"{'[Screen Here]':^{line_length+8}}")
		print('    ' + '_' * line_length)
		print('    |', end='')
		for i in range(self.n_column):
			print(column_colour + chr(i+65) + normal_colour, end='|')
		print()
		print('    ' + '-' * line_length)
		for row in range(self.n_row):
			print(f'{row_colour}{row+1:<2}{normal_colour}  |', end='')
			for column in range(self.n_column):
				match self.seating_plan[row][column]:
					case 0:
						symbol = Colour.GREEN_BG + 'O' + normal_colour
					case 1:
						symbol = Colour.RED_BG + 'X' + normal_colour
					case 2:
						symbol = Colour.YELLOW_BG + '!' + normal_colour
				print(symbol, end='|')
			print(f'  {row_colour}{row+1:>2}{normal_colour}')
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
	def searchTicket(cls, ticket_number: str) -> tuple[str, str, int, str, int, int]:
		"""
		DEPRECATED ------
		In an ideal world, it is much faster than linear search.
		However, in reality, with the below code, it does not increase the search time by that much.
		Moreover, it raises the complexity of the code by a lot.
		It is difficult to maintain and debug, compared to a direct for-loop.
		
		Also, it is difficult to tell whether the ticket_number exists or not, compared to a for-else-loop.
		
		In a small-scale business, you can't feel the increased speed,
		in a large-scale business, you would like to use some real database instead of a Python list.
		-----------------
		
		Searches the ticket with the ticket number, assumes ticket number is valid.
		
		It uses binary search.
		
		P.S. Cannot just use ticket index and then do House.tickets_table[ticket_index],
		because some tickets may get deleted or refunded.
		
		NOT MAINTAINED ANYMORE, SO NO BUG FIX
		
		
		:param ticket_number: Ticket number for searching it
		:type ticket_number: str
		:return: The information about that ticket
		:rtype: tuple[str, str, int, str, int, int]
		"""
		logger: Logger = getLogger("House.searchTicket")
		logger.info("Searching ticket")
		
		def getRealIndexFromTicketNumber(ticket_number: str) -> int:
			"""
			Get the 'real' decimal ticket number from the ticket number
			"""
			logger: Logger = getLogger("House.searchTicket.getRealIndexFromTicketNumber")
			ticket_number: str = ticket_number[1:]  # Ignore the 'T'
			ticket_index: int = int(ticket_number)
			logger.info(f"Turning ticket number {ticket_number} into index {ticket_index}")
			return ticket_index
		
		possible_list_index_range: list[int, int] = [0, len(cls.tickets_table) - 1]
		target_ticket_index: int = getRealIndexFromTicketNumber(ticket_number)
		
		while True:
			if possible_list_index_range[0] == possible_list_index_range[1]:
				return cls.tickets_table[possible_list_index_range[0]]
			
			guess_list_index: int = int((possible_list_index_range[1] - possible_list_index_range[0]) / 2)  # int = floor, not round
			guess_ticket_number: str = cls.tickets_table[guess_list_index][0]
			guess_ticket_index: int = getRealIndexFromTicketNumber(guess_ticket_number)
			
			if guess_ticket_index == target_ticket_index:
				return cls.tickets_table[guess_list_index]
			
			if guess_ticket_index <= target_ticket_index:
				possible_list_index_range[0] = guess_list_index
			else:
				possible_list_index_range[1] = guess_list_index
			
			
		
		
		