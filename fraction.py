from typing import Tuple
import math


def calculateGreatestCommonDivisor(a: int, b: int) -> int:
	"""Return greatest common divisor calculated by the Euclidean algorithm."""
	while b != 0:
		a, b = b, a % b

	return a


def mixedFraction2Fraction(numerator: int, denominator: int, whole: int) -> Tuple[int, int]:
	"""Convert mixed fraction to regular fraction and return it as a tuple (<numerator>, <denominator>)."""

	if whole != 0 and (numerator < 0 or denominator < 0):
		raise ArithmeticError("numerator and denominator must be positive when part of mixed fraction")

	sign = int(math.copysign(1, whole))
	return sign * numerator + whole * denominator, denominator


def fraction2MixedFraction(numerator: int, denominator: int) -> Tuple[int, int, int, int]:
	"""Convert regular fraction to mixed fraction and return the tuple (<numerator>, <denominator>, <whole>, <sign>)."""
	sign = int(math.copysign(1, numerator * denominator))
	num = abs(numerator)
	den = abs(denominator)
	return num % den, den, num // den, sign


class Fraction:
	"""Represents a symbolic fraction with overloaded operators +, -, *, / and conversion to float and string."""

	def __init__(self, numerator: int, denominator: int = 1, whole: int = 0):
		if denominator == 0:
			raise ZeroDivisionError("division by zero")

		self.numerator, self.denominator = mixedFraction2Fraction(numerator, denominator, whole)

		self.simplify()

	def simplify(self) -> None:
		"""Simplify the fraction by dividing the numerator and denominator by the greatest common divisor."""
		divisor = calculateGreatestCommonDivisor(self.numerator, self.denominator)
		self.numerator //= divisor
		self.denominator //= divisor

	def __str__(self):
		numerator, denominator, whole, sign = fraction2MixedFraction(self.numerator, self.denominator)
		signSymbol = "-" if sign < 0 else ""

		if whole == 0:
			if denominator == 1:
				return f"{signSymbol}{numerator}"
			if numerator == 0:
				return 0
			return f"{signSymbol}{numerator}/{denominator}"
		if numerator == 0:
			return f"{signSymbol}{whole}"
		return f"{signSymbol}{whole}_{numerator}/{denominator}"

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
