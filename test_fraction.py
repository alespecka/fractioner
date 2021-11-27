import unittest
from random import randint

from fraction import mixedFraction2Fraction, fraction2MixedFraction, calculateGreatestCommonDivisor, Fraction


fractionExamples = [
	{"fraction": (1, 2), "mixedFraction": (1, 2, 0)},
	{"fraction": (3, 2), "mixedFraction": (1, 2, 1)},
	{"fraction": (55, 6), "mixedFraction": (1, 6, 9)},
	# {"fraction": (55, 1), "mixedFraction": (55, 1, 0)},
	# {"fraction": (9, 3), "mixedFraction": (3, 3, 2)}
]

beg, end = -100, 100
fractionPairs = [
	(
		(randint(beg, end), ),
		(randint(beg, end), )
	),
	(
		(randint(beg, end), randint(beg, end)),
		(randint(beg, end), randint(beg, end))
	),
	(
		(randint(beg, end), randint(beg, end), randint(beg, end)),
		(randint(beg, end), randint(beg, end), randint(beg, end))
	)
]


def frac2Float(numerator: int, denominator: int = 1, whole: int = 0):
	return whole + numerator / denominator


class TestFraction(unittest.TestCase):
	def testCalculateGreatestCommonDivisor(self):
		self.assertEqual(calculateGreatestCommonDivisor(15, 5), 5)
		self.assertEqual(calculateGreatestCommonDivisor(42, 49), 7)
		self.assertEqual(calculateGreatestCommonDivisor(12, 1), 1)
		self.assertEqual(calculateGreatestCommonDivisor(0, 55), 55)
		self.assertEqual(calculateGreatestCommonDivisor(36, 0), 36)

	def testMixedFraction2Fraction(self):
		for example in fractionExamples:
			self.assertEqual(mixedFraction2Fraction(*example["mixedFraction"]), example["fraction"])

	def testFraction2MixedFraction(self):
		for example in fractionExamples:
			self.assertEqual(fraction2MixedFraction(*example["fraction"]), example["mixedFraction"])

	def testFloat(self):
		n, d, w = 33, 4, 2
		self.assertAlmostEqual(float(Fraction(n, d, w)), frac2Float(n, d, w))

	def testStr(self):
		self.assertEqual(str(Fraction(87)), "87")
		self.assertEqual(str(Fraction(4, 12)), "1/3")
		self.assertEqual(str(Fraction(9, 3)), "3")
		self.assertEqual(str(Fraction(0, 77)), "0")
		self.assertEqual(str(Fraction(8, 3)), "2_2/3")
		self.assertEqual(str(Fraction(4, 5, 3)), "3_4/5")
		self.assertEqual(str(Fraction(9, 3, 3)), "6")
		self.assertEqual(str(Fraction(11, 5, 1)), "3_1/5")

	def testAdd(self):
		for frac1, frac2 in fractionPairs:
			self.assertAlmostEqual(float(Fraction(*frac1) + Fraction(*frac2)), frac2Float(*frac1) + frac2Float(*frac2))

	def testSub(self):
		for frac1, frac2 in fractionPairs:
			self.assertAlmostEqual(float(Fraction(*frac1) - Fraction(*frac2)), frac2Float(*frac1) - frac2Float(*frac2))

	def testMul(self):
		for frac1, frac2 in fractionPairs:
			self.assertAlmostEqual(float(Fraction(*frac1) * Fraction(*frac2)), frac2Float(*frac1) * frac2Float(*frac2))

	def testTruediv(self):
		for frac1, frac2 in fractionPairs:
			self.assertAlmostEqual(float(Fraction(*frac1) / Fraction(*frac2)), frac2Float(*frac1) / frac2Float(*frac2))
