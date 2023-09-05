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

from ..src.SBA.coorutils import *
from typing import Callable
from unittest import TestCase

analysis: Callable = coorExprAnalysis


class Test_coorExprAnalysis(TestCase):  # NOQA: disable 'all caps in class name' warning
	def test_singleCoordinate(self):
		self.assertEqual(analysis('A1'), [(0, 0)])
		self.assertEqual(analysis('1A'), [(0, 0)])
		self.assertEqual(analysis('2B'), [(1, 1)])
		self.assertEqual(analysis('B2'), [(1, 1)])
		self.assertEqual(analysis('99Z'), [(98, 25)])
		self.assertEqual(analysis('Z99'), [(98, 25)])
		self.assertEqual(analysis('17M'), [(16, 12)])
		self.assertEqual(analysis('o8'), [(7, 14)])
		self.assertEqual(analysis('23Q', n_row=84), [(22, 16)])
		self.assertEqual(analysis('Q90', n_row=90), [(89, 16)])
		self.assertEqual(analysis('1z', n_row=1), [(0, 25)])
		self.assertEqual(analysis('23Q', n_column=25), [(22, 16)])
		self.assertEqual(analysis('23Q', n_column=17), [(22, 16)])
		self.assertEqual(analysis('1A', n_column=1), [(0, 0)])
		self.assertEqual(analysis('23Q', n_column=84), [(22, 16)])
		self.assertEqual(analysis('23Q', n_row=84, n_column=98), [(22, 16)])

	def test_twoCoordinates(self):
		self.assertTrue(analysis('A1:A2'), [(0, 0), (0, 1)])
		self.assertTrue(analysis('1A:2A'), [(0, 0), (0, 1)])
		self.assertTrue(analysis('1A:A2'), [(0, 0), (0, 1)])
		self.assertTrue(analysis('A1:2A'), [(0, 0), (0, 1)])
		self.assertTrue(analysis('1A:99Z'), [(0, 0), (98, 26)])
		self.assertTrue(analysis('q5:13u'), [(4, 16), (12, 20)])
		self.assertTrue(analysis('8C:74I'), [(7, 2), (73, 8)])
		self.assertTrue(analysis('1A:1B', n_row=23), [(0, 0), (0, 1)])
		self.assertTrue(analysis('1A:1B', n_row=1), [(0, 0), (0, 1)])
		self.assertTrue(analysis('7D:88Y', n_column=95), [(6, 3), (87, 24)])
		self.assertTrue(analysis('7D:88Y', n_column=88), [(6, 3), (87, 24)])
		self.assertTrue(analysis('23F:73Q', n_row=87, n_column=25), [(22, 5), (72, 16)])
		self.assertTrue(analysis('23F:73Q', n_row=73, n_column=17), [(22, 5), (72, 16)])
		self.assertTrue(analysis('23F:73Q', n_row=73, n_column=26), [(22, 5), (72, 25)])
		self.assertTrue(analysis('23F:73Q', n_row=86, n_column=17), [(22, 5), (72, 25)])
		self.assertTrue(analysis('1A:99Z', n_row=99, n_column=26), [(0, 0), (98, 25)])

	def test_stringFormatting(self):
		self.assertEqual(analysis('    1 a    '), [(0, 0)])
		self.assertEqual(analysis('  A  1: B2  '), [(0, 0), (1, 1)])
	
	def test_functionException(self):
		with self.assertRaises(TypeError):
			analysis()  # NOQA
		with self.assertRaises(TypeError):
			analysis(12345)  # NOQA
		with self.assertRaises(TypeError):
			analysis((1, 1))  # NOQA
		with self.assertRaises(TypeError):
			analysis([(0, 0)])  # NOQA
		with self.assertRaises(TypeError):
			analysis("A1", 2, 4)  # NOQA
		with self.assertRaises(ValueError):
			analysis("A1", n_column=0)
		with self.assertRaises(ValueError):
			analysis("A1", n_row=0)
		with self.assertRaises(ValueError):
			analysis("A1", n_column=100)
		with self.assertRaises(ValueError):
			analysis("A1", n_row=100)
		with self.assertRaises(ValueError):
			analysis("A1", n_row=23, n_column=0)
		with self.assertRaises(ValueError):
			analysis("A1", n_row=12345, n_column=4)
	
	def test_singleInvalidSyntax(self):
		with self.assertRaises(EmptyCoordinate):
			analysis('')
		with self.assertRaises(InvalidCharacter):
			analysis('(^^)')
		with self.assertRaises(InvalidCharacter):
			analysis('45.5Aqua')
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
			analysis('12345')
		with self.assertRaises(NoColumnCoordinate):
			analysis('1')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			analysis('12A23')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			analysis('111R111R111')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			analysis('Q55Q')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			analysis('JFDK324jpd345dsfk')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			analysis('A1B2')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			analysis('C11RR22')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			analysis('12r34R')
		with self.assertRaises(RowNumberIsZero):
			analysis('0A')
		with self.assertRaises(RowNumberIsZero):
			analysis('0Z')
		
	def test_multipleInvalidSyntax(self):
		with self.assertRaises(MoreThanOneColon):
			analysis('7Y::6C')
		with self.assertRaises(MoreThanOneColon):
			analysis('42B:99K:6C')
		with self.assertRaises(NoColumnCoordinate):
			analysis('4:5P')
		with self.assertRaises(NoColumnCoordinate):
			analysis('43L:32')
		with self.assertRaises(NoRowCoordinate):
			analysis('35P:P')
		with self.assertRaises(NoRowCoordinate):
			analysis('J:8E')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			analysis('12G6:42P')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			analysis('G6:42P24')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			analysis('12G6:42P24')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			analysis('T20T:T23T')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			analysis('T20:T23T')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			analysis('T20T:T23')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			analysis('34QW:43Y')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			analysis('34Q:43YY')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			analysis('34QW:5jkl3Y')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			analysis('32M:PP21')
		with self.assertRaises(RowNumberIsZero):
			analysis('31A:0T')
		with self.assertRaises(RowNumberIsZero):
			analysis('0A:0Z')
	
	def test_rangeCheck(self):
		with self.assertRaises(SameCoordinates):
			analysis('35P:35P')
		with self.assertRaises(SameCoordinates):
			analysis('P35:P35')
		with self.assertRaises(SameCoordinates):
			analysis('35P:P35')
		with self.assertRaises(SameCoordinates):
			analysis('p45:45P')
		with self.assertRaises(CoordinatesWrongOrder):
			analysis('78T:32D')
		with self.assertRaises(CoordinatesWrongOrder):
			analysis('99C:98F')
		with self.assertRaises(CoordinatesWrongOrder):
			analysis('32D:u18')
		with self.assertRaises(CoordinatesWrongOrder):
			analysis('1b:1A')
		with self.assertRaises(CoordinatesWrongOrder):
			analysis('w87:87h')
		with self.assertRaises(CoordinatesWrongOrder):
			analysis('5V:1A')
		with self.assertRaises(RowNumberOutOfRange):
			analysis('99Z', n_row=13)
		with self.assertRaises(RowNumberOutOfRange):
			analysis('36c', n_row=23, n_column=9)
		with self.assertRaises(RowNumberOutOfRange):
			analysis('1A:56L', n_row=35)
		with self.assertRaises(RowNumberOutOfRange):
			analysis('23d:34k', n_row=1, n_column=1)
		with self.assertRaises(ColumnNumberOutOfRange):
			analysis('1a:99Z', n_column=23)
		with self.assertRaises(ColumnNumberOutOfRange):
			analysis('23o', n_column=14)
		with self.assertRaises(ColumnNumberOutOfRange):
			analysis('78q', n_column=10, n_row=87)
