import unittest

from input_error import InputError
from evaluation import parse, infix2Postfix, convertMixedFractions, evaluate, approxEvaluate, evaluatePostfix,\
	parseMixedFraction

testData = [
	{
		"expression": "(1_1/4 * 4 + 5) * 1/3",
		"ans": "3_1/3",
		"val": 10/3,
		"infix": ["(", "1_1/4", "*", "4", "+", "5", ")", "*", "1/3"],
		"postfix": ["1_1/4", "4", "*", "5", "+", "1/3", "*"]
	},
	{
		"expression": "(1 + 2) * (3 - 4)",
		"ans": "-3",
		"val": -3,
		"infix": ["(", "1", "+", "2", ")", "*", "(", "3", "-", "4", ")"],
		"postfix":  ["1", "2", "+", "3", "4", "-", "*"]
	},
	{
		"expression": "(1 + 2) * 3 - (4 - 5) / -6",
		"ans": "8_5/6",
		"val": 8 + 5/6,
		"infix": ["(", "1", "+", "2", ")", "*", "3", "-", "(", "4", "-", "5", ")", "/", "-6"],
		"postfix":  ["1", "2", "+", "3", "*", "4", "5", "-", "-6", "/", "-"]
	},
]


class TestEvaluation(unittest.TestCase):
	def testParse(self):
		expression = "(1_1/4 * 4 + 5) * 1/3"
		lst = list(parse(expression))
		self.assertEqual(lst, ["(", "1_1/4", "*", "4", "+", "5", ")", "*", "1/3"])

		invalid = ["", "2.1 + 14", "(1_1/4 * a + 5) * 1/3"]
		for expression in invalid:
			self.assertRaises(InputError, evaluate, expression)

	def testInfix2Postfix(self):
		for item in testData:
			postfix = item.get("postfix")
			infix = item.get("infix")
			if postfix and infix:
				self.assertEqual(infix2Postfix(infix), postfix)

	def testConvertMixedFractions(self):
		self.assertEqual(convertMixedFractions("3 * 1_1/2 - 3_4/5"), "3*(1+1/2)-(3+4/5)")

	def testEvaluatePostfix(self):
		for item in testData:
			postfix = item.get("postfix")
			if postfix:
				self.assertAlmostEqual(float(evaluatePostfix(postfix)), item["val"])

	def testApproxEvaluate(self):
		for item in testData:
			self.assertAlmostEqual(float(approxEvaluate(item["expression"])), item["val"])

	def testEvaluate(self):
		for item in testData:
			self.assertEqual(str(evaluate(item["expression"])), item["ans"])

		expressions = ["-1/3", "-1_1/2 * 10", "3 * 1_1/2 - 3_4/5", "3 * 1_1/2 - 3_4/5", "(-2 * (1 + 1_1/2) - 3/4)"]
		for expression in expressions:
			exact = float(evaluate(expression))
			approx = approxEvaluate(expression)
			self.assertAlmostEqual(exact, approx)

		invalidExpressions = ["", "2.1 + 14", "(1_1/4 * a + 5) * 1/3"]
		for expression in invalidExpressions:
			self.assertRaises(InputError, evaluate, expression)

		self.assertRaises(ArithmeticError, evaluate, "-2/0")
		self.assertRaises(ArithmeticError, evaluate, "3 / (1 - 1)")

	def testParseMixedFraction(self):
		self.assertEqual(parseMixedFraction("5"), (5, 1, 0))
		self.assertEqual(parseMixedFraction("12/104"), (12, 104, 0))
		self.assertEqual(parseMixedFraction("77_302/43"), (302, 43, 77))

		invalidOperands = ["1/2/3", "978_17", "52/9_1", "3_3_3", "/3", "_12", "_31/5", "0.2_1/2", ""]
		for operand in invalidOperands:
			self.assertRaises(InputError, parseMixedFraction, operand)
