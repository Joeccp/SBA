"""Common constants and functions"""
from os import get_terminal_size
import string
from sys import version_info

terminal_width, terminal_height = tuple(get_terminal_size())


def checkPythonVersion() -> None:
	"""
	Checks the Python version.
	If the python version is older than 3.11, it raises an exception.
	:return: None
	:raises SystemExit: If Python version is older than 3.11
	"""
	major_version, minor_version, *_ = version_info
	if major_version < 3:
		err_msg: str = "This program does not support Python 2"
		raise SystemExit(err_msg)
	elif minor_version < 11:
		err_msg: str = "Unsupported old Python version, please use Python 3.11 or newer"
		raise SystemExit(err_msg)


def alphabetToRowIndex(alphabets: str) -> int:
	"""Converts alphabet (A-Z, AA-ZZ) to column index starts from 0
	
	A-Z & AA-ZZ represents (26 + 26*26) = 702 possibilities,
	it is believed that this is very enough for any normal use case
	
	:param alphabets:
		Alphabets (A-Z or AA-ZZ) which represents a row,
		one/two character(s) string, case-insensitive
	:type alphabets: str
	:return: Integer column index which is used when handling seating plan, 0-701
	:rtype: int
	:raises TypeError: If the argument `alphabet` is not a string
	:raises ValueError: If the argument `alphabet` is invalid
	"""
	if type(alphabets) is not str:
		err_msg: str = f"`alphabet` argument must be a string, not {type(alphabets).__name__}"
		raise TypeError(err_msg)
	length: int = len(alphabets)
	if length == 0:
		err_msg: str = f"`alphabets` argument cannot be an empty string"
		raise ValueError(err_msg)
	if length > 2:
		err_msg: str = f"alphabetToRowIndex() does not support string which contains more than 2 characters"
		raise ValueError(err_msg)
	alphabets: str = alphabets.upper()
	for character in alphabets:
		if character not in string.ascii_uppercase:
			raise ValueError(f"'{character}' is not an alphabet")
	# Single alphabet
	if length == 1:
		ret: int = ord(alphabets) - 65
		return ret  # ret in range 0-25
	# Two alphabets
	first_char, second_char = alphabets
	# ret: int = (ord(second_char) - 65) + (ord(first_char) - 65) * 26 + 26  # which equals to:
	ret: int = ord(second_char) + 26 * (ord(first_char)) - 1729
	return ret
	


def seatIDToPlanIndex(seatID: str) -> tuple[int, int]:
	"""Converts seat ID to seating plan index
	
	:param seatID:
		Seat ID is an alphabet(s) index followed by a column number (starts from 1),
		which represents a coordinate of a specific seat inside a cinema house
	:type seatID: str
	:return:
		A coordinate of a seating plan which represents a specific seat inside a cinema house,
		both row and column coordinate starts from 0
	:rtype: tuple[int, int]
	:raises TypeError: If the argument `seatID` is not a string
	:raises ValueError: If the argument `seatID` is invalid
	"""
	
	


if __name__ == '__main__':
	...
