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
		return len(House.tickets_table)

	