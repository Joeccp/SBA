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
	WHITE_BG: str = '\033[47m'
	GREEN_BG: str = '\033[102m'
	YELLOW_BG: str = '\033[103m'
	RED_BG: str = '\033[101m'




row_colour: str = Colour.BLUE
column_colour: str = Colour.PURPLE
normal_colour: str = Colour.WHITE_BG + Colour.BLACK
