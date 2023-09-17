"""Defines different colour code"""

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
from os import path
from typing import Literal

"""
In this module, there are many variables store the colour information,
such as `colour_mode` and `normal_colour`.
These variables may change.

Due to the mechanism of importing in Python,
the changes of these variables cannot be seen outside this module immediately,
you have to import it AGAIN
"""

ColourCode = Literal['DARK', 'LIGHT']

colour_mode: ColourCode = 'DARK'


class Colour:
	"""
	Encapsulate different ANSI escape sequences,
	for printing coloured texts and background
	"""
	RESET: str = '\033[0m'
	BLUE: str = '\033[1;94m'  # For row letters
	PURPLE: str = '\033[1;35m'  # For column numbers
	RED: str = '\033[1;31m'
	BLACK: str = '\033[30m'
	GREEN: str = '\033[1;32m'
	WHITE: str = '\033[37m'
	WHITE_BG: str = '\033[47m'
	GREEN_BG: str = '\033[102m'
	YELLOW_BG: str = '\033[103m'
	RED_BG: str = '\033[101m'
	BLACK_BG: str = '\033[40m'


row_colour: str = Colour.BLUE
column_colour: str = Colour.PURPLE

font_colour: str = Colour.WHITE
background_colour: str = Colour.BLACK_BG
normal_colour: str = font_colour + background_colour


def setColour(colour_code: ColourCode) -> None:
	"""
	Set the font and background colour
	
	:param colour_code: A colour code
	:type colour_code: ColourCode
	:return: None
	"""
	global background_colour, colour_mode, font_colour, normal_colour
	
	logger: Logger = getLogger('setColour')
	logger.info(f"Admin wants to set colour to {colour_code}")
	
	if colour_code == 'DARK':
		logger.info("Setting colour to DARK")
		colour_mode = 'DARK'
		font_colour = Colour.WHITE
		background_colour = Colour.BLACK_BG
		normal_colour = font_colour + background_colour
	elif colour_code == 'LIGHT':
		logger.info("Setting colour to LIGHT")
		colour_mode = 'LIGHT'
		font_colour = Colour.BLACK
		background_colour = Colour.WHITE_BG
		normal_colour = font_colour + background_colour
	else:
		logger.info("Unknown colour code: Setting to DARK...")
		setColour('DARK')
	
	logger.info(f"The colour scheme is now {colour_mode}")
	
	logger.info("Saving colour code...")
	absolute_path = path.dirname(__file__)
	relative_path = "../../data/colour.txt"
	full_path = path.join(absolute_path, relative_path)
	logger.debug(f"Full path = {full_path}")
	
	logger.info("Reaching the file")
	with open(full_path, 'w') as file:
		logger.info("Writing the colour data to the file")
		file.write(colour_mode)
		
	print(normal_colour, end='')


def loadColour() -> None:
	"""
	Load the font and background colour setting

	Reads the data from data/colour.txt
	If the file does not exist, create one and set to DARK

	:return: None
	"""
	
	logger: Logger = getLogger('loadColour')
	logger.info("Loading the colour scheme")
	
	absolute_path = path.dirname(__file__)
	relative_path = "../../data/colour.txt"
	full_path = path.join(absolute_path, relative_path)
	logger.debug(f"Full path = {full_path}")
	
	try:
		logger.info("Reaching the file")
		with open(full_path, 'r') as file:
			# The context of the file should be a valid ColorCode
			colour_code: str = file.read().strip().upper()
			logger.info(f"Colour code stored in the file is {colour_code}")
			if colour_code not in ['DARK', 'LIGHT']:  # Save insurance
				logger.info("Unknown colour_code, default set to DARK")
				colour_code: ColourCode = 'DARK'
			colour_code: ColourCode
	except FileNotFoundError:
		logger.info("File not found, default set to DARK")
		colour_code = 'DARK'
	
	setColour(colour_code)
