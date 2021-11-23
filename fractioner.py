from evaluation import evaluate


symbol = "? "


def main() -> None:
	expression = input(symbol).strip()

	while expression.lower() != "exit":
		evaluate(expression)
		expression = input(symbol).strip()


def testMain() -> None:
	expression = "(1/2 * 3/4) + 3"
	evaluate(expression)


if __name__ == "__main__":
	# main()
	testMain()