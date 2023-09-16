"""Admin mode -- Control Panel"""

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
from os import path, remove
from typing import Optional
from webbrowser import open as openWebBrowser  # NOQA: lowercase function imported as uppercase function

from .coorutils import Coor, CoordinateExpressionException, getCoorsFromCoorExpr
from .colour import setColour
from .house import House, Ticket
from .language import inputLang, printLang, setLanguage
from .utils import clearScreen, loadData, saveData


def createHouse() -> None:
	"""
	Admin mode 1: Create a new house

	:return: None
	"""
	logger: Logger = getLogger("createHouse")
	logger.info("Admin Mode 1: Create a new house")
	printLang(f"House {House.n_House + 1} will be the new house",
	          f"新的電影院將會是：電影院{House.n_House + 1}")
	logger.info("Waiting number of rows input")
	n_row_str: str = inputLang(f"Enter how many row does House {House.n_House + 1} has (1-99): ",
	                           f"請輸入電影院{House.n_House + 1}將會有多少行座位 （1-99）： ").strip()
	if not n_row_str.isdecimal():
		printLang("ERROR: Number of rows must be decimal number",
		          "錯誤：行數必須爲數字")
		printLang("House creation failed, exiting to Control Panel menu...",
		          "電影院創建失敗，返回控制面板中......")
		logger.info("Invalid number of rows, going back to the control panel menu")
		return
	n_row: int = int(n_row_str)
	if n_row > 99 or n_row == 0:
		printLang("ERROR: Number of rows out of possible range",
		          "錯誤：行數超出範圍")
		printLang("House creation failed, exiting to Control Panel menu...",
		          "電影院創建失敗，返回控制面板中......")
		logger.info("Number of rows out of possible range, going back to the Control Panel menu")
		return
	logger.info("Waiting number of columns input")
	n_col_str: str = inputLang(f"Enter how many column does House {House.n_House + 1} has (1-26): ",
	                           f"請輸入電影院{House.n_House + 1}將會有多少列座位（1-26）").strip()
	if not n_col_str.isdecimal():
		printLang("ERROR: Number of columns must be decimal number",
		          "錯誤：列數必須爲數字")
		printLang("House creation failed, exiting to Control Panel menu...",
		          "電影院創建失敗，返回控制面板中......")
		logger.info("Invalid number of columns, going back to the Control Panel menu")
		return
	n_col: int = int(n_col_str)
	if n_col > 26 or n_col == 0:
		printLang("ERROR: Number of columns out of possible range",
		          "錯誤：列數超出範圍")
		printLang("House creation failed, exiting to Control Panel menu...",
		          "電影院創建失敗，返回控制面板中......")
		logger.info("Number of columns out of possible range, going back to the Control Panel menu")
		return
	house: House = House(row_number=n_row, column_number=n_col)
	logger.info("Waiting movie name input")
	movie: str = inputLang("Please enter the movie name (or leave it blank if the house is closed): ",
	                       "請輸入電影名稱（或者留空以代表電影院關閉）:").strip()
	if movie == '':
		pass
	else:
		house.movie = movie
	logger.info(f"House {house.house_number}'s movie: {movie or '(None)'}")
	printLang("Success!", "成功！")
	saveData()


def updateMovie() -> None:
	"""
	Admin mode 2: Update the movie of a house

	:return: None
	"""
	logger: Logger = getLogger("updateMovie")
	logger.info("Admin Mode 2: Update the movie of a house")
	if house_list := House.houses_table.values():
		printLang("House list:", "電影院列表：")
		for house in house_list:
			if house.movie:
				printLang(f"House {house.house_number} now playing: {house.movie}",
				          f"電影院{house.house_number} 正在播映：{house.movie}")
			else:
				printLang(f"House {house.house_number} is closed",
				          f"電影院{house.house_number} 已關閉")
	else:
		printLang("No house", "無電影院")
		return
	logger.info("Waiting house number input")
	house_num_str: str = inputLang("Please select the house:\n-> ", "請選擇電影院：").strip()
	if not house_num_str.isdecimal():
		printLang("ERROR: House number can only be decimal number",
		          "錯誤：電影院號碼必須爲數字")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		logger.info("Invalid house number, going back to the Control Panel menu")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table.keys():
		printLang('ERROR: No such house', "錯誤：無此電影院")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		logger.info("No such house, going back to the Control Panel menu")
		return
	house: House = House.houses_table[house_num]
	movie: str = inputLang("Please enter the movie name (or leave it blank if no movie will be played): ",
	                       "請輸入電影名稱（或者留空以代表電影院關閉）:").strip()
	old_movie: str = house.movie
	house.movie = movie
	printLang(f"Successfully changed the movie in house {house.house_number}!",
	          f"已成功更改電影院{house.house_number} 的電影名稱！")
	printLang(f"{old_movie or '(None)'} --> {house.movie}",
	          f"{old_movie or '（無）'} --> {house.movie}")
	logger.info(f"Movie of House {house.house_number}: {old_movie or '(None)'} --> {house.movie}")
	do_clean: str = inputLang("Would you like to clear all relevant data too? (y/N)",
	                          "你想清除此電影院的所有相關資料嗎? (y/N)").strip().upper()
	if do_clean == 'Y':
		logger.info("Admin wants to clear all relevant data")
		printLang(f"Clearing all seat of house {house_num}",
		          f"正在清除電影院{house_num} 的所有相關資料")
		house.clearPlan()
		printLang("Success!", "成功！")
		printLang("Deleting all related tickets", "正在刪除相關的電影票")
		logger.info("Clearing all related tickets")
		n_tickets_removed: int = 0
		for ticket in House.tickets_table:
			ticket_index, ticket_no, time, house_no, *other_information = ticket
			if house_no == house.house_number:
				House.tickets_table.remove(ticket)
				n_tickets_removed += 1
		print(f"Removed {n_tickets_removed} tickets", f"刪除了{n_tickets_removed}張電影票")
		logger.info(f"Removed {n_tickets_removed} tickets")
		saveData()
		return
	elif do_clean == 'N':
		print("OK")
		saveData()
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	else:
		printLang("ERROR: Invalid confirmation, did not clean all data as default",
		          "錯誤：無效確認，預設沒有清除所有相關資料")
		saveData()
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return


def checkHousesInformation() -> None:
	"""
	Admin mode 5: Check houses information

	:return: None
	"""
	logger: Logger = getLogger("checkHousesInformation")
	logger.info("Admin Mode 5: Check houses information")
	if House.houses_table:
		printLang("House list", "電影院列表")
		for house in House.houses_table.values():
			printLang(f"House {house.house_number}: {house.movie if house.movie else '(None)':<50} "
			          f"{house.n_available}/{house.n_seat}",
			          f"電影院{house.house_number}：{house.movie if house.movie else '（無）}':<50} "
			          f"{house.n_available}/{house.n_seat}"
			          )
	else:
		printLang("No house", "無電影院")
		return
	print()
	logger.info("Waiting house number input")
	house_num_str: str = inputLang("Select a house (Just hit enter to go back to the Control Panel):\n-> ",
	                               "請選擇電影院（或按 Enter 以返回控制面板）:\n-> ")
	if house_num_str == '':
		return
	if not house_num_str.isdecimal():
		printLang("ERROR: House number can only be decimal number",
		          "錯誤：電影院號碼必須爲數字")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table.keys():
		printLang("ERROR: No such house", "錯誤：無此電影院")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	logger.info(f"Viewing house {house_num} data")
	house: House = House.houses_table[house_num]
	printLang(f"House {house.house_number} is now playing: {house.movie}",
	          f"電影院{house.house_number} 正在播映: {house.movie}")
	house.printSeatingPlan()


def seatStatusOverride() -> None:
	"""
	Admin Mode 6: Seat status override

	:return: None
	"""
	logger: Logger = getLogger("seatStatusOverride")
	logger.info("Admin Mode 6: Seat status override")
	printLang("Note: Seats brought / reserved / emptied from this control panel "
	          "DO NOT have / WILL NOT delete a ticket.",
	          "注意：任何透過本模式對座位狀態的更改"
	          "都不會更動電影票")
	printLang("Staffs should check the status of the seat manually before changing the status of a seat.",
	          "職員在覆蓋座位狀態前，應該先自行查詢原來的座位狀態")
	printLang("The mode will NOT check the seat status for you.",
	          "本模式不會幫你檢查原來的座位狀態")
	printLang("Command format:\n\n"
	          "(EMPTY | BUY | RESERVE) - <House number> - <Coordinate Expression> \n"
	          "(or hit Enter to go back to the Control Panel menu)",
	          "指令格式:\n\n"
	          "(EMPTY | BUY | RESERVE) - <電影院號碼> - <坐標表達式> \n"
	          "（或按 Enter 以返回控制面板）"
	          )
	logger.info("Waiting command input")
	command: str = (input("-> ")
	                .strip()
	                .upper()
	                .replace(' ', '')
	                .replace('<', '')  # Prevent confusion due to the command format
	                .replace('>', '')
	                .replace('(', '')
	                .replace(')', '')
	                .replace('（', '')  # Same as above, but Chinese
	                .replace('）', '')
	                .replace('《', '')
	                .replace('》', '')
	                .replace('|', '')  # <-- This too? Really?
	                .replace('—', '-')  # Chinese input
	                )
	if command == '':
		logger.info("Empty command, going back to the Control Panel menu")
		return
	command_list: list[str] = command.split('-')
	if len(command_list) != 3:
		logger.info('Invalid command, going back to the Control Panel menu')
		printLang("ERROR: Invalid command", "錯誤：無效指令")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	action: str = command_list[0]
	match action:
		case 'EMPTY':
			seat_status: int = 0
		case 'BUY':
			seat_status: int = 1
		case 'RESERVE':
			seat_status: int = 2
		case _:
			logger.info('Invalid action, going back to the Control Panel menu')
			printLang("ERROR: Unknown action", "錯誤：無效覆蓋動作")
			printLang("Going back to the Control Panel menu...",
			          "返回控制面板中......")
			return
	house_num_str: str = command_list[1]
	if not house_num_str.isdecimal():
		logger.info('Invalid command, going back to the Control Panel menu')
		printLang("ERROR: Invalid house number", "錯誤：無效電影院號碼")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table:
		logger.info('Invalid command, going back to the Control Panel menu')
		printLang("ERROR: Invalid house number", "錯誤：無效電影院號碼")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	house: House = House.houses_table[house_num]
	coor_expr: str = command_list[2]
	try:
		coor_list: list[Coor] = getCoorsFromCoorExpr(
			coor_expr, n_row=house.n_row, n_column=house.n_column
		)
	except CoordinateExpressionException as error:  # NOQA
		logger.info(f'Invalid command: {error.__doc__}. '
		            'Going back to the Control Panel menu')
		printLang(f"ERROR: {error.__doc__}", f"錯誤：{error.chinese_msg}")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	else:
		if len(coor_list) == 1:
			coor, = coor_list
			row, column = coor
			logger.info(f"{action} House {house.house_number} {row + 1} {chr(column + 65)}")
			logger.debug(f"house.seating_plan[{row}][{column}]: "
			             f"{house.seating_plan[row][column]} --> {seat_status}")
			house.seating_plan[row][column] = seat_status
			printLang("Success!\n", "成功！\n")
			return
		
		for coor in coor_list:
			row: int
			column: int
			row, column = coor
			logger.info(f"{action} House {house.house_number} {row + 1} {chr(column + 65)}")
			logger.debug(f"house.seating_plan[{row}][{column}]: "
			             f"{house.seating_plan[row][column]} --> {seat_status}")
			house.seating_plan[row][column] = seat_status
		printLang("Success!\n", "成功！\n")
		printLang(f"{len(coor_list)} seats overwritten.",
		          f"{len(coor_list)}個座位的狀態已被覆蓋")
		logger.info(f"{len(coor_list)} seats overwritten.")
	finally:
		saveData()


def checkTicketInformation() -> None:
	"""
	Admin Mode 7: Check ticket information

	:return: None
	"""
	logger: Logger = getLogger("checkTicketInformation")
	logger.info("Admin Mode 7: Check ticket information")
	printLang('Enter the ticket number to see the information about that ticket,\n'
	          'or hit enter to see all ticket information',
	          '輸入電影票號碼以查詢相關資料，\n'
	          '（或按 Enter 以查看所有電影票的資料）'
	          )
	ticket_number: str = input("-> ").strip().upper().replace(' ', '')
	if ticket_number == '':
		ticket_count: int = 0
		for ticket in House.tickets_table:
			ticket_index, ticket_no, time, house_no, movie, row_index, column_index = ticket
			print(f"{ticket_no:<6} @{time} "
			      f"House {house_no:<2} -- {movie:<50} ~"
			      f"Seat<{row_index + 1}{chr(column_index + 65)}>",
			      f"{ticket_no:<6} @{time} "
			      f"電影院{house_no:<2} -- {movie:<50} ~"
			      f"座位<{row_index + 1}{chr(column_index + 65)}>"
			      )
			ticket_count += 1
		if ticket_count == 0:
			printLang("No ticket", "無電影票")
	else:
		if len(ticket_number) < 6:
			printLang("ERROR: Invalid ticket number -- ticket number too short",
			          "錯誤：無效電影票號碼——電影票號碼太短")
			printLang("Going back to the Control Panel menu...",
			          "返回控制面板中......")
			logger.info("Invalid ticket number, going back to the Control Panel menu")
			return
		if not ticket_number.startswith('T'):
			printLang("ERROR: Invalid ticket number format -- ticket number starts with 'T'",
			          "錯誤：無效電影票號碼——電影票號碼由「T」開始")
			printLang("Going back to the Control Panel menu...",
			          "返回控制面板中......")
			logger.info("Invalid ticket number, going back to the Control Panel menu")
			return
		if not ticket_number[1:].isdecimal():
			printLang("ERROR: Invalid ticket number -- "
			          "ticket number should ba a single character 'T' followed by decimal numbers",
			          "錯誤：無效電影票號碼——電影票號碼由「T」開始然後是數字")
			printLang("Going back to the Control Panel menu...",
			          "返回控制面板中......")
			logger.info("Invalid ticket number, going back to the Control Panel menu")
			return
		if len(ticket_number) > 6 and ticket_number[1] == '0':
			printLang("ERROR: Invalid ticket number -- more than 4 leading zeros",
			          "錯誤：無效電影票號碼——電影票號碼的前置零不可有多於四位")
			printLang("Going back to the Control Panel menu...",
			          "返回控制面板中......")
			logger.info("Invalid ticket number, going back to the Control Panel menu")
			return
		if set(ticket_number[1:]) == {'0'}:
			printLang("ERROR: Invalid ticket number -- ticket number is all zero",
			          "錯誤：無效電影票號碼——電影票號碼不可全部爲零")
			printLang("Going back to the Control Panel menu...",
			          "返回控制面板中......")
			logger.info("Invalid ticket number, going back to the Control Panel menu")
			return
		ticket_index: int = int(ticket_number[1:])
		ticket: Optional[Ticket] = House.searchTicket(ticket_index)
		if ticket is None:
			printLang("ERROR: No such ticket", "無此電影票")
			logger.info("No such ticket, going back to the Control Panel menu")
			return
		ticket_index, ticket_no, time, house_no, movie, row_index, column_index = ticket
		logger.info(f"Admin wants to check this ticket: {ticket}")
		printLang(f"{ticket_no:<6} @{time} "
		          f"House {house_no:<2} -- {movie:<50} ~"
		          f"Seat<{row_index + 1}{chr(column_index + 65)}>",
		          f"{ticket_no:<6} @{time} "
		          f"電影院{house_no:<2} -- {movie:<50} ~"
		          f"座位<{row_index + 1}{chr(column_index + 65)}>")
	printLang(f"TOTAL: {House.get_n_tickets()} ticket{'s' if House.get_n_tickets() > 1 else ''} active, "
	          f"{House.total_tickets} ticket{'s' if House.total_tickets > 1 else ''} were created.",
	          f"纍計：{House.get_n_tickets()}張電影票有效，曾有{House.total_tickets}張電影票存在過。")


def deleteTicket() -> None:
	"""
	Admin mode 8: Delete a ticket

	:return: None
	"""
	logger: Logger = getLogger("deleteTicket")
	logger.info("Admin Mode 8: Delete a ticket")
	logger.info("Waiting ticket number input")
	printLang("Please enter the ticket number (starts with 'T'):",
	          "請輸入電影票號碼（由「T」開始）：")
	ticket_number: str = input("-> ").strip().upper().replace(' ', '')
	if len(ticket_number) < 6:
		printLang("ERROR: Invalid ticket number -- ticket number too short",
		          "錯誤：無效電影票號碼——電影票號碼太短")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		logger.info("Invalid ticket number, going back to the Control Panel menu")
		return
	if not ticket_number.startswith('T'):
		printLang("ERROR: Invalid ticket number format -- ticket number starts with 'T'",
		          "錯誤：無效電影票號碼——電影票號碼由「T」開始")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		logger.info("Invalid ticket number, going back to the Control Panel menu")
		return
	if not ticket_number[1:].isdecimal():
		printLang("ERROR: Invalid ticket number -- "
		          "ticket number should ba a single character 'T' followed by decimal numbers",
		          "錯誤：無效電影票號碼——電影票號碼由「T」開始然後是數字")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		logger.info("Invalid ticket number, going back to the Control Panel menu")
		return
	if len(ticket_number) > 6 and ticket_number[1] == '0':
		printLang("ERROR: Invalid ticket number -- more than 4 leading zeros",
		          "錯誤：無效電影票號碼——電影票號碼的前置零不可有多於四位")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		logger.info("Invalid ticket number, going back to the Control Panel menu")
		return
	if set(ticket_number[1:]) == {'0'}:
		printLang("ERROR: Invalid ticket number -- ticket number is all zero",
		          "錯誤：無效電影票號碼——電影票號碼不可全部爲零")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		logger.info("Invalid ticket number, going back to the Control Panel menu")
		return
	ticket_index: int = int(ticket_number[1:])
	ticket: Optional[Ticket] = House.searchTicket(ticket_index)
	if ticket is None:
		printLang("ERROR: No such ticket", "無此電影票")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		logger.info("Invalid ticket number, going back to the Control Panel menu")
		return
	ticket_index, ticket_no, time, house_no, movie, row_index, column_index = ticket
	logger.info(f"Admin wants to delete this ticket: {ticket}")
	printLang(f"{ticket_no:<6} @{time} "
	          f"House {house_no:<2} -- {movie:<50} ~"
	          f"Seat<{row_index + 1}{chr(column_index + 65)}>",
	          f"{ticket_no:<6} @{time} "
	          f"電影院{house_no:<2} -- {movie:<50} ~"
	          f"座位<{row_index + 1}{chr(column_index + 65)}>")
	logger.debug(f"Ticket info: {ticket}")
	House.houses_table[house_no].seating_plan[row_index][column_index] = 0
	House.tickets_table.remove(ticket)
	printLang("Successfully deleted this ticket", "已成功地刪除此電影票")
	logger.info(f"Ticket {ticket_no} deleted")
	saveData()
	logger.debug(f"Total: {House.get_n_tickets()} ticket{'s' if House.get_n_tickets() > 1 else ''} active")


def clearHouseSeats() -> None:
	"""
	Admin mode 9: Clear all the seats of a house

	:return: None
	"""
	logger: Logger = getLogger("clearHouseSeats")
	logger.info("Admin Mode 9: Clear all the seats of a house")
	printLang("House list:", "電影院列表：")
	for house in House.houses_table.values():
		if house.movie:
			printLang(f"House {house.house_number} now playing: {house.movie}",
			          f"電影院{house.house_number}正在播映：{house.movie}")
		else:
			printLang(f"House {house.house_number} is closed",
			          f"電影院{house.house_number}已關閉")
	logger.info("Waiting house number input")
	house_num_str: str = inputLang("Enter the house number of a house which you would like to empty:\n-> "
	                               "請輸入你想清空的電影院的號碼：\n->").strip()
	if not house_num_str.isdecimal():
		logger.info("Invalid house number, going back to the Control Panel menu")
		printLang("ERROR: House number can only be decimal number",
		          "錯誤：電影院號碼必須爲數字")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table.keys():
		logger.info("Invalid house number, going back to the control panel menu")
		printLang("ERROR: No such house", "無此電影院")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	house: House = House.houses_table[house_num]
	printLang(f"House {house_num}", f"電影院{house_num}")
	house.printSeatingPlan()
	logger.info(f"Waiting to confirm clear of all seat of House {house_num}")
	confirm: str = inputLang(
		"Please confirm you would like to clear all seats and tickets of this house (y/N): ",
		"請確認你先清除所有此電影院的所有座位及電影票（y/N）：").strip().upper()
	if confirm == '' or confirm == 'N':
		logger.info("Confirmation failed")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	elif confirm == 'Y':
		logger.info("Confirmed, clearing seating plan")
		printLang(f"Clearing all seat of house {house_num}", f"正在清除電影院{house_num}的所有座位")
		house.clearPlan()
		printLang("Deleting all related tickets", "正在刪除所有相關電影票")
		logger.info("Deleting all related tickets")
		n_tickets_removed: int = 0
		for ticket in House.tickets_table:
			ticket_index, ticket_num, *other_information = ticket
			if house_num == house.house_number:
				logger.info(f"Deleting {ticket_num}, ticket info: {ticket}")
				House.tickets_table.remove(ticket)
				n_tickets_removed += 1
		printLang(f"Removed {n_tickets_removed} ticket{'s' if n_tickets_removed > 1 else ''}",
		          f"刪除了{n_tickets_removed}張電影票")
		logger.info(f"Removed {n_tickets_removed} ticket{'s' if n_tickets_removed > 1 else ''}")
		saveData()
		return
	else:
		logger.info("Confirmation failed")
		printLang("ERROR: Invalid confirmation", "錯誤：無效確認")
		printLang("Confirmation failed", "確認失敗")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return


def deleteHouse() -> None:
	"""
	Admin mode 10: DELETE A HOUSE

	:return: None
	"""
	logger: Logger = getLogger('deleteHouse')
	logger.info("Admin mode 10: DELETE A HOUSE")
	printLang("House list:", "電影院列表:")
	house_count: int = 0
	for house in House.houses_table.values():
		if house.movie:
			printLang(f"House {house.house_number} now playing: {house.movie}",
			          f"電影院{house.house_number}正在播映：{house.movie}")
		else:
			printLang(f"House {house.house_number} is closed",
			          f"電影院{house.house_number}已關閉")
	if house_count == 0:
		logger.info("No house, Going back to the Control Panel menu...")
		printLang("No house", "無電影院")
		return
	logger.info("Waiting house number input")
	house_num_str: str = inputLang("Enter the house number of a house which you would like to delete:\n-> ",
	                               "請輸入你想刪除的電影院的號碼：\n-> ").strip()
	if not house_num_str.isdecimal():
		logger.info("Invalid house number, going back to the Control Panel menu")
		printLang("ERROR: House number can only be decimal number",
		          "錯誤；電影院號碼必須爲數字")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table.keys():
		logger.info("Invalid house number, going back to the Control Panel menu")
		printLang('ERROR: No such house', "錯誤：無此電影院")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	house: House = House.houses_table[house_num]
	printLang(f"House {house_num}", f"電影院{house_num}")
	house.printSeatingPlan()
	logger.info(f"Waiting to confirm clear of all seat of House {house_num}")
	confirm: str = inputLang("Please confirm you would like to delete this house (y/N): ",
	                         "請確認你想刪除這個電影院（y/N）：").strip().upper()
	if confirm == '' or confirm == 'N':
		logger.info("Confirmation failed")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	elif confirm == 'Y':
		logger.info("Confirmed, clearing seating plan")
		printLang(f"Clearing all seat of house {house_num}",
		          f"正在清除電影院{house_num} 的所有座位")
		house.clearPlan()
		printLang("Deleting all related tickets", "正在刪除所有相關的電影票")
		logger.info("Deleting all related tickets")
		n_tickets_removed: int = 0
		for ticket in House.tickets_table:
			ticket_index, ticket_num, *other_information = ticket
			if house_num == house.house_number:
				logger.info(f"Deleting {ticket_num}, ticket info: {ticket}")
				House.tickets_table.remove(ticket)
				n_tickets_removed += 1
		printLang(f"Removed {n_tickets_removed} ticket{'s' if n_tickets_removed > 1 else ''}",
		          f"刪除了{n_tickets_removed}張電影票")
		logger.info(f"Removed {n_tickets_removed} ticket{'s' if n_tickets_removed > 1 else ''}")
		printLang("Removing this house", "正在刪除此電影院")
		logger.info("Removing this house")
		del House.houses_table[house_num]
		printLang("Success!", "成功！")
		# No need House.house_num -= 1, as it is only for giving new house number
	else:
		logger.info("Confirmation failed")
		printLang("ERROR: Invalid confirmation", "錯誤：無效確認")
		printLang("Confirmation failed", "確認失敗")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return


def clearAllData() -> None:
	"""
	Admin Mode 11: CLEAR ALL DATA
	
	:return: None
	"""
	logger: Logger = getLogger("clearAllData")
	logger.info("Admin Mode 11: CLEAR ALL DATA")
	logger.info("Confirming")
	confirm: str = input("Please confirm you would like to clear ALL data (y/N): ").strip().upper()
	if confirm == '' or confirm == 'N':
		logger.info("Confirmation failed, going back to the Control Panel menu")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	elif confirm == 'Y':
		pass
	else:
		logger.info("Confirmation failed, going back to the Control Panel menu")
		printLang("ERROR: Invalid confirmation", "錯誤：無效確認")
		printLang("Confirmation failed", "確認失敗")
		printLang("Going back to the Control Panel menu...",
		          "返回控制面板中......")
		return
	House.tickets_table = []
	House.total_tickets = 0
	logger.info("Removed unsaved tickets data")
	printLang("Successfully removed unsaved tickets data", "成功刪除未儲存的電影票資料")
	try:
		logger.info("Finding any saved tickets data")
		absolute_path = path.dirname(__file__)
		relative_path = '../../data/tickets'
		full_path = path.join(absolute_path, relative_path)
		logger.debug(f"Full path = {full_path}")
		remove(full_path)
	except FileNotFoundError:
		logger.info("No saved tickets data")
		printLang("No saved tickets data", "沒有已儲存的電影票資料")
	else:
		logger.info("DELETED SAVED TICKETS DATA")
		printLang("Successfully deleted saved tickets data", "成功刪除已儲存的電影票資料")
	finally:
		logger.info("Process of removing tickets data finished")
		printLang("Process of removing tickets data finished", "刪除電影票資料之程序完結")
	House.houses_table = {}
	House.n_House = 0
	logger.info("Removed unsaved houses data")
	printLang("Successfully unsaved local houses data", "成功刪除未儲存的電影院資料")
	try:
		logger.info("Finding any saved houses data")
		absolute_path = path.dirname(__file__)
		relative_path = '../../data/houses'
		full_path = path.join(absolute_path, relative_path)
		remove(full_path)
	except FileNotFoundError:
		logger.info("No saved houses data")
		printLang("No saved houses data", "沒有已儲存的電影院資料")
	else:
		logger.info("DELETED SAVED HOUSES DATA")
		printLang("Successfully deleted saved houses data", "成功刪除已儲存的電影院資料")
	finally:
		logger.info("Process of removing houses data finished")
		printLang("Process of removing tickets houses finished", "刪除電影院資料之程序完結")
	logger.info("Resetting the colour scheme to DARK")
	printLang("Resetting the colour scheme to DARK", "正在重設配色為 DARK")
	setColour('DARK')
	try:
		logger.info("Finding the colour scheme setting file")
		absolute_path = path.dirname(__file__)
		relative_path = '../../data/colour.txt'
		full_path = path.join(absolute_path, relative_path)
		remove(full_path)
	except FileNotFoundError:
		logger.info("No colour scheme setting file")
		printLang("No colour scheme setting file", "沒有配色設定檔案")
	else:
		logger.info("DELETED COLOUR SCHEME SETTING FILE")
		printLang("Successfully deleted colour scheme setting file", "成功刪除配色設定檔案")
	finally:
		logger.info("Process of removing colour scheme setting file finished finished")
		printLang("Process of removing colour scheme setting file finished finished",
		          "刪除配色資料之程序完結")
	printLang("Finish!", "完成！")
	logger.info("Finished clearing all saved data!")


def changeColour() -> None:
	"""
	Admin Mode 14: Change the colour scheme
	
	:return: None
	"""
	from .colour import colour_mode
	
	logger: Logger = getLogger("changeColour")
	logger.info("Admin Mode 14: Change the colour scheme")
	if colour_mode == 'DARK':
		logger.info("The colour scheme is now DARK, changing to LIGHT...")
		setColour('LIGHT')
	elif colour_mode == 'LIGHT':
		logger.info("The colour scheme is now LIGHT, changing to DARK...")
		setColour('DARK')
	else:
		logger.warning("ERROR: Unknown colour scheme, changing to DARK anyway...")
		setColour('DARK')
	
	from .colour import colour_mode
	
	printLang(f"Success! The colour scheme is now {colour_mode}",
	          f"成功！現在的配色為：{colour_mode}")


def changeLanguage() -> None:
	"""
	Admin Mode 15: Change the language
	
	:return: None
	"""
	from .language import language
	
	logger: Logger = getLogger("changeLanguage")
	logger.info("Admin Mode 15: Change the language")
	
	if language == 'ENGLISH':
		logger.info("The language is now ENGLISH, changing to CHINESE...")
		setLanguage('CHINESE')
	elif language == 'CHINESE':
		logger.info("The language is now CHINESE, changing to ENGLISH...")
		setLanguage('ENGLISH')
	else:
		logger.warning("ERROR: Unknown language, changing to DARK anyway...")
		setLanguage('ENGLISH')
	
	printLang(
		"Success! The language is now ENGLISH",
		"成功！ 現在的語言為中文"
	)


def adminMode() -> None:
	"""
	Admin mode

	:return: None
	:raise SystemExit: To manually quit the entire program
	"""
	clearScreen()
	print("CINEMA KIOSK SYSTEM")
	print("CONTROL PANEL\n\n\n")
	while True:
		from .colour import normal_colour
		
		logger: Logger = getLogger("adminMode")
		logger.info("Entered main menu of the Control Panel")
		print(normal_colour)
		logger.info("Waiting mode code input")
		printLang("\n"
		          " 0: EXIT CONTROL PANEL\n"
		          " 1: Create a new house\n"
		          " 2: Update the movie of a house\n"
		          " 3: Save data\n"
		          " 4: Load data\n"
		          " 5: Check houses information\n"
		          " 6: Seat status override\n"
		          " 7: Check ticket information\n"
		          " 8: Delete a ticket\n"
		          " 9: Clear all the seats of a house\n"
		          "10: DELETE A HOUSE\n"
		          "11: CLEAR ALL DATA\n"
		          "12: STOP THE ENTIRE PROGRAM\n"
		          "13: Help\n"
		          "14: Change the colour scheme\n"
		          "15: 🌐Change the language",
		          "\n"
		          " 0: 退出控制面板\n"
		          " 1: 創建新電影院\n"
		          " 2: 更新電影名稱\n"
		          " 3: 儲存資料\n"
		          " 4: 載入資料\n"
		          " 5: 查詢電影院資訊\n"
		          " 6: 覆蓋座位狀態\n"
		          " 7: 查詢電影票資訊\n"
		          " 8: 刪除電影票\n"
		          " 9: 清空電影院的所有座位\n"
		          "10: 刪除電影院\n"
		          "11: 刪除所有資料\n"
		          "12: 停止本程式\n"
		          "13: 教學\n"
		          "14: 轉換配色\n"
		          "15: 🌐轉換語言"
		          )
		mode: str = inputLang("Please choose a mode (0/1/2/3/4/5/6/7/8/9/10/11/12/13/14)\n-> ",
		                      "請選擇模式（0/1/2/3/4/5/6/7/8/9/10/11/12/13/14）\n-> ").strip()
		
		if mode == '':
			continue
		
		if not mode.isdecimal():
			printLang("ERROR: Mode code should be all decimal",
			          "錯誤：模式代碼應該全部都是數字")
			logger.info("Invalid mode code")
			continue
		
		# EXIT CONTROL PANEL
		if mode == '0':
			printLang("Bye!", "再見！")
			logger: Logger = getLogger("adminMode.mode_0")
			logger.info("Admin Mode 0: EXIT CONTROL PANEL")
			logger.info("ADMIN LOGOUT")
			return
		
		# Create a new house
		elif mode == '1':
			createHouse()
		
		# Update the movie of a house
		elif mode == '2':
			updateMovie()
		
		# Save data
		elif mode == '3':
			logger: Logger = getLogger("adminMode.mode_3")
			logger.info("Admin Mode 3: Save data")
			saveData(print_log=True)
		
		# Load data
		elif mode == '4':
			logger: Logger = getLogger("adminMode.mode_4")
			logger.info("Admin Mode 4: Load data")
			loadData(print_log=True)
		
		# Check houses information
		elif mode == '5':
			checkHousesInformation()
		
		# Seat status override
		elif mode == '6':
			seatStatusOverride()
		
		# Check ticket information
		elif mode == '7':
			checkTicketInformation()
		
		# Delete a ticket
		elif mode == '8':
			deleteTicket()
		
		# Clear all seats of a house
		elif mode == '9':
			clearHouseSeats()
		
		# DELETE A HOUSE
		elif mode == '10':
			deleteHouse()
		
		# CLEAR ALL DATA
		elif mode == '11':
			clearAllData()
		
		# STOP THE ENTIRE PROGRAM
		elif mode == '12':
			logger: Logger = getLogger("adminMode.mode_12")
			logger.info("QUITING PROGRAM: Admin mode 12")
			printLang("Bye!", "再見！")
			quit()
		
		# Help
		elif mode == '13':
			logger: Logger = getLogger("adminMode.mode_13")
			logger.info("Admin Mode 13: Help")
			openWebBrowser("https://joeccp.github.io/SBA/")
			logger.info("Opened a website browser and visit https://joeccp.github.io/SBA/")
		
		# Change the colour scheme
		elif mode == '14':
			changeColour()
		
		# Change the language
		elif mode == '15':
			changeLanguage()
		
		else:
			logger.info("Unknown mode code")
			printLang(f"ERROR: Unknown mode code {mode}", f"錯誤：無效模式代碼——{mode}")
