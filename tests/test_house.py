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
	def test_buildHouse(self):
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
	
	def test_n_available(self):
		house: House = House(row_number=5, column_number=10)
		house.seating_plan = [
			[1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
		]
		self.assertEqual(house.n_available, 25)
