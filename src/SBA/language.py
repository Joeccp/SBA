"""Language"""

#  Copyright 2023 Joe Chau
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from logging import getLogger, Logger
from typing import Literal


language: Literal['CHINESE', 'ENGLISH'] = 'ENGLISH'


def setLanguage(language_: Literal['CHINESE', 'ENGLISH']) -> None:
	"""
	Change the language
	
	:param language_: The language code
	:type language_: Literal['CHINESE', 'ENGLISH']
	:return: None
	"""
	global language
	
	logger: Logger = getLogger('changeLanguage')
	logger.info("Changing the language")
	
	if language_ not in ['CHINESE', 'ENGLISH']:
		logger.info(f"Unknown language: {language_}, set to ENGLISH as default")
		language_: Literal['CHINESE', 'ENGLISH'] = 'ENGLISH'
	
	logger.info(f"Setting the language to {language_}")
	language = language_
	

def printLang(english_message: str = '', chinese_message: str = '', /, **kwargs) -> None:
	"""
	Print the message with the correct language
	
	NOTE: The 'sep' argument should not be used. printLang() does not have the *args argument!
	
	:param english_message: The English message that you want to print it out. Position-only parameter.
	:type english_message: str
	:param chinese_message: The Chinese message that you want to print it out. Position-only parameter.
	:type chinese_message: str
	:param kwargs: The same keyword arguments that are used for print(), but should not contain `sep`
	:return: None
	"""
	# Only important log message should be logged with this logger,
	# to prevent spamming the log file
	logger: Logger = getLogger('printLang')
	
	if 'sep' in kwargs.keys():
		logger.warning("`sep` ARGUMENT DETECTED!")
	
	if language == 'ENGLISH':
		print(english_message, **kwargs)
	else:
		print(chinese_message, **kwargs)


def inputLang(english_message: str = '', chinese_message: str = '', /) -> str:
	"""
	Input with a message of the correct language
	
	:param english_message: The English message that you want to print it out as a input message.
		Position-only parameter.
	:type english_message: str
	:param chinese_message: The Chinese message that you want to print it out as a input message.
		Position-only parameter.
	:type chinese_message: str
	:return: The input string
	:rtype: str
	"""
	# No important log message = no need new logger
	
	if language == 'ENGLISH':
		ret: str = input(english_message)
	else:
		ret: str = input(chinese_message)
	return ret
