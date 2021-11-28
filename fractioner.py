"""Command-line program that symbolically evaluates expressions with fractions."""

import argparse

import evaluation
from input_error import InputError
from fraction import Fraction


welcomeString = """Welcome to Fractioner!

For help type 'help'.
To exit type 'exit'.
"""

helpString = """----------------------------------------------------------------------------------------
Help for Fractioner 

For help type 'help'.
To exit type 'exit'.

Fractioner is a symbolic fraction calculator.

Valid expression may contain operators parentheses and operands. The expression must
follow these rules:

* Four operators are supported +, -, *, /.
* Operands may be whole numbers, fractions or mixed fractions.
* Mixed fractions are represented by <whole>_<numerator>/<denominator>, e.g. "1_2/3".
* Operators and operand must be separated by one or more spaces.
* Any number of pairs of parentheses may be included.
* Parentheses do not need to be separated by spaces from operators or operands.
* There is a single variable 'ans', which contains the result of the last expression.

EXAMPLES
--------
Here is an example run:

? 1/2 + 1/3 - 2
= -1_1/6
? (2_3/4 - 1_1/5) * 5
= 7_3/4
? ((1 - 3) - (5/3 + 1/3)) * (2_3/8 + 9/8) / 1/2
= -28
? ans / -7
= 4

As you can see above, we may use 'ans' variable, which stores the result of the previous
expression.
----------------------------------------------------------------------------------------
"""

questionSymbol = "? "
answerSymbol = "= "
eps = 1e-12


def evalExpression(expression: str, testMode: bool = False) -> Fraction:
	ans = evaluation.evaluate(expression)
	print(answerSymbol + str(ans))

	if testMode:
		approx = evaluation.approxEvaluate(expression)
		error = abs(float(ans) - approx)
		print(f"symbolic solution: {float(ans)}, numeric solution: {approx}, absolute error: {error}")
		if error < eps:
			print("TEST SUCCEEDED")
		else:
			print("TEST FAILED")

	return ans


def main() -> None:
	parser = argparse.ArgumentParser(description="Calculator for symbolic manipulation with fractions.")
	parser.add_argument("-t", "--test", action="store_true", dest="testMode", help="run app in the test mode")
	args = parser.parse_args()
	testMode = args.testMode

	print(welcomeString)

	ans = None

	while True:
		expression = input(questionSymbol)

		cmd = expression.strip().lower()
		if not cmd:
			continue
		if cmd == "exit":
			break
		elif cmd == "help":
			print(helpString)
			continue
		else:
			try:
				if ans:
					expression = expression.replace("ans", str(ans))
				else:
					idx = expression.find("ans")
					if idx >= 0:
						raise InputError("variable 'ans' has not been set yet", span=(idx, idx+3))

				ans = evalExpression(expression, testMode)
			except InputError as err:
				if err.span:
					print(expression)
					print(" " * err.span[0] + "^" * (err.span[1] - err.span[0]))
				print(err)
			except ZeroDivisionError as err:
				print(err)


def testMain() -> None:
	# expression = "1 - 16.0 * 3"
	# expression = "-1/3"
	# expression = "-1/3"
	expression = "-1_1/2"
	# expression = "-2"
	# expression = "(-2 * (1 + 1_1/2) - 3/4) "
	# expression = "3 * 1_1/2 - 3_4/5"
	# expression = "(1_1/4 * 4 + 5) * 1/3"
	# expression = "(2.2 - 0.2) * 3 + 4"

	try:
		print(expression)

		ans = evaluation.evaluate(expression)
		approx = evaluation.approxEvaluate(expression)

		error = abs(float(ans) - approx)

		print(f"ans = {ans}")
		print(f"ans = {float(ans)}")
		print(f"test = {approx}")
		print(f"absolute error = {error}")
	except InputError as err:
		if err.span:
			print(" " * err.span[0] + "^" * (err.span[1] - err.span[0]))
		print(err)
	except ZeroDivisionError as err:
		print(err)


if __name__ == "__main__":
	main()
	# testMain()
