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

# NOQA: E402

if __name__ == '__main__':
	# 'main' is above the imports as you will get error about relative import if executed directly
	# If it is under the imports, it will never run due to the error
	print("Please do NOT run me directly. Instead, run __main__.py in the root directory of this project")
	quit()

# You can't even import some of the module here as you will get NameError in an older version of the Python
# Better to check before import, so people will know what's wrong
# System platform is also checked here to maintain consistency
# As a result, system platform and Python version are checked when importing this module

from .utils import checkPythonVersion, checkSystemPlatform

checkSystemPlatform()
checkPythonVersion()

from .admin import adminMode
from .colour import normal_colour
from .login import login
from .user import userMode
from .utils import clearScreen, initLog, loadData


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
	clearScreen()
	print(normal_colour)
	loadData()
	login(first_time=True)
	adminMode()
	clearScreen()
	while True:
		clearScreen()
		adminMode() if login() else userMode()
