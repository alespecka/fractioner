import re
from typing import List, Tuple, Iterable

from fraction import Fraction


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
			topToken = tokens.pop()
			while topToken != "(":
				postfix.append(topToken)
				topToken = tokens.pop()
		else:
			postfix.append(token)

	while tokens:
		postfix.append(tokens.pop())

	return postfix


def strFraction2Float(s: str) -> float:
	s = s.replace("_", "+")
	f = eval(s)
	return f


def parseMixedFraction(term: str) -> Tuple[int, int, int]:
	message = "term has an invalid format"

	if '/' in term:
		if '_' in term:
			if not re.match("[0-9]+_[0-9]+/[0-9]+$", term):
				raise SyntaxError(message)
			whole, numerator, denominator = re.split("[_/]", term)
			return int(numerator), int(denominator), int(whole)
		else:
			if not re.match("[0-9]+/[0-9]+$", term):
				raise SyntaxError(message)
			numerator, denominator = term.split("/")
			return int(numerator), int(denominator), 0
	else:
		if not re.match("[0-9]+$", term):
			raise SyntaxError(message)
		return int(term), 1, 0


def evaluatePostfix(postfix: Iterable[str]) -> float:
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


def parse(expression: str) -> Iterable[str]:
	if not expression:
		raise SyntaxError("expression is empty")
	if not re.match("[-+*/()_0-9 ]+$", expression):
		raise SyntaxError("expression contains unsupported characters")

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
	return eval(convertMixedFractions(expression))


def evaluate(expression: str) -> float:
	infix = parse(expression)
	postfix = infix2Postfix(infix)
	return evaluatePostfix(postfix)
