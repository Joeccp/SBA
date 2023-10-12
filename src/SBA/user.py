"""User mode"""

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


from datetime import datetime
from logging import getLogger, Logger
from string import ascii_uppercase
from time import sleep
from typing import Optional
from webbrowser import open as openWebBrowser

from .colour import Colour, column_colour, row_colour
from .house import House, Ticket
from .language import inputLang, printLang
from .utils import clearScreen, saveData

message: str = ""


def buyTicket() -> None:
	"""
	User Mode 1: Buy Ticket

	:return: None
	"""
	from .colour import normal_colour
	from .language import language
	
	global message
	
	logger: Logger = getLogger("buyTicket")
	logger.info("User Mode 1: Buy a ticket")
	clearScreen()
	printLang("CINEMA KIOSK SYSTEM\n\n\n\n\n\n\n", "電影售票系統\n\n\n\n\n\n\n")
	printLang("House(s) available:", "可選的電影院：")
	total_available_house_count: int = 0
	for house in House.houses_table.values():
		if house.movie and house.n_available != 0:
			printLang(f"House {house.house_number}: {house.movie:<50} {house.n_available}/{house.n_seat}",
			          f"電影院{house.house_number}：{house.movie:<50} {house.n_available}/{house.n_seat}")
			total_available_house_count += 1
	if total_available_house_count == 0:
		if language == "ENGLISH":
			message = "Sorry, no house available now"
		else:
			message = "抱歉，現在沒有可選的電影院"
		return
	printLang("\nPlease enter the house number (or hit Enter to go back to the main menu):",
	          "\n請輸入電影院號碼（或按 Enter 以返回主頁面）")
	logger.info("Waiting house number input")
	house_num_str: str = input("-> ").strip()
	if house_num_str == '':
		message = ''
		logger.info("Empty house number, going back to the user menu")
		return
	if not house_num_str.isdecimal():
		if language == "ENGLISH":
			message = "ERROR: House number can only be decimal numbers"
		else:
			message = "錯誤：電影院號碼必須爲數字"
		logger.info("Invalid house number, going back to the user menu")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table.keys():
		if language == "ENGLISH":
			message = "ERROR: That house does not exist"
		else:
			message = "錯誤：無此電影院"
		logger.info("Invalid house number, going back to the user menu")
		return
	house: House = House.houses_table[house_num]
	logger.info(f"User selected house {house_num}")
	clearScreen()
	printLang(f"House {house.house_number} is now playing: {house.movie}",
	          f"電影院{house.house_number} 正在播映：{house.movie}")
	house.printSeatingPlan()
	
	printLang(
		f"\nEnter the {row_colour}row{normal_colour} and {column_colour}column{normal_colour} number of the seat"
		f"(or just hit Enter to go back to the main menu):",
		f"\n請輸入座位的{row_colour}行數{normal_colour}和{column_colour}列數{normal_colour}"
		f"（或按 Enter 以返回主頁面）"
	)
	logger.info("Waiting seat coordinate input")
	coor: str = input("\n-> ").strip().upper().replace(" ", '')
	if coor == '':
		message = ''
		logger.info("Empty coordinate, going back to the user menu")
		return
	if len(coor) == 1:
		logger.info("Invalid coordinate, going back to the user menu")
		if language == "ENGLISH":
			message = "ERROR: Invalid format of the seat number"
		else:
			message = "錯誤：無效座位坐標格式"
		return
	if coor[-1] not in ascii_uppercase:
		logger.info("Invalid coordinate, going back to the user menu")
		if language == "ENGLISH":
			message = f"ERROR: {column_colour}Column{normal_colour} index is not a character"
		else:
			message = f"錯誤：座位{column_colour}列數{normal_colour}必須是英文字母"
		return
	column_str: str = coor[-1]
	column_int: int = ord(column_str) - 65
	if column_int >= house.n_column:
		logger.info("Invalid coordinate, going back to the user menu")
		if language == "ENGLISH":
			message = f"ERROR: Invalid {column_colour}column{normal_colour}"
		else:
			message = f"錯誤：無效座位{column_colour}行數{normal_colour}"
		return
	row_str: str = coor[:-1]
	if len(row_str) > 2:
		logger.info("Invalid coordinate, going back to the user menu")
		if language == "ENGLISH":
			message = f"ERROR: Impossible {row_colour}row{normal_colour} number"
		else:
			message = f"錯誤：不可能的{row_colour}行數{normal_colour}"
		return
	row_int: int = int(row_str) - 1
	if house.seating_plan[row_int][column_int] != 0:
		logger.info("Seat already sold, going back to the user menu")
		if language == "ENGLISH":
			message = "Sorry, the seat is not available"
		else:
			message = "抱歉，該座位不予發售"
		return
	house.seating_plan[row_int][column_int] = 1
	House.total_tickets += 1
	ticket_index: int = House.total_tickets
	ticket_number: str = f"T{ticket_index:0>5}"
	time: str = datetime.now().isoformat(timespec="seconds")
	ticket: Ticket = (
		ticket_index, ticket_number, time, house.house_number, house.movie, row_int, column_int
	)
	printLang("Your ticket:", "你的電影票如下：")
	printLang(f"{ticket_number:<6} @{time}: "
	          f"House {house.house_number:<2} -- {house.movie:<50} ~"
	          f"Seat<{row_colour}{row_int + 1}{column_colour}{chr(column_int + 65)}{normal_colour}>",
	          f"{ticket_number:<6} @{time}: "
	          f"電影院{house.house_number:<2} -- {house.movie:<50} ~"
	          f"座位<{row_colour}{row_int + 1}{column_colour}{chr(column_int + 65)}{normal_colour}>"
	          )
	logger.info("User has successfully bought a ticket")
	logger.info(f"Ticket info: {ticket}")
	House.tickets_table.append(ticket)
	saveData()
	printLang("\n\nThank you for your purchase!", "\n\n感謝您的購買！")
	inputLang("\nHit Enter to go back to the main menu", "按 Enter 以返回主頁面")
	message = ""


def checkTicket() -> None:
	"""
	User Mode 2: Check Ticket
	
	:return: None
	"""
	from .colour import normal_colour
	from .language import language
	
	global message
	
	logger: Logger = getLogger("checkTicket")
	logger.info("User Mode 2: Check ticket information")
	clearScreen()
	printLang("CINEMA KIOSK SYSTEM\n\n\n\n\n\n\n", "電影售票系統\n\n\n\n\n\n\n")
	if not House.tickets_table:
		if language == "ENGLISH":
			message = "Sorry, there are no tickets"
		else:
			message = "抱歉，現在沒有任何電影票"
		logger.info("No tickets, going back to the user menu")
		return
	printLang("Please enter your ticket number (starts with 'T'):",
	          "請輸入你的電影票號碼（由「T」開始）")
	logger.info("Waiting ticket number input")
	ticket_number: str = input("-> ").strip().upper()
	if ticket_number == "":
		message = ""
		logger.info("Empty ticket number, going back to the user menu")
		return
	if not ticket_number.startswith('T'):
		if language == "ENGLISH":
			message = "ERROR: Invalid ticket number format -- ticket number starts with 'T'"
		else:
			message = "錯誤：無效電影票號碼——電影票號碼由「T」開始"
		logger.info("Invalid ticket number, going back to the user menu")
		return
	if ticket_number == 'T':
		if language == "ENGLISH":
			message = "ERROR: Invalid ticket number -- ticket number has no decimal numbers"
		else:
			message = "錯誤：無效的電影票號碼——電影票號碼必須有數字"
		logger.info("Invalid ticket number, going back to the user menu")
		return
	if len(ticket_number) < 6:
		if language == "ENGLISH":
			message = "ERROR: Invalid ticket number -- ticket number too short"
		else:
			message = "錯誤：無效電影票號碼——電影票號碼太短"
		logger.info("Invalid ticket number, going back to the user menu")
		return
	if not ticket_number[1:].isdecimal():
		if language == "ENGLISH":
			message = ("ERROR: Invalid ticket number -- "
			           "ticket number should ba a single character 'T' followed by decimal numbers")
		else:
			message = "錯誤：無效電影票號碼——電影票號碼由「T」開始然後是數字"
		logger.info("Invalid ticket number, going back to the user menu")
		return
	if len(ticket_number) > 6 and ticket_number[1] == '0':
		if language == "ENGLISH":
			message = "ERROR: Invalid ticket number -- more than 4 leading zeros"
		else:
			message = "錯誤：無效電影票號碼——電影票號碼的前置零不可有多於四位"
		logger.info("Invalid ticket number, going back to the control panel menu")
		return
	if set(ticket_number[1:]) == {'0'}:
		if language == "ENGLISH":
			message = "ERROR: Invalid ticket number -- ticket number is all zero"
		else:
			message = "錯誤：無效電影票號碼——電影票號碼不可全部爲零"
		logger.info("Invalid ticket number, going back to the control panel menu")
		return
	print()
	ticket_index: int = int(ticket_number[1:])
	ticket: Optional[Ticket] = House.searchTicket(ticket_index)
	if ticket is None:
		logger.info("No such ticket, going back to the user menu")
		printLang("No such ticket", "無此電影票")
		print("\n\n")
		inputLang("Hit enter to go back to the main menu",
		          "按 Enter 以返回主頁面")
		message = ""
		return
	ticket_index, ticket_no, time, house_no, movie, row_index, column_index = ticket
	printLang(f"{ticket_no:<6} @{time} "
	          f"House {house_no:<2} -- {movie:<30} ~ "
	          f"Seat<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}>",
	          f"{ticket_no:<6} @{time} "
	          f"電影院{house_no:<2} -- {movie:<30} ~ "
	          f"座位<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}>"
	          )
	print("\n\n")
	inputLang("\nHit Enter to go back to the main menu", "按 Enter 以返回主頁面")
	message = ""


def ticketRefund() -> None:
	"""
	User Mode 3: Ticket Refund

	:return: None
	"""
	from .colour import normal_colour
	from .language import language
	
	global message
	
	logger: Logger = getLogger("ticketRefund")
	logger.info("User Mode 3: Ticket refund")
	clearScreen()
	printLang("CINEMA KIOSK SYSTEM\n\n\n\n\n\n\n\n\n\n\n\n",
	          "電影售票系統\n\n\n\n\n\n\n\n\n\n\n\n")
	if not House.tickets_table:
		if language == "ENGLISH":
			message = "Sorry, there are no tickets"
		else:
			message = "抱歉，現在沒有任何電影票"
		logger.info("No tickets, going back to the user menu")
		return
	printLang("Please enter your ticket number (starts with 'T'):",
	          "請輸入你的電影票號碼（由「T」開始）")
	logger.info("Waiting ticket number input")
	ticket_number: str = input("-> ").strip().upper().replace(' ', '')
	if ticket_number == "":
		logger.info("Empty ticket number, going back to the user menu")
		message = ""
		return
	if not ticket_number.startswith('T'):
		logger.info("Invalid ticket number, going back to the user menu")
		if language == "ENGLISH":
			message = "ERROR: Invalid ticket number format -- ticket number starts with 'T'"
		else:
			message = "錯誤：無效電影票號碼——電影票號碼由「T」開始"
		return
	if ticket_number == 'T':
		logger.info("Invalid ticket number, going back to the user menu")
		if language == "ENGLISH":
			message = "ERROR: Invalid ticket number -- ticket number has no decimal numbers"
		else:
			message = "錯誤：無效的電影票號碼——電影票號碼必須有數字"
		return
	if len(ticket_number) < 6:
		logger.info("Invalid ticket number, going back to the user menu")
		if language == "ENGLISH":
			message = "ERROR: Invalid ticket number -- ticket number too short"
		else:
			message = "錯誤：無效電影票號碼——電影票號碼太短"
		return
	if not ticket_number[1:].isdecimal():
		logger.info("Invalid ticket number, going back to the user menu")
		if language == "ENGLISH":
			message = ("ERROR: Invalid ticket number -- "
			           "ticket number should ba a single character 'T' followed by decimal numbers")
		else:
			message = "錯誤：無效電影票號碼——電影票號碼由「T」開始然後是數字"
		return
	if len(ticket_number) > 6 and ticket_number[1] == '0':
		if language == "ENGLISH":
			message = "ERROR: Invalid ticket number -- more than 4 leading zeros"
		else:
			message = "錯誤：無效電影票號碼——電影票號碼的前置零不可有多於四位"
		logger.info("Invalid ticket number, going back to the control panel menu")
		return
	if set(ticket_number[1:]) == {'0'}:
		if language == "ENGLISH":
			message = "ERROR: Invalid ticket number -- ticket number is all zero"
		else:
			message = "錯誤：無效電影票號碼——電影票號碼不可全部爲零"
		logger.info("Invalid ticket number, going back to the control panel menu")
		return
	print()
	ticket_index: int = int(ticket_number[1:])
	ticket: Optional[Ticket] = House.searchTicket(ticket_index)
	if ticket is None:
		logger.info("No such ticket, going back to the user menu")
		printLang("No such ticket", "無此電影票")
		print("\n\n")
		inputLang("Hit enter to go back to the main menu",
		          "按 Enter 以返回主頁面")
		message = ""
		return
	ticket_index, ticket_no, time, house_no, movie, row_index, column_index = ticket
	logger.info(f"User want to delete this ticket: {ticket}")
	printLang(f"{ticket_no:<6} @{time} "
	          f"House {house_no:<2} -- {movie:<30} ~ "
	          f"Seat<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}>",
	          f"{ticket_no:<6} @{time} "
	          f"電影院{house_no:<2} -- {movie:<30} ~ "
	          f"座位<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}>"
	          )
	printLang("\nAre you sure you want to get refund of this ticket? (y/N)",
	          "\n你確定要為此電影票退款嗎？（y/N）")
	logger.info("Confirming")
	confirm: str = input("-> ").strip().upper()
	if confirm == 'Y':
		House.houses_table[house_no].seating_plan[row_index][column_index] = 0
		House.tickets_table.remove(ticket)
		logger.info("Ticket deleted")
		saveData()
		printLang("\nRefund succeed!", "\n退款成功！")
		message = ''
		return
	else:
		logger.info("Confirmation failed, go back to the user menu")
		print()
		if language == "ENGLISH":
			message = "Confirmation failed. Refund Failed"
		else:
			message = "確認失敗，退款失敗"
		return


def userMode() -> None:
	"""
	User mode
	:return: None
	"""
	from .colour import normal_colour
	from .language import language
	
	global message
	
	message = ""
	while True:
		logger: Logger = getLogger("userMode")
		logger.info("Entered the user menu")
		clearScreen()
		printLang("CINEMA KIOSK SYSTEM\n\n\n", "電影售票系統\n\n\n")
		print(Colour.RED + message + normal_colour + "\n\n\n")
		for house in House.houses_table.values():
			if house.movie:
				printLang(
					f"House {house.house_number}: {house.movie:<50} "
					f"{Colour.GREEN if house.n_available > 0 else Colour.RED}{house.n_available}{normal_colour}"
					f"/{house.n_seat}",
					f"電影院{house.house_number}：{house.movie:<50} "
					f"{Colour.GREEN if house.n_available > 0 else Colour.RED}{house.n_available}{normal_colour}"
					f"/{house.n_seat}"
				)
		printLang(
			"\n"
			"0: LOG OUT\n"
			"1: Buy a ticket\n"
			"2: Check ticket information\n"
			"3: Ticket refund\n"
			"4: HELP\n"
			"Please select a mode ([0-4]):",
			"\n"
			"0：登出\n"
			"1：買票\n"
			"2：查票\n"
			"3：退款\n"
			"4：教學\n"
			"請選擇模式 ([0-4])："
		)
		logger.info("Waiting mode code input")
		mode: str = input("-> ").strip()
		if not mode.isdecimal():
			if language == "ENGLISH":
				message = "ERROR: Mode number should be a decimal number."
			else:
				message = "錯誤：模式代碼必須全部都是數字"
			logger.info("Invalid mode code")
			continue
		
		if mode == '0':
			logger: Logger = getLogger("userMode.mode_0")
			logger.info("User Mode 0: Log out")
			logger.info("USER LOGOUT")
			for i in range(3, 0, -1):
				printLang(f"\rYou will be logged out after {i} seconds...",
				          f"\r你將會於{i}秒後登出......",
				          end='')
				sleep(1)
			return
		
		elif mode == '1':
			buyTicket()  # Buy ticket
		
		elif mode == '2':
			checkTicket()  # Check ticket
		
		elif mode == '3':
			ticketRefund()  # Ticket refund
		
		# HELP
		elif mode == '4':
			logger: Logger = getLogger("userMode.mode_4")
			logger.info("User Mode 4: Help")
			openWebBrowser("https://joeccp.github.io/SBA/")
			logger.info("Opened a website browser and visit https://joeccp.github.io/SBA/")
		
		else:
			logger.info("Unknown mode code")
			if language == "ENGLISH":
				message = "ERROR: Unknown mode"
				if mode.startswith('0'):
					message = message + ". Did you accidentally enter any leading zeros?"
			else:
				message = "錯誤：無效模式代碼"
				if mode.startswith('0'):
					message = message + "。你可能輸入了不需要的前置零。"
			continue
