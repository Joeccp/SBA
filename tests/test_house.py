"""Unit tests for the House class"""

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

from unittest import TestCase

from ..src.SBA.house import House


class Test_House(TestCase):  # NOQA: disable 'all caps in class name' warning
	
	@classmethod
	def setUpClass(cls) -> None:
		"""Before testing, reset all house data"""
		House.houses_table = {}
		House.n_House = 0
		House.tickets_table = []
		House.total_tickets = 0
	
	@classmethod
	def tearDownClass(cls) -> None:
		"""After testing, reset all house data"""
		House.houses_table = {}
		House.n_House = 0
		House.tickets_table = []
		House.total_tickets = 0
	
	def setUp(self) -> None:
		"""Clear houses table before each test so house number will be 1 every time"""
		House.houses_table = {}
	
	def test_initHouse(self):
		"""Tests the basic attributes of a House instance"""
		house: House = House(row_number=5, column_number=10)
		self.assertEqual(house.n_row, 5)
		self.assertEqual(house.n_column, 10)
		self.assertEqual(house.seating_plan, [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		])
		self.assertEqual(house.n_seat, 50)
		self.assertEqual(house.n_available, 50)
		self.assertEqual(house.house_number, 1)
		self.assertEqual(house.house_revenue, 0)
		self.assertEqual(house.adult_price, 0)
		self.assertEqual(house.child_price, 0)
	
	def test_seatingPlanOperation(self):
		"""Tests operations toward seating_plan"""
		house: House = House(row_number=5, column_number=10)
		house.seating_plan = [
			[1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
		]
		self.assertEqual(house.n_available, 25)
		
		self.assertEqual(
			house[0],
			[1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
		)
		
		house.clearPlan()
		self.assertEqual(house.seating_plan, [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		])
		self.assertEqual(house.n_available, 50)
		
		with self.assertRaises(Exception):  # MethodShouldNotBeUsed exception
			house[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	
	def test_ticket(self):
		"""Tests separation about tickets"""
		house: House = House(row_number=99, column_number=26)
		house.movie = "An Excellent Movie"
		House.tickets_table = [
			[1, "T00001", '0186-05-05T00:00:00', 1, "An Excellent Movie", 0, 0, 0],
			[2, "T00002", '2006-02-27T00:00:00', 1, "An Excellent Movie", 0, 1, 0],
			[3, "T00003", '2006-05-22T05:02:00', 1, "An Excellent Movie", 0, 2, 0],
			[4, "T00004", '2018-08-01T03:05:00', 1, "An Excellent Movie", 0, 3, 0],
			[5, "T00005", '2018-09-04T04:08:06', 1, "An Excellent Movie", 0, 4, 0],
			[6, "T00006", '2020-08-13T00:06:09', 1, "An Excellent Movie", 0, 5, 0],
			[7, "T00007", '2020-09-13T01:02:05', 1, "An Excellent Movie", 0, 6, 0],
			[8, "T00008", '2021-11-26T01:03:09', 1, "An Excellent Movie", 0, 7, 0],
			[9, "T00009", '2023-07-26T01:04:00', 1, "An Excellent Movie", 0, 8, 0],
			[10, "T00010", '2023-07-26T22:22:22', 1, "An Excellent Movie", 0, 9, 0],
			[11, "T00011", '2023-09-09T01:05:03', 1, "An Excellent Movie", 0, 10, 0],
			[12, "T00012", '2023-09-09T01:06:02', 1, "An Excellent Movie", 0, 11, 0],
		]
		House.total_tickets = 12
		
		self.assertEqual(House.get_n_tickets(), 12)
		self.assertEqual(
			House.searchTicket(2),
			[2, "T00002", '2006-02-27T00:00:00', 1, "An Excellent Movie", 0, 1, 0]
		)
		self.assertEqual(House.searchTicket(0), None)
		self.assertEqual(House.searchTicket(13), None)
		
		House.tickets_table.remove([2, "T00002", '2006-02-27T00:00:00', 1, "An Excellent Movie", 0, 1, 0])
		self.assertEqual(House.total_tickets, 12)  # Total tickets should not change
		self.assertEqual(House.get_n_tickets(), 11)
		self.assertEqual(
			House.searchTicket(2),
			None
		)
		self.assertEqual(
			House.searchTicket(3),
			[3, "T00003", '2006-05-22T05:02:00', 1, "An Excellent Movie", 0, 2, 0]
		)
