import re


def evaluate(expression: str):
	infix = re.split("([ ()])", expression)  # split with respect to brackets and spaces
	infix = list(filter(lambda string: string and string != " ", infix))  # remove empty strings and spaces
	print(infix)
