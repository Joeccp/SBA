"""Unit tests for coorutils"""

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

from src.coorutils import *
from typing import Callable
from unittest import TestCase

analysis: Callable = coorExprAnalysis


class Test_coorExprAnalysis(TestCase):
	def test_singleCoordinate(self):
		self.assertEqual(analysis('A1'), [(0, 0)])
		self.assertEqual(analysis('1A'), [(0, 0)])
		self.assertEqual(analysis('2B'), [(1, 1)])
		self.assertEqual(analysis('B2'), [(1, 1)])
		self.assertEqual(analysis('99Z'),[(98, 25)])
		self.assertEqual(analysis('Z99'),[(98, 25)])
		self.assertEqual(analysis('17M'), [(16, 12)])
		self.assertEqual(analysis('o8'), [(7, 14)])

	
	def test_twoCoordinates(self):
		self.assertTrue(analysis('A1:A2'), [(0, 0), (0, 1)])
		self.assertTrue(analysis('1A:2A'), [(0, 0), (0, 1)])
		self.assertTrue(analysis('1A:A2'), [(0, 0), (0, 1)])
		self.assertTrue(analysis('A1:2A'), [(0, 0), (0, 1)])
		self.assertTrue(analysis('1A:99Z'), [(0, 0), (98, 26)])
		self.assertTrue(analysis('q5:13u'), [(4, 16), (12, 20)])
		self.assertTrue(analysis('8C:74I'), [(7, 2), (73, 8)])
		

	def test_stringForamtting(self):
		self.assertEqual(analysis('    1 a    '), [(0, 0)])
		self.assertEqual(analysis('  A  1: B2  '), [(0, 0), (1, 1)])
	
	
	def test_functionException(self):
		with self.assertRaises(TypeError):
			analysis()
		with self.assertRaises(TypeError):
			analysis(12345)
		with self.assertRaises(TypeError):
			analysis((1, 1))
		with self.assertRaises(TypeError):
			analysis([(0, 0)])
		with self.assertRaises(TypeError):
			analysis("A1", 2, 4)
		with self.assertRaises(ValueError):
			analysis("A1", n_column=0)
		with self.assertRaises(ValueError):
			analysis("A1", n_row=0)
		with self.assertRaises(ValueError):
			analysis("A1", n_column=100)
		with self.assertRaises(ValueError):
			analysis("A1", n_row=100)
		with self.assertRaises(ValueError):
			analysis("A1",n_row=23, n_column=0)
		with self.assertRaises(ValueError):
			analysis("A1", n_row=12345, n_column=4)
	
	def test_invalidSyntax(self):
		with self.assertRaises(EmptyCoordinate):
			analysis('')
		with self.assertRaises(InvalidCharacter):
			analysis('(^^)')
		with self.assertRaises(InvalidCharacter):
			analysis('A1-B2')
		with self.assertRaises(NoStartingCoordinate):
			analysis(':Z99')
		with self.assertRaises(NoEndingCoordinate):
			analysis('G34:')
		with self.assertRaises(NoColumnCoordinate):
			analysis('12')
		with self.assertRaises(NoRowCoordinate):
			analysis('Q')
		with self.assertRaises(NoRowCoordinate):
			analysis("HIJKL")
		with self.assertRaises(NoColumnCoordinate):
			analysis('012345')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			analysis('12A23')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			analysis('111R111R111')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			analysis('Q55Q')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			analysis('JFDK324jpd345dsfk')