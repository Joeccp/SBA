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
from unittest import TestCase

class Test_coorExprAnalysis(TestCase):  # NOQA: disable 'all caps in class name' warning
	def test_singleCoordinate(self):
		"""Tests single coordinate"""
		self.assertEqual(coorExprAnalysis('A1'), [(0, 0)])
		self.assertEqual(coorExprAnalysis('1A'), [(0, 0)])
		self.assertEqual(coorExprAnalysis('2B'), [(1, 1)])
		self.assertEqual(coorExprAnalysis('B2'), [(1, 1)])
		self.assertEqual(coorExprAnalysis('99Z'), [(98, 25)])
		self.assertEqual(coorExprAnalysis('Z99'), [(98, 25)])
		self.assertEqual(coorExprAnalysis('17M'), [(16, 12)])
		self.assertEqual(coorExprAnalysis('o8'), [(7, 14)])
		self.assertEqual(coorExprAnalysis('23Q', n_row=84), [(22, 16)])
		self.assertEqual(coorExprAnalysis('Q90', n_row=90), [(89, 16)])
		self.assertEqual(coorExprAnalysis('1z', n_row=1), [(0, 25)])
		self.assertEqual(coorExprAnalysis('23Q', n_column=25), [(22, 16)])
		self.assertEqual(coorExprAnalysis('23Q', n_column=17), [(22, 16)])
		self.assertEqual(coorExprAnalysis('1A', n_column=1), [(0, 0)])
		self.assertEqual(coorExprAnalysis('23Q', n_column=84), [(22, 16)])
		self.assertEqual(coorExprAnalysis('23Q', n_row=84, n_column=98), [(22, 16)])

	def test_twoCoordinates(self):
		"""Tests multiple coordinates"""
		self.assertTrue(coorExprAnalysis('A1:A2'), [(0, 0), (0, 1)])
		self.assertTrue(coorExprAnalysis('1A:2A'), [(0, 0), (0, 1)])
		self.assertTrue(coorExprAnalysis('1A:A2'), [(0, 0), (0, 1)])
		self.assertTrue(coorExprAnalysis('A1:2A'), [(0, 0), (0, 1)])
		self.assertTrue(coorExprAnalysis('1A:99Z'), [(0, 0), (98, 26)])
		self.assertTrue(coorExprAnalysis('q5:13u'), [(4, 16), (12, 20)])
		self.assertTrue(coorExprAnalysis('8C:74I'), [(7, 2), (73, 8)])
		self.assertTrue(coorExprAnalysis('1A:1B', n_row=23), [(0, 0), (0, 1)])
		self.assertTrue(coorExprAnalysis('1A:1B', n_row=1), [(0, 0), (0, 1)])
		self.assertTrue(coorExprAnalysis('7D:88Y', n_column=95), [(6, 3), (87, 24)])
		self.assertTrue(coorExprAnalysis('7D:88Y', n_column=88), [(6, 3), (87, 24)])
		self.assertTrue(coorExprAnalysis('23F:73Q', n_row=87, n_column=25), [(22, 5), (72, 16)])
		self.assertTrue(coorExprAnalysis('23F:73Q', n_row=73, n_column=17), [(22, 5), (72, 16)])
		self.assertTrue(coorExprAnalysis('23F:73Q', n_row=73, n_column=26), [(22, 5), (72, 25)])
		self.assertTrue(coorExprAnalysis('23F:73Q', n_row=86, n_column=17), [(22, 5), (72, 25)])
		self.assertTrue(coorExprAnalysis('1A:99Z', n_row=99, n_column=26), [(0, 0), (98, 25)])

	def test_stringFormatting(self):
		"""Tests how coorExprAnalysis handle white-spaces"""
		self.assertEqual(coorExprAnalysis('    1 a    '), [(0, 0)])
		self.assertEqual(coorExprAnalysis('  A  1: B2  '), [(0, 0), (1, 1)])
	
	def test_functionException(self):
		"""Tests basic about the invalid usage (argument) of the function"""
		with self.assertRaises(TypeError):
			coorExprAnalysis()  # NOQA
		with self.assertRaises(TypeError):
			coorExprAnalysis(12345)  # NOQA
		with self.assertRaises(TypeError):
			coorExprAnalysis((1, 1))  # NOQA
		with self.assertRaises(TypeError):
			coorExprAnalysis([(0, 0)])  # NOQA
		with self.assertRaises(TypeError):
			coorExprAnalysis("A1", 2, 4)  # NOQA
		with self.assertRaises(ValueError):
			coorExprAnalysis("A1", n_column=0)
		with self.assertRaises(ValueError):
			coorExprAnalysis("A1", n_row=0)
		with self.assertRaises(ValueError):
			coorExprAnalysis("A1", n_column=100)
		with self.assertRaises(ValueError):
			coorExprAnalysis("A1", n_row=100)
		with self.assertRaises(ValueError):
			coorExprAnalysis("A1", n_row=23, n_column=0)
		with self.assertRaises(ValueError):
			coorExprAnalysis("A1", n_row=12345, n_column=4)
	
	def test_singleInvalidSyntax(self):
		"""Tests exceptions about the result of the function when analyzing single coordinate"""
		with self.assertRaises(EmptyCoordinate):
			coorExprAnalysis('')
		with self.assertRaises(InvalidCharacter):
			coorExprAnalysis('(^^)')
		with self.assertRaises(InvalidCharacter):
			coorExprAnalysis('45.5Aqua')
		with self.assertRaises(InvalidCharacter):
			coorExprAnalysis('A1-B2')
		with self.assertRaises(NoStartingCoordinate):
			coorExprAnalysis(':Z99')
		with self.assertRaises(NoEndingCoordinate):
			coorExprAnalysis('G34:')
		with self.assertRaises(NoColumnCoordinate):
			coorExprAnalysis('12')
		with self.assertRaises(NoRowCoordinate):
			coorExprAnalysis('Q')
		with self.assertRaises(NoRowCoordinate):
			coorExprAnalysis("HIJKL")
		with self.assertRaises(NoColumnCoordinate):
			coorExprAnalysis('12345')
		with self.assertRaises(NoColumnCoordinate):
			coorExprAnalysis('1')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			coorExprAnalysis('12A23')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			coorExprAnalysis('111R111R111')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			coorExprAnalysis('Q55Q')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			coorExprAnalysis('JFDK324jpd345dsfk')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			coorExprAnalysis('A1B2')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			coorExprAnalysis('C11RR22')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			coorExprAnalysis('12r34R')
		with self.assertRaises(RowNumberIsZero):
			coorExprAnalysis('0A')
		with self.assertRaises(RowNumberIsZero):
			coorExprAnalysis('0Z')
		
	def test_multipleInvalidSyntax(self):
		"""Tests exceptions about the result of the function when analyzing multiple coordinates"""
		with self.assertRaises(MoreThanOneColon):
			coorExprAnalysis('7Y::6C')
		with self.assertRaises(MoreThanOneColon):
			coorExprAnalysis('42B:99K:6C')
		with self.assertRaises(NoColumnCoordinate):
			coorExprAnalysis('4:5P')
		with self.assertRaises(NoColumnCoordinate):
			coorExprAnalysis('43L:32')
		with self.assertRaises(NoRowCoordinate):
			coorExprAnalysis('35P:P')
		with self.assertRaises(NoRowCoordinate):
			coorExprAnalysis('J:8E')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			coorExprAnalysis('12G6:42P')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			coorExprAnalysis('G6:42P24')
		with self.assertRaises(RowCoordinatesAtTwoSide):
			coorExprAnalysis('12G6:42P24')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			coorExprAnalysis('T20T:T23T')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			coorExprAnalysis('T20:T23T')
		with self.assertRaises(ColumnCoordinatesAtTwoSide):
			coorExprAnalysis('T20T:T23')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			coorExprAnalysis('34QW:43Y')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			coorExprAnalysis('34Q:43YY')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			coorExprAnalysis('34QW:5jkl3Y')
		with self.assertRaises(AlphabetCharacterInRowNumber):
			coorExprAnalysis('32M:PP21')
		with self.assertRaises(RowNumberIsZero):
			coorExprAnalysis('31A:0T')
		with self.assertRaises(RowNumberIsZero):
			coorExprAnalysis('0A:0Z')
	
	def test_rangeCheck(self):
		"""Tests the range check"""
		with self.assertRaises(SameCoordinates):
			coorExprAnalysis('35P:35P')
		with self.assertRaises(SameCoordinates):
			coorExprAnalysis('P35:P35')
		with self.assertRaises(SameCoordinates):
			coorExprAnalysis('35P:P35')
		with self.assertRaises(SameCoordinates):
			coorExprAnalysis('p45:45P')
		with self.assertRaises(CoordinatesWrongOrder):
			coorExprAnalysis('78T:32D')
		with self.assertRaises(CoordinatesWrongOrder):
			coorExprAnalysis('99C:98F')
		with self.assertRaises(CoordinatesWrongOrder):
			coorExprAnalysis('32D:u18')
		with self.assertRaises(CoordinatesWrongOrder):
			coorExprAnalysis('1b:1A')
		with self.assertRaises(CoordinatesWrongOrder):
			coorExprAnalysis('w87:87h')
		with self.assertRaises(CoordinatesWrongOrder):
			coorExprAnalysis('5V:1A')
		with self.assertRaises(RowNumberOutOfRange):
			coorExprAnalysis('99Z', n_row=13)
		with self.assertRaises(RowNumberOutOfRange):
			coorExprAnalysis('36c', n_row=23, n_column=9)
		with self.assertRaises(RowNumberOutOfRange):
			coorExprAnalysis('1A:56L', n_row=35)
		with self.assertRaises(RowNumberOutOfRange):
			coorExprAnalysis('23d:34k', n_row=1, n_column=1)
		with self.assertRaises(ColumnNumberOutOfRange):
			coorExprAnalysis('1a:99Z', n_column=23)
		with self.assertRaises(ColumnNumberOutOfRange):
			coorExprAnalysis('23o', n_column=14)
		with self.assertRaises(ColumnNumberOutOfRange):
			coorExprAnalysis('78q', n_column=10, n_row=87)


class Test_getCoorsFromCoorExpr(TestCase):  # NOQA: disable 'all caps in class name' warning
	def test_singleCoordinate(self) -> None:
		self.assertEqual(getCoorsFromCoorExpr('A1'), [(0, 0)])
		self.assertEqual(getCoorsFromCoorExpr('1A'), [(0, 0)])
		self.assertEqual(getCoorsFromCoorExpr('2B'), [(1, 1)])
		self.assertEqual(getCoorsFromCoorExpr('B2'), [(1, 1)])
		self.assertEqual(getCoorsFromCoorExpr('99Z'), [(98, 25)])
		self.assertEqual(getCoorsFromCoorExpr('Z99'), [(98, 25)])
		self.assertEqual(getCoorsFromCoorExpr('17M'), [(16, 12)])
		self.assertEqual(getCoorsFromCoorExpr('o8'), [(7, 14)])
		self.assertEqual(getCoorsFromCoorExpr('23Q', n_row=84), [(22, 16)])
		self.assertEqual(getCoorsFromCoorExpr('Q90', n_row=90), [(89, 16)])
		self.assertEqual(getCoorsFromCoorExpr('1z', n_row=1), [(0, 25)])
		self.assertEqual(getCoorsFromCoorExpr('23Q', n_column=25), [(22, 16)])
		self.assertEqual(getCoorsFromCoorExpr('23Q', n_column=17), [(22, 16)])
		self.assertEqual(getCoorsFromCoorExpr('1A', n_column=1), [(0, 0)])
		self.assertEqual(getCoorsFromCoorExpr('23Q', n_column=84), [(22, 16)])
		self.assertEqual(getCoorsFromCoorExpr('23Q', n_row=84, n_column=98), [(22, 16)])
