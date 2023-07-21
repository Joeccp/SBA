"""Defines House"""
from typing import Self
from common import clearScreen


class House:
	"""
	A rectangular house of a cinema
	
	In the seating plan,
	0 = Empty (O)
	1 = Sold (X)
	2 = Reserved (!)
	"""
	
	n_House: int = 0
	table: dict[int, Self] = {}
	
	def __init__(self, *,  row_number: int, column_number: int) -> None:
		"""
		0 < row_number < 100
		0 < column_number < 27
		"""
		self.n_row: int = row_number
		self.n_column: int = column_number
		self.plan: list[list[int]] = [[0 for _ in range(self.n_column)] for _ in range(self.n_row)]
		House.n_House += 1
		self.house_number: int = House.n_House
		House.table[self.house_number] = self
		self.movie = ''

	
	def clearPlan(self) -> None:
		self.plan: list[list[int]] = [[0 for _ in range(self.n_column)] for _ in range(self.n_row)]
	
	
	def printPlan(self) -> None:
		line_length: int = self.n_column * 2 + 1
		print(f"    {'[Screen]':^{line_length}}")
		print('    ' + '_' * line_length)
		print('    |', end='')
		for i in range(self.n_column):
			print(chr(i+65), end='|')
		print()
		print('    ' + '-' * line_length)
		for row in range(self.n_row):
			print(f'{row+1:<2}  |', end='')
			for column in range(self.n_column):
				match self.plan[row][column]:
					case 0:
						symbol = 'O'
					case 1:
						symbol = 'X'
					case 2:
						symbol = '!'
				print(symbol, end='|')
			print(f'  {row+1:>2}')
			print('    ' + '-' * line_length)



if __name__ == '__main__':
	r = int(input("Row number:"))
	c = int(input("Column number:"))
	house = House(row_number=r, column_number=c)
	house.print()