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
				raise InputError("mismatched parenthesis")
			topToken = tokens.pop()
			while topToken != "(":
				postfix.append(topToken)
				if not tokens:
					raise InputError("mismatched parenthesis")
				topToken = tokens.pop()

		else:
			postfix.append(token)

	while tokens:
		token = tokens.pop()
		if token == "(":
			raise InputError("mismatched parenthesis")
		postfix.append(token)

	return postfix


# def strFraction2Float(s: str) -> float:
# 	s = s.replace("_", "+")
# 	f = eval(s)
# 	return f


def parseMixedFraction(term: str) -> Tuple[int, int, int]:
	"""
	Parse fraction and return in as a tuple (<numerator>, <denominator>, <whole>).

	Term is expected to be in one of the following forms ''.
	:param term
		String in either the mixed fraction (e.g. '1_2/3'), regular fraction (e.g. '1/2') or integer (e.g. '1') form.

	:return tuple (<numerator>, <denominator>, <whole>)
	"""
	message = f"term '{term}' has invalid format"

	if '/' in term:
		if '_' in term:
			# test if term is in mixed fraction format e.g. 1_2/3
			if not re.match("[+-]*[0-9]+_[0-9]+/[0-9]+$", term):
				raise InputError(message)

			whole, numerator, denominator = re.split("[_/]", term)
			return int(numerator), int(denominator), int(whole)

		else:
			# test if term is in regular fraction format e.g. 1/2
			if not re.match("[+-]*[0-9]+/[0-9]+$", term):
				raise InputError(message)

			numerator, denominator = term.split("/")
			return int(numerator), int(denominator), 0

	else:
		# test if term is in integer format e.g. 1
		if not re.match("[+-]*[0-9]+$", term):
			raise InputError(message)

		return int(term), 1, 0


def evaluatePostfix(postfix: Iterable[str]) -> Fraction:
	"""Evaluate postfix expression"""
	stack = []

	for token in postfix:
		if token in operators:
			b = stack.pop()
			a = stack.pop()
			operation = operations[token]
			c = operation(a, b)
			stack.append(c)
		else:
			fraction = Fraction(*parseMixedFraction(token))
			# strFraction2Float(token)
			stack.append(fraction)

	# print(len(stack))
	return stack.pop()


validCharacters = "-+*/()_0123456789 "


def parse(expression: str) -> Iterable[str]:
	"""
	Parse input expression and return the tokens, e.i. terms, operators and parentheses, as iterable.

	Every pair of tokens except for parentheses (i.e. terms or operators) must be separated by spaces.
	"""
	if not expression:
		raise InputError("expression is empty")

	obj = re.search("[^-+*/()_0-9 ]", expression)
	if obj:
		span = obj.span()
		raise InputError(f"invalid character '{expression[span[0] : span[1]]}'", span)
	# for i, char in enumerate(expression):
	# 	if char not in validCharacters:
	# 		raise InputError(f"invalid character '{char}'", i)

	tokens = re.split("([ ()])", expression)  # split with respect to parentheses and spaces
	tokens = filter(lambda string: string and string != " ", tokens)  # remove empty strings and spaces
	return tokens


def convertMixedFractions(expression: str) -> str:
	"""Add parentheses around mixed fraction and convert '_' to '+', e.g. '3 * 1_1/2' becomes '3*(1+1/2)'."""
	tokens = parse(expression)
	newTokens = []
	for string in tokens:
		if '_' in string:
			newTokens.append('(')
			newTokens.append(string.replace('_', '+'))
			newTokens.append(')')
		else:
			newTokens.append(string)

	return "".join(newTokens)


def approxEvaluate(expression: str) -> float:
	"""
	Evaluate expression with fractions numerically.

	:param expression
		Every pair of tokens except for parentheses (i.e. terms or operators) must be separated by spaces.

	:raises InputError if the expression has invalid format.

	:returns Result of evaluation.
	"""
	return eval(convertMixedFractions(expression))


def evaluate(expression: str) -> Fraction:
	"""
	Evaluate expression with fractions symbolically.

	:param expression
		Every pair of tokens except for parentheses (i.e. terms or operators) must be separated by spaces.

	:raises InputError if the expression has invalid format.

	:returns Result of evaluation
	"""

	infix = parse(expression)
	postfix = infix2Postfix(infix)
	return evaluatePostfix(postfix)
