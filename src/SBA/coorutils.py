"""Utilities for handling coordinate"""

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
from string import ascii_uppercase, digits
from typing import Any, Callable, TypeAlias

Coor: TypeAlias = tuple[int, int]


class EmptyCoordinate(Exception):
	"""Empty coordinate"""


class InvalidCharacter(Exception):
	"""Invalid character inside coordinate expression"""


class MoreThanOneColon(Exception):
	"""More than one colon in a coordinate expression"""


class NoColumnCoordinate(Exception):
	"""No column coordinate"""


class NoRowCoordinate(Exception):
	"""No row coordinate"""


class AlphabetCharacterInRowNumber(Exception):
	"""Column coordinate has more than two characters"""


class RowNumberIsZero(Exception):
	"""Row number cannot be 0 (row number starts with 1)"""


class NoStartingCoordinate(Exception):
	"""Starting coordinate not given"""


class NoEndingCoordinate(Exception):
	"""Ending coordinate not given"""


class CoordinatesWrongOrder(Exception):
	"""Wrong order of the two coordinates"""


class SameCoordinates(Exception):
	"""Two same coordinates"""


class RowNumberOutOfRange(Exception):
	"""The row number is out of range, and does not exist"""


class ColumnNumberOutOfRange(Exception):
	"""The column number is out of range, and does not exist"""


class RowCoordinatesAtTwoSide(Exception):
	"""Two row coordinates given in a single seat coordinate"""


class ColumnCoordinatesAtTwoSide(Exception):
	"""Two column coordinates given in a single seat coordinate"""


def ExceptionLogger(function: Callable) -> Callable:
	def functionWithLogger(*args, **kwargs) -> Any:
		try:
			return_: Any = function(*args, **kwargs)
			return return_
		except Exception as exception:  # NOQA # Too many possible exceptions
			logger: Logger = getLogger(function.__name__)
			logger.debug(f'Exception: {exception.__class__.__name__}')
			raise exception
	
	return functionWithLogger


@ExceptionLogger
def coorExprAnalysis(coor_expr: str, /, *, n_row: int = 99, n_column: int = 26) -> list[tuple[int, int]]:
	"""
	Analysis the coordinate expression.
	
	If the coordinate expression represents a single seat,
	returns a list containing single-seat coordinate
	
	If the coordinate expression represents two or more seats,
	returns a list of two single-seat coordinates representing the start and end of an area
	
	Single seat coordinate means a tuple containing the row and column indexes respectively
	
	Assumes column coordinate starts from A to Z only.
	
	:param coor_expr: A coordinate expression
	:type coor_expr: str
	:param n_row: Number of row of the house
	:type n_row: int
	:param n_column: Number of column of the house
	:type n_column: int
	:return: A list containing one or more single-seat coordinate
	:rtype: list[tuple[int, int]]
	:raise EmptyCoordinate:
	:raise InvalidCharacter:
	:raise MoreThanOneColon:
	:raise NoColumnCoordinate:
	:raise NoRowCoordinate:
	:raise AlphabetCharacterInRowNumber:
	:raise RowNumberIsZero:
	:raise NoStartingCoordinate:
	:raise NoEndingCoordinate:
	:raise CoordinatesWrongOrder:
	:raise SameCoordinates:
	:raise RowNumberOutOfRange:
	:raise ColumnNumberOutOfRange:
	:raise RowCoordinatesAtTwoSide:
	:raise ColumnCoordinatesAtTwoSide:
	:raise TypeError:
	:raise ValueError:
	"""
	logger: Logger = getLogger('coorExprAnalysis')
	logger.info(f"Analysing the coordinate expression: {coor_expr}")
	
	if type(coor_expr) is not str or type(n_row) is not int or type(n_column) is not int:
		raise TypeError
	if not 1 <= n_row <= 99 or not 1 <= n_column <= 99:
		raise ValueError
	
	coor_expr: str = (coor_expr
	                  .strip()
	                  .replace(' ', '')
	                  .replace('\t', '')
	                  .upper())
	
	if coor_expr == '':
		raise EmptyCoordinate
	
	for char in coor_expr:
		if char not in ascii_uppercase + digits + ':':
			raise InvalidCharacter
	
	if coor_expr[0] == ':':
		raise NoStartingCoordinate
	
	if coor_expr[-1] == ':':
		raise NoEndingCoordinate
	
	if ':' not in coor_expr:  # Single seat
		if all([char in ascii_uppercase for char in coor_expr]):
			raise NoRowCoordinate
		if all([char in digits for char in coor_expr]):
			raise NoColumnCoordinate
		if coor_expr[0] in ascii_uppercase and coor_expr[-1] in ascii_uppercase:
			raise ColumnCoordinatesAtTwoSide
		if coor_expr[0] in digits and coor_expr[-1] in digits:
			raise RowCoordinatesAtTwoSide
		
		if coor_expr[0] in digits:  # Row first
			column: str = coor_expr[-1]  # Row first = last char is column
			row_str: str = coor_expr[:-1]
			if any([char in ascii_uppercase for char in row_str]):
				raise AlphabetCharacterInRowNumber
			row: int = int(row_str)
		
		else:  # Column first
			column: str = coor_expr[0]  # Column first = first char is column
			row_str: str = coor_expr[1:]
			if any([char in ascii_uppercase for char in row_str]):
				raise AlphabetCharacterInRowNumber
			row: int = int(row_str)
		
		coordinate: tuple[int, str] = (row, column)
		coordinates: list[tuple[int, str]] = [coordinate]
	
	elif coor_expr.count(':') > 1:
		raise MoreThanOneColon
	
	else:
		coordinates: list[tuple[int, str]] = []
		for coor in coor_expr.split(':'):
			if all([char in ascii_uppercase for char in coor]):
				raise NoRowCoordinate
			if all([char in digits for char in coor]):
				raise NoColumnCoordinate
			if coor[0] in ascii_uppercase and coor[-1] in ascii_uppercase:
				raise ColumnCoordinatesAtTwoSide
			if coor[0] in digits and coor[-1] in digits:
				raise RowCoordinatesAtTwoSide
			
			if coor[0] in digits:  # Row first
				column: str = coor[-1]  # Row first = last char is column
				row_str: str = coor[:-1]
				if any([char in ascii_uppercase for char in row_str]):
					raise AlphabetCharacterInRowNumber
				row: int = int(row_str)
			
			else:  # Column first
				column: str = coor[0]  # Column first = first char is column
				row_str: str = coor[1:]
				if any([char in ascii_uppercase for char in row_str]):
					raise AlphabetCharacterInRowNumber
				row: int = int(row_str)
			
			coordinate: tuple[int, str] = (row, column)
			coordinates.append(coordinate)
	
	coordinate_indexes: list[tuple[int, int]] = []
	for coordinate in coordinates:
		row: int = coordinate[0]
		if row == 0:
			raise RowNumberIsZero
		row_index: int = row - 1
		column: str = coordinate[1]
		column_index: int = ord(column) - 65
		coordinate_index: tuple[int, int] = (row_index, column_index)
		coordinate_indexes.append(coordinate_index)
	
	if len(coordinate_indexes) == 2:
		start, end = coordinate_indexes
		if start == end:
			raise SameCoordinates
		if start[0] > end[0]:
			raise CoordinatesWrongOrder
		if start[0] == end[0]:  # Same row
			if start[1] > end[1]:
				raise CoordinatesWrongOrder
	
	max_row_index: int = n_row - 1
	max_column_index: int = n_column - 1
	for coordinate_index in coordinate_indexes:
		row_index, column_index = coordinate_index
		if row_index > max_row_index:
			raise RowNumberOutOfRange
		if column_index > max_column_index:
			raise ColumnNumberOutOfRange
	
	logger.debug(f'{coordinate_indexes}')
	return coordinate_indexes


@ExceptionLogger
def getCoorsFromCoorExpr(coor_expr: str, /, *, n_row: int = 99, n_column: int = 26) -> list[Coor]:
	"""
	Returns a list of coordinates which the coor_expr argument defines.
	
	:param coor_expr: A coordinate expression
	:type coor_expr: str
	:param n_row: Number of row of the house
	:type n_row: int
	:param n_column: Number of column of the house
	:type n_column: int
	:return: A list of coordinates
	:rtype: list[tuple[int, int]]
	"""
	logger: Logger = getLogger('getCoorsFromCoorExpr')
	logger.info(f"Analysing the coordinate expression: {coor_expr}")
	
	analysis_result: list[Coor] = coorExprAnalysis(coor_expr, n_row=n_row, n_column=n_column)
	
	if len(analysis_result) == 1:
		logger.info("Single coordinate")
		return analysis_result
	
	analysis_result_start: Coor = analysis_result[0]
	analysis_result_end: Coor = analysis_result[1]
	
	# Single row:
	if analysis_result_start[0] == analysis_result_end[0]:
		logger.info("Single row")
		row_index: int = analysis_result_start[0]
		coordinates: list[Coor] = []
		for column_index in range(analysis_result_start[1], analysis_result_end[1] + 1):
			coordinates.append((row_index, column_index))
		return coordinates
		
	# Single column:
	if analysis_result_start[1] == analysis_result_end[1]:
		logger.info("Single column")
		column_index: int = analysis_result_start[1]
		coordinates: list[Coor] = []
		for row_index in range(analysis_result_start[0], analysis_result_end[0] + 1):
			coordinates.append((row_index, column_index))
		return coordinates
	
	starting_coordinate: Coor = analysis_result_start
	ending_coordinate: Coor = analysis_result_end
	
	# Detect 'top-right to bottom-left' and change it to 'top-left to bottom-right'
	if analysis_result_start[1] > analysis_result_end[1]:
		logger.info("Top-right to bottom-left detected! Changing it...")
		starting_coordinate: Coor = (analysis_result_start[0], analysis_result_end[1])
		ending_coordinate: Coor = (analysis_result_end[0], analysis_result_start[1])
		
	logger.debug(f"Starting coordinate: {starting_coordinate}")
	logger.debug(f"Ending coordinate: {ending_coordinate}")
	
	coordinates: list[Coor] = []
	
	for row_index in range(starting_coordinate[0], ending_coordinate[0] + 1):
		for column_index in range(starting_coordinate[1], ending_coordinate[1] + 1):
			logger.debug(f"Adding coordinate {row_index} {column_index}")
			coordinates.append((row_index, column_index))

	return coordinates
