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
from time import sleep
from typing import Optional
from webbrowser import open as openWebBrowser

from .colour import Colour, column_colour, row_colour
from .coorutils import CoordinateExpressionException, getCoorsFromCoorExpr
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
			printLang(f"House {house.house_number}: {house.movie:<50} "
			          f"{Colour.GREEN if house.n_available > 0 else Colour.RED}"
			          f"{house.n_available}{normal_colour}/{house.n_seat}",
			          f"電影院{house.house_number}：{house.movie:<50} "
			          f"{Colour.GREEN if house.n_available > 0 else Colour.RED}"
			          f"{house.n_available}{normal_colour}/{house.n_seat}")
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
	if house.movie == '':
		if language == 'ENGLISH':
			message = "ERROR: That house is not available"
		else:
			message = "錯誤：此電影院暫不開放"
		logger.info("House not open, going back to the user menu")
		return
	logger.info(f"User selected house {house_num}")
	
	# Get number of adult tickets
	get_adult_ticket_number_message: str = ''
	while True:
		clearScreen()
		printLang("CINEMA KIOSK SYSTEM\n\n\n", "電影售票系統\n\n\n")
		print(Colour.RED + get_adult_ticket_number_message + normal_colour + "\n\n\n")
		printLang(f"House {house.house_number} is now playing: {house.movie}",
		          f"電影院{house.house_number} 正在播映：{house.movie}")
		printLang(f"Number of available seat{'s' if house.n_available > 1 else ''}: "
		          f"{house.n_available}/{house.n_seat}",
		          f"可選座位數：{house.n_available}/{house.n_seat}")
		printLang(f"Price: ${house.adult_price}", f"成人票價：${house.adult_price}")
		printLang(f"Child price: ${house.child_price}", f"兒童票價：${house.child_price}")
		
		house.printSeatingPlan()
		
		printLang("Please enter the number of adult ticket: ", "請輸入成人票的數量：")
		adult_ticket_count_str: str = input('->').strip().replace(' ', '')
		if not adult_ticket_count_str.isdecimal():
			if language == 'ENGLISH':
				get_adult_ticket_number_message: str = "ERROR: Number of tickets must be an integer"
			else:
				get_adult_ticket_number_message: str = "錯誤：數量必須爲數字"
			continue
		adult_ticket_count: int = int(adult_ticket_count_str)
		if adult_ticket_count > house.n_available:
			if language == 'ENGLISH':
				get_adult_ticket_number_message: str = "ERROR: Number of tickets exceeds number of available seat"
			else:
				get_adult_ticket_number_message: str = "錯誤：電影票數量大於可選座位數量"
			continue
		
		break
	
	# Get number of child tickets
	get_child_ticket_number_message: str = ''
	while True:
		clearScreen()
		printLang("CINEMA KIOSK SYSTEM\n\n\n", "電影售票系統\n\n\n")
		print(Colour.RED + get_child_ticket_number_message + normal_colour + "\n\n\n")
		printLang(f"House {house.house_number} is now playing: {house.movie}",
		          f"電影院{house.house_number} 正在播映：{house.movie}")
		printLang(f"Price: ${house.adult_price}", f"成人票價：${house.adult_price}")
		printLang(f"Child price: ${house.child_price}", f"兒童票價：${house.child_price}")
		house.printSeatingPlan()
		
		printLang(f"You had selected {adult_ticket_count} adult ticket{'s' if adult_ticket_count > 1 else ''}")
		printLang("Please enter the number of child ticket: ", "請輸入兒童票的數量：")
		child_ticket_count_str: str = input('->').strip().replace(' ', '')
		if not child_ticket_count_str.isdecimal():
			if language == 'ENGLISH':
				get_child_ticket_number_message: str = "ERROR: Number of tickets must be an integer"
			else:
				get_child_ticket_number_message: str = "錯誤：數量必須爲數字"
			continue
		child_ticket_count: int = int(child_ticket_count_str)
		total_ticket_number: int = adult_ticket_count + child_ticket_count
		if total_ticket_number > house.n_available:
			if language == 'ENGLISH':
				get_child_ticket_number_message: str = "ERROR: Number of tickets exceeds number of available seat"
			else:
				get_child_ticket_number_message: str = "錯誤：電影票數量大於可選座位數量"
			continue
		
		break
	
	if adult_ticket_count + child_ticket_count == 0:
		message = ''
		return
	
	# Confirm
	clearScreen()
	printLang("CINEMA KIOSK SYSTEM\n\n\n", "電影售票系統\n\n\n")
	printLang(f"House {house.house_number} is now playing: {house.movie}",
	          f"電影院{house.house_number} 正在播映：{house.movie}")
	house.printSeatingPlan()
	total_adult_price: int = house.adult_price * adult_ticket_count
	total_child_price: int = house.child_price * child_ticket_count
	total_price: int = total_adult_price + total_child_price
	printLang(f"You have selected {total_ticket_number} seat{'s' if total_ticket_number else ''}\n"
	          f"Number of adult{'s' if adult_ticket_count > 1 else ''}(${house.adult_price}): {adult_ticket_count}\n"
	          f"Number of child{'ren' if child_ticket_count > 1 else ''}(${house.child_price}): {child_ticket_count}\n"
	          f"Payment: ${total_adult_price}(adult) + ${total_child_price}(child) = ${total_price}",
	          f"你已選擇了{total_ticket_number}張電影票\n"
	          f"成人票（${house.adult_price}）：{adult_ticket_count}張\n"
	          f"兒童票（${house.child_price}）：{child_ticket_count}張\n"
	          f"應繳款項：${total_adult_price}（成人） + ${total_child_price}（兒童） = ${total_price}"
	          )
	confirm: str = inputLang("Please confirm: [Y/n]\n", "請確認：[Y/n]\n").strip().upper()
	if confirm != 'Y' and confirm != '':
		if language == 'ENGLISH':
			message = 'Confirmation failed. Purchase failed.'
		else:
			message = '確認失敗，取消購票。'
		return
	
	# Select seat
	selected_seat_list: list[tuple[int, int]] = []
	select_ticket_message: str = ''
	while True:
		clearScreen()
		printLang("CINEMA KIOSK SYSTEM\n\n\n", "電影售票系統\n\n\n")
		print(Colour.RED + select_ticket_message + normal_colour + "\n\n\n")
		printLang(f"House {house.house_number} is now playing: {house.movie}",
		          f"電影院{house.house_number} 正在播映：{house.movie}")
		house.printSeatingPlanWithSelectedSeat(selected_seat_list)
		printLang(f"You have selected {total_ticket_number} seat{'s' if total_ticket_number else ''}\n"
		          f"Number of adult{'s' if adult_ticket_count > 1 else ''}(${house.adult_price}): {adult_ticket_count}\n"
		          f"Number of child{'ren' if child_ticket_count > 1 else ''}(${house.child_price}): {child_ticket_count}\n"
		          f"Payment: ${total_adult_price}(adult) + ${total_child_price}(child) = ${total_price}",
		          f"你已選擇了{total_ticket_number}張電影票\n"
		          f"成人票（${house.adult_price}）：{adult_ticket_count}張\n"
		          f"兒童票（${house.child_price}）：{child_ticket_count}張\n"
		          f"應繳款項：${total_adult_price}（成人） + ${total_child_price}（兒童）= ${total_price}"
		          )
		selected_seat_count: int = len(selected_seat_list)
		coor_expr: str = inputLang("Please enter (part of) the coordinate, "
		                           f"You have brought {total_ticket_number} "
		                           f"seat{'s' if total_ticket_number > 1 else ''}, "
		                           f"selected {selected_seat_count} seat{'s' if len(selected_seat_list) > 1 else ''} "
		                           f"and remains {total_ticket_number-selected_seat_count} "
		                           f"seat{'s' if total_ticket_number-selected_seat_count > 1 else ''} to select "
		                           "(Or hit Enter to go back to the menu)\n->",
		                           "請輸入（部分）選擇的座位編號，"
		                           f"你購買了{total_ticket_number}個座位，你選擇了{selected_seat_count}個座位，"
		                           f"你還需要選擇{total_ticket_number-selected_seat_count}個座位"
		                           "（或按 Enter 以返回主頁面）\n->").strip().replace(' ', '')
		
		if coor_expr == '':
			message = ''
			return
		
		try:
			selected_seat_list.extend(getCoorsFromCoorExpr(coor_expr, n_row=house.n_row, n_column=house.n_column))
		except CoordinateExpressionException as error:
			if language == 'ENGLISH':
				select_ticket_message = f"ERROR: {error.__doc__}"
			else:
				select_ticket_message = f"錯誤：{error.chinese_msg}"
			continue
	
		# Remove repeated
		selected_seat_list_no_repeat: set[tuple[int, int]] = set(selected_seat_list)
		selected_seat_list: list[tuple[int, int]] = list(selected_seat_list_no_repeat)
		selected_seat_list: list[tuple[int, int]] = sorted(selected_seat_list, key=lambda tup: tup)
	
		if len(selected_seat_list) > total_ticket_number:
			if language == 'ENGLISH':
				message = "ERROR: Selected too many seats"
			else:
				message = "錯誤：選擇了過多的座位"
			return  # Return instead of continue, as buyer can't delete the selected seat
		
		# Check selected ticket
		for row_index, column_index in selected_seat_list:
			if house.seating_plan[row_index][column_index] != 0:
				if language == 'ENGLISH':
					message = f"ERROR: Seat {row_index+1}{chr(column_index+65)} is not available"
				else:
					message = f"錯誤：座位{row_index+1}{chr(column_index+65)}不供發售"
				return  # Return instead of continue, as buyer can't delete the selected seat
	
		if len(selected_seat_list) == total_ticket_number:
			break
	
	# Confirm
	clearScreen()
	printLang("CINEMA KIOSK SYSTEM\n\n\n", "電影售票系統\n\n\n")
	printLang(f"House {house.house_number} is now playing: {house.movie}",
	          f"電影院{house.house_number} 正在播映：{house.movie}")
	house.printSeatingPlanWithSelectedSeat(selected_seat_list)
	printLang(f"You have selected {total_ticket_number} seat{'s' if total_ticket_number else ''}\n"
	          f"Number of adult{'s' if adult_ticket_count > 1 else ''}(${house.adult_price}): {adult_ticket_count}\n"
	          f"Number of child{'ren' if child_ticket_count > 1 else ''}(${house.child_price}): {child_ticket_count}\n"
	          f"Payment: ${total_adult_price}(adult) + ${total_child_price}(child) = ${total_price}",
	          f"你已選擇了{total_ticket_number}張電影票\n"
	          f"成人票（${house.adult_price}）：{adult_ticket_count}張\n"
	          f"兒童票（${house.child_price}）：{child_ticket_count}張\n"
	          f"應繳款項：${total_adult_price}（成人） + ${total_child_price}（兒童） = ${total_price}"
	          )
	confirm: str = inputLang("Please confirm: [Y/n]\n", "請確認：[Y/n]\n").strip().upper()
	if confirm != 'Y' and confirm != '':
		if language == 'ENGLISH':
			message = 'Confirmation failed. Purchase failed.'
		else:
			message = '確認失敗，取消購票。'
		return
	
	# Buy
	# Child
	clearScreen()
	printLang("CINEMA KIOSK SYSTEM\n\n\n", "電影售票系統\n\n\n")
	printLang(f"House {house.house_number} is now playing: {house.movie}",
	          f"電影院{house.house_number} 正在播映：{house.movie}")
	house.printSeatingPlanWithSelectedSeat(selected_seat_list)
	printLang("Your ticket:", "你的電影票如下：")
	for row_index, column_index in selected_seat_list[:child_ticket_count]:
		house.seating_plan[row_index][column_index] = 1
		House.total_tickets += 1
		ticket_index: int = House.total_tickets
		ticket_number: str = f"T{ticket_index:0>5}"
		time: str = datetime.now().isoformat(timespec="seconds")
		price: int = house.child_price
		ticket: Ticket = (
			ticket_index, ticket_number, time, house.house_number, house.movie, row_index, column_index, price
		)
		printLang(f"{ticket_number:<6} @{time}: "
		          f"House {house.house_number:<2} -- {house.movie:<25} ~"
		          f"Seat<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}> "
		          f"${price}\n",
		          f"{ticket_number:<6} @{time}: "
		          f"電影院{house.house_number:<2} -- {house.movie:<25} ~"
		          f"座位<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}> "
		          f"${price}\n"
		          )
		House.tickets_table.append(ticket)
		house.house_revenue += price
		House.total_revenue += price
		saveData()
	# Adult
	for row_index, column_index in selected_seat_list[child_ticket_count:]:
		house.seating_plan[row_index][column_index] = 1
		House.total_tickets += 1
		ticket_index: int = House.total_tickets
		ticket_number: str = f"T{ticket_index:0>5}"
		time: str = datetime.now().isoformat(timespec="seconds")
		price: int = house.adult_price
		ticket: Ticket = (
			ticket_index, ticket_number, time, house.house_number, house.movie, row_index, column_index, price
		)
		printLang(f"{ticket_number:<6} @{time}: "
		          f"House {house.house_number:<2} -- {house.movie:<25} ~"
		          f"Seat<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}> "
		          f"${price}\n",
		          f"{ticket_number:<6} @{time}: "
		          f"電影院{house.house_number:<2} -- {house.movie:<25} ~"
		          f"座位<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}> "
		          f"${price}\n"
		          )
		House.tickets_table.append(ticket)
		house.house_revenue += price
		House.total_revenue += price
		saveData()
	
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
	ticket_index, ticket_no, time, house_no, movie, row_index, column_index, price = ticket
	printLang(f"{ticket_no:<6} @{time} "
	          f"House {house_no:<2} -- {movie:<25} ~ "
	          f"Seat<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}> "
	          f"${price}",
	          f"{ticket_no:<6} @{time} "
	          f"電影院{house_no:<2} -- {movie:<25} ~ "
	          f"座位<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}> "
	          f"${price}"
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
	ticket_index, ticket_no, time, house_no, movie, row_index, column_index, price = ticket
	logger.info(f"User want to delete this ticket: {ticket}")
	printLang(f"{ticket_no:<6} @{time} "
	          f"House {house_no:<2} -- {movie:<25} ~ "
	          f"Seat<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}> "
	          f"${price}",
	          f"{ticket_no:<6} @{time} "
	          f"電影院{house_no:<2} -- {movie:<25} ~ "
	          f"座位<{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}> "
	          f"${price}"
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
