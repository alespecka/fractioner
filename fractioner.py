from evaluation import evaluate


symbol = "? "


def main() -> None:
	expression = input(symbol).strip()

	while expression.lower() != "exit":
		evaluate(expression)
		expression = input(symbol).strip()


def testMain() -> None:
	expression = "(1_1/4 * 4 + 5) * 1/3"
	# expression = "(2.2 - 0.2) * 3 + 4"
	evaluate(expression)


if __name__ == "__main__":
	# main()
	testMain()
