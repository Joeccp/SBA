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

from logging import getLogger, Logger
from time import sleep
from traceback import format_exception

from .admin import adminMode
from .colour import loadColour
from .language import loadLanguage
from .login import login
from .user import userMode
from .utils import clearScreen, initLog, loadData, RealExit


exception_list: list[Exception] = []


def main() -> None:
	"""
	The main program
	users (or admin) can login then go to adminMode() or userMode()
	
	It is an infinite loop, so it will never return,
	uses quit() (which is SystemExit) to quit at adminMode()
	
	:return: None
	"""
	
	initLog()
	logger: Logger = getLogger("main")
	logger.info("Inside the main function")
	
	def _main() -> None:
		"""
		This function just holds all the work of the main function (except initLog)
		
		This function exists, so that when recursively call _main, it will not do initLog() for many times
		
		:return: None
		"""
	
	
		global exception_list
		
		try:
		
			logger: Logger = getLogger("main._main")
			logger.info("Inside the main loop")
		
			# So elegant :)
			loadColour()
			loadLanguage()
			clearScreen()
			from .colour import normal_colour
			print(normal_colour)
			loadData()
			login(first_time=True)
			adminMode()
			clearScreen()
			while True:
				clearScreen()
				adminMode() if login() else userMode()
		
		# Very not elegant :(
		# Below is an error handling chaos, need to be improved
		# For the below input/output, no need translation, so that even the translator failed, it still works
		except SystemExit:
			logger: Logger = getLogger("main._main.SystemExit_handler")
			logger.info("SystemExit. Bye.")
			
			print(r"Admin Exit -- Bye Bye! \(●'◡'●)/")
			quit()  # Raises SystemExit. This should not be caught by any try-except block
		
		except KeyboardInterrupt:
			# This will not catch any keyboard interrupt when handling errors
			logger: Logger = getLogger("main._main.KeyboardInterrupt_handler")
			logger.info("Keyboard interrupted")
			logger.info("Waiting for confirm")
			confirm: str = input("\n\nYou just pressed a special keystroke.\n"
			                     "You are going to quit this program. Are you sure about that? [y/N]")
			confirm: str = confirm.strip().upper()
			if confirm == 'Y':
				logger.info("Confirmed. Bye.")
				print("Got it. Have a nice day.")
				quit()  # Raises SystemExit. This should not be caught by any try-except block
			print("Confirmation failed. Restarting the program")
			logger.info("Confirmation failed. Restarting the program")
			_main()

		except RealExit as error:
			logger: Logger = getLogger("main._main.RealExit_handler")
			logger.error(f"Forced exit --- RealExit")
			logger.info("TRACEBACK STARTS")
			for error_message_line in format_exception(error):
				error_message_line: str = error_message_line.strip()
				error_message_row_list: list[str] = error_message_line.split('\n')
				for error_message_row in error_message_row_list:
					logger.error(error_message_row)
			logger.info("TRACEBACK ENDS")
			
			raise error  # This should also not be caught by any try-except block
		
		except Exception as error:
			exception_list.append(error)
			
			logger: Logger = getLogger("main._main.Exception_handler")
			logger.critical(f"ERROR --- {error.__class__.__name__}")
			logger.info("TRACEBACK STARTS")
			for error_message_line in format_exception(error):
				error_message_line: str = error_message_line.strip()
				error_message_row_list: list[str] = error_message_line.split('\n')
				for error_message_row in error_message_row_list:
					logger.critical(error_message_row)
			logger.info("TRACEBACK ENDS")
			logger.info("Main function will be executed again")
			
			print(f"Sorry! Something went wrong! :(        {error.__class__.__name__}")
			for i in range(5, 0, -1):
				print(f"\rThis system will be restarted after {i} second{'s' if i > 1 else ''}...", end='')
				sleep(1)
			_main()

	_main()
