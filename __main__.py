"""A cinema kiosk system"""

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

import argparse
from datetime import datetime
from os import path

from src.admin import adminMode
from src.colour import normal_colour
from src.login import login
from src.user import userMode
from src.utils import checkPythonVersion, checkSystemPlatform, clearScreen, initLog, loadData


__author__ = 'Joe Chau'
__contact__ = 's2018014@bhjs.edu.hk'
__copyright__ = """
		Copyright 2023 Joe Chau

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""
__license__ = 'Apache-2.0'



def main() -> None:
	"""
	The main program
	users (or admin) can login then go to adminMode() or userMode()
	
	It is an infinite loop, so it will never return,
	uses quit() (which is SystemExit) to quit at adminMode()
	
	:return: None
	"""
	
	# So elegant :)
	initLog()
	checkSystemPlatform()
	checkPythonVersion()
	clearScreen()
	print(normal_colour)
	loadData()
	login(first_time=True)
	adminMode()
	clearScreen()
	while True:
		clearScreen()
		if login():
			adminMode()
		else:
			userMode()



if __name__ == '__main__':
	# Parse arguments
	parser = argparse.ArgumentParser(
		description="A simulation of a cinema kiosk system",
		epilog="For documentation of the usage of this program, visit https://joeccp.github.io/SBA/",
		usage="SBA"
	)
	parser.add_argument("-l", "--license",
	                    help="Print copyright information",
	                    action='store_true')
	args = parser.parse_args()
	if args.license:
		print(__license__); quit()
	
	# -------------------------------------------------------------------------
	# main is called INSIDE this if-statement,
	# so that main will NOT be called immediately after __main__ being imported
	main()
	# -------------------------------------------------------------------------
	
	