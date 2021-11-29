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


def runTest(expression: str, ans: Fraction) -> None:
	"""Run test and print result to the standard output."""
	approx = evaluation.approxEvaluate(expression)
	error = abs(float(ans) - approx)
	msg = f"symbolic solution: {float(ans):.4g}, numeric solution: {approx:.4g}, absolute error: {error:.4g}"
	if error < eps:
		print("TEST SUCCEEDED. " + msg)
	else:
		print("TEST FAILED. " + msg)


def substituteAnswer(expression: str, ans: Fraction) -> str:
	if ans:
		expression = expression.replace("ans", str(ans))
	else:
		idx = expression.find("ans")
		if idx >= 0:
			raise InputError("variable 'ans' has not been set yet", span=(idx, idx + 3))

	return expression


def evalExpression(expression: str, ans: Fraction, testMode: bool) -> Fraction:
	"""Run evaluation and handle exceptions that may arise."""
	try:
		expression = substituteAnswer(expression, ans)

		ans = evaluation.evaluate(expression)
		print(answerSymbol + str(ans))

		if testMode:
			runTest(expression, ans)

	except InputError as err:
		if err.span:
			print(expression)
			print(" " * err.span[0] + "^" * (err.span[1] - err.span[0]))
		print(err)
	except ArithmeticError as err:
		print(f"arithmetic error: {err}")

	return ans


def runApp(testMode: bool) -> None:
	"""Read input from the user and depending on input run evaluation, show help or exit."""
	ans = None

	while True:
		expression = input(questionSymbol).strip()

		cmd = expression.lower()
		if not cmd:
			continue
		if cmd == "exit":
			break
		elif cmd == "help":
			print(helpString)
			continue
		else:
			ans = evalExpression(expression, ans, testMode)


def main() -> None:
	"""Parse command-line arguments and run application."""
	try:
		parser = argparse.ArgumentParser(description="Calculator for symbolic manipulation with fractions.")
		parser.add_argument("-t", "--test", action="store_true", dest="testMode", help="run app in the test mode")
		args = parser.parse_args()

		print(welcomeString)

		runApp(args.testMode)
	except KeyboardInterrupt:
		return


if __name__ == "__main__":
	main()
