from typing import Tuple
import math


def calculateGreatestCommonDivisor(a: int, b: int) -> int:
	"""Return greatest common divisor calculated by the Euclidean algorithm."""
	while a != 0:
		a, b = b % a, a

	return b


def mixedFraction2Fraction(numerator: int, denominator: int, whole: int) -> Tuple[int, int]:
	"""Convert mixed fraction to regular fraction and return it as a tuple (<numerator>, <denominator>)."""
	return numerator + whole * denominator, denominator


def fraction2MixedFraction(numerator: int, denominator: int) -> Tuple[int, int, int]:
	"""Convert regular fraction to mixed fraction and return in as a tuple (<numerator>, <denominator>, <whole>)."""
	return numerator % denominator, denominator, numerator // denominator


class Fraction:
	"""Represents a symbolic fraction with overloaded operators +, -, *, / and conversion to float and string."""

	def __init__(self, numerator: int, denominator: int = 1, whole: int = 0):
		if denominator == 0:
			raise ZeroDivisionError("division by zero")

		self.numerator, self.denominator = mixedFraction2Fraction(numerator, denominator, whole)

		self.simplify()

	def simplify(self) -> None:
		"""Simplify the fraction by dividing the numerator and denominator by the greatest common divisor."""
		divisor = calculateGreatestCommonDivisor(self.denominator, self.numerator)
		self.numerator //= divisor
		self.denominator //= divisor

	def __str__(self):
		numerator, denominator, whole = fraction2MixedFraction(self.numerator, self.denominator)
		if whole == 0:
			if denominator == 1:
				return f"{numerator}"
			if numerator == 0:
				return 0
			return f"{numerator}/{denominator}"
		if numerator == 0:
			return f"{whole}"
		return f"{whole}_{numerator}/{denominator}"

	def __add__(self, other):
		numerator = self.numerator * other.denominator + self.denominator * other.numerator
		denominator = self.denominator * other.denominator
		return Fraction(numerator, denominator)

	def __sub__(self, other):
		numerator = self.numerator * other.denominator - self.denominator * other.numerator
		denominator = self.denominator * other.denominator
		return Fraction(numerator, denominator)

	def __mul__(self, other):
		numerator = self.numerator * other.numerator
		denominator = self.denominator * other.denominator
		return Fraction(numerator, denominator)

	def __truediv__(self, other):
		numerator = self.numerator * other.denominator
		denominator = self.denominator * other.numerator
		return Fraction(numerator, denominator)

	def __float__(self):
		return self.numerator / self.denominator
