from evaluation import evaluate, approxEvaluate


symbol = "? "


def main() -> None:
	expression = input(symbol).strip()

	while expression.lower() != "exit":
		ans = evaluate(expression)
		print(ans)
		expression = input(symbol).strip()


def testMain() -> None:
	expression = "3 * 1_1/2 - 3_4/5"
	# expression = "(1_1/4 * 4 + 5) * 1/3"
	# expression = "(2.2 - 0.2) * 3 + 4"
	ans = evaluate(expression)
	approx = approxEvaluate(expression)

	err = abs(ans - approx)

	print(f"ans = {ans}")
	print(f"test = {approx}")
	print(f"absolute error = {err}")


if __name__ == "__main__":
	main()
	# testMain()
