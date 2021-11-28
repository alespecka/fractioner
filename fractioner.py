import argparse

import evaluation
from input_error import InputError
from fraction import Fraction


symbol = "? "
eps = 1e-12

"""Command-line program that symbolically evaluates expressions with fractions."""


helpString = "this is help string"


def evalExpression(expression: str, testMode: bool = False) -> Fraction:
	ans = evaluation.evaluate(expression)
	print(ans)

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
	parser = argparse.ArgumentParser(description="Calculator for symbolic manipulation with strings.")
	parser.add_argument("-t", "--test", action="store_true", dest="testMode", help="turn on the test mode")
	args = parser.parse_args()
	testMode = args.testMode

	ans = None

	while True:
		expression = input(symbol)

		cmd = expression.strip().lower()
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
					begin = err.span[0]
					length = err.span[1] - err.span[0]
					print(" " * begin + "^" * length)
				print(err)
			except ZeroDivisionError as err:
				print(err)


def testMain() -> None:
	# expression = "1 - 16.0 * 3"
	# expression = "-1/3"
	expression = "-1/3"
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
