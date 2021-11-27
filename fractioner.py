import argparse

from evaluation import evaluate, approxEvaluate
from input_error import InputError


symbol = "? "
eps = 1e-12


def main() -> None:
	parser = argparse.ArgumentParser(description="Calculator for symbolic manipulation with strings.")
	parser.add_argument("-t", "--test", action="store_true", dest="testMode", help="turn on the test mode")
	args = parser.parse_args()
	testMode = args.testMode

	ans = None
	expression = input(symbol)

	while expression.strip().lower() != "exit":
		try:
			ans = evaluate(expression)
			print(ans)
			if testMode:
				approx = approxEvaluate(expression)
				error = abs(float(ans) - approx)
				print(f"symbolic solution: {float(ans)}, numeric solution: {approx}, absolute error: {error}")
				if error < eps:
					print("TEST SUCCEEDED")
				else:
					print("TEST FAILED")

		except InputError as err:
			if err.span:
				begin = err.span[0] + len(symbol)
				length = err.span[1] - err.span[0]
				print(" " * begin + "^" * length)
			print(err)
		except ZeroDivisionError as err:
			print(err)

		expression = input(symbol)
		if ans:
			expression = expression.replace("ans", str(ans))


def testMain() -> None:
	expression = "1 - 16.0 * 3"
	# expression = "1/-2"
	# expression = "(-2 * (1 + 1_1/2) - 3/4) "
	# expression = "3 * 1_1/2 - 3_4/5"
	# expression = "(1_1/4 * 4 + 5) * 1/3"
	# expression = "(2.2 - 0.2) * 3 + 4"

	try:
		print(expression)

		ans = evaluate(expression)
		approx = approxEvaluate(expression)

		error = abs(float(ans) - approx)

		print(f"ans = {ans}")
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
