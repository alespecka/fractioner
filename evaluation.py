import re
from typing import List


operators = "+-*/"
precedence = {"*": 3, "/": 3, "+": 2, "-": 2, "(": 1}


def infix2postfix(infix: List[str]) -> List[str]:
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


def evaluate(expression: str):
	infix = re.split("([ ()])", expression)  # split with respect to brackets and spaces
	infix = list(filter(lambda string: string and string != " ", infix))  # remove empty strings and spaces
	postfix = infix2postfix(infix)

	print(expression)
	print(infix)
	print(postfix)
