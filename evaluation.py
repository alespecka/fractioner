import re
from typing import List, Tuple, Iterable

from fraction import Fraction
from input_error import InputError


operators = "+-*/"
operations = {
	"+": lambda x, y: x + y,
	"-": lambda x, y: x - y,
	"*": lambda x, y: x * y,
	"/": lambda x, y: x / y
}
precedence = {"*": 3, "/": 3, "+": 2, "-": 2, "(": 1}


def infix2Postfix(infix: Iterable[str]) -> List[str]:
	"""Convert infix expression to postfix expression (reversed Polish notation)"""
	tokens = []
	postfix = []

	for token in infix:
		if token in operators:
			while tokens and precedence[tokens[-1]] >= precedence[token]:
				postfix.append(tokens.pop())
			tokens.append(token)

		elif token == "(":
			tokens.append(token)

		elif token == ")":
			if not tokens:
				raise InputError("mismatched parentheses")
			topToken = tokens.pop()
			while topToken != "(":
				postfix.append(topToken)
				if not tokens:
					raise InputError("mismatched parentheses")
				topToken = tokens.pop()

		else:
			postfix.append(token)

	while tokens:
		token = tokens.pop()
		if token == "(":
			raise InputError("mismatched parentheses")
		postfix.append(token)

	return postfix


def parseMixedFraction(operand: str) -> Tuple[int, int, int]:
	"""
	Parse operand, which can be a whole number, a fraction or a mixed fraction.

	:param operand
		String in either the mixed fraction (e.g. '1_2/3'), regular fraction (e.g. '1/2') or integer (e.g. '1') form.

	:return tuple (<numerator>, <denominator>, <whole>)
	"""
	message = f"operand '{operand}' is invalid"

	if '/' in operand:
		if '_' in operand:
			# test if operand is in mixed fraction format e.g. 1_2/3
			if not re.match("[+-]?[0-9]+_[0-9]+/[0-9]+$", operand):
				raise InputError(message)

			whole, numerator, denominator = re.split("[_/]", operand)
			return int(numerator), int(denominator), int(whole)

		else:
			# test if operand is in regular fraction format e.g. 1/2
			if not re.match("[+-]?[0-9]+/[0-9]+$", operand):
				raise InputError(message)

			numerator, denominator = operand.split("/")
			return int(numerator), int(denominator), 0

	else:
		# test if operand is in integer format e.g. 1
		if not re.match("[+-]?[0-9]+$", operand):
			raise InputError(message)

		return int(operand), 1, 0


def evaluatePostfix(postfix: Iterable[str]) -> Fraction:
	"""Evaluate postfix expression"""
	stack = []

	for token in postfix:
		if token in operators:
			if len(stack) < 2:
				raise InputError(f"operator '{token}' is missing one or both operands")
			b = stack.pop()
			a = stack.pop()
			operation = operations[token]
			c = operation(a, b)
			stack.append(c)
		else:
			fraction = Fraction(*parseMixedFraction(token))
			# strFraction2Float(token)
			stack.append(fraction)

	if not stack:
		raise InputError()
	if len(stack) > 1:
		operands = "', '".join(map(lambda fract: str(fract), stack))
		raise InputError(f"operands '{operands}' do not have operator to act on them")

	return stack.pop()


def parse(expression: str) -> Iterable[str]:
	"""
	Parse input expression and return the tokens, e.i. operands, operators and parentheses, as iterable.

	Every pair of tokens except for parentheses (i.e. operands or operators) must be separated by spaces.
	"""
	searchObj = re.search("[^-+*/()_0-9 ]", expression)
	if searchObj:
		span = searchObj.span()
		raise InputError(f"invalid character '{expression[span[0] : span[1]]}'", span)

	tokens = re.split("([ ()])", expression)  # split with respect to parentheses and spaces
	tokens = filter(lambda string: string and string != " ", tokens)  # remove empty strings and spaces
	return tokens


def convertMixedFractions(expression: str) -> str:
	"""Add parentheses around mixed fraction and convert '_' to '+', e.g. '3 * 1_1/2' becomes '3*(1+1/2)'."""
	tokens = parse(expression)
	newTokens = []
	for string in tokens:
		if '_' in string:
			sign = "-" if string and string.strip()[0] == "-" else "+"
			newTokens.append('(')
			newTokens.append(string.replace('_', sign))
			newTokens.append(')')
		else:
			newTokens.append(string)

	return "".join(newTokens)


def approxEvaluate(expression: str) -> float:
	"""
	Evaluate expression with fractions numerically.

	:param expression
		Every pair of tokens except for parentheses (i.e. operands or operators) must be separated by spaces.

	:raises InputError if the expression has invalid format.

	:returns Result of evaluation.
	"""
	return eval(convertMixedFractions(expression))


def evaluate(expression: str) -> Fraction:
	"""
	Evaluate expression with fractions symbolically.

	:param expression
		Every pair of tokens except for parentheses (i.e. operands or operators) must be separated by spaces.

	:raises InputError if the expression has invalid format.

	:returns Result of evaluation
	"""

	infix = parse(expression)
	postfix = infix2Postfix(infix)
	return evaluatePostfix(postfix)
