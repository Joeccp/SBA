"""The main program"""

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


from .admin import adminMode
from .colour import normal_colour
from .login import login
from .user import userMode
from .utils import checkPythonVersion, checkSystemPlatform, clearScreen, initLog, loadData


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
		adminMode() if login() else userMode()
	

if __name__ == '__main__':
	main()
