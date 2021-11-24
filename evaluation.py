import re
from typing import List, Iterable


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
			stack.append(strFraction2Float(token))

	# print(len(stack))
	return stack.pop()


def parse(expression: str) -> Iterable[str]:
	tokens = re.split("([ ()])", expression)  # split with respect to parentheses and spaces
	tokens = filter(lambda string: string and string != " ", tokens)  # remove empty strings and spaces
	return tokens


def evaluate(expression: str) -> None:
	infix = parse(expression)
	infix = list(infix)
	postfix = infix2Postfix(infix)

	print(expression)
	print(infix)
	print(postfix)

	ans = evaluatePostfix(postfix)
	approx = eval(expression)
	err = abs(ans - approx)

	print(f"ans = {ans}")
	print(f"test = {approx}")
	print(f"absolute error = {err}")
