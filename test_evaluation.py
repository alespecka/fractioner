import unittest

from evaluation import parse, infix2Postfix, convertMixedFractions, evaluate, approxEvaluate, evaluatePostfix,\
	parseMixedFraction

# testData = [
# 	{"expression": "(1_1/4 * 4 + 5) * 1/3"}
# ]


class TestEvaluation(unittest.TestCase):
	def testParse(self):
		expression = "(1_1/4 * 4 + 5) * 1/3"
		lst = list(parse(expression))
		self.assertEqual(lst, ["(", "1_1/4", "*", "4", "+", "5", ")", "*", "1/3"])

		invalid = ["", "2.1 + 14", "(1_1/4 * a + 5) * 1/3"]
		for expression in invalid:
			self.assertRaises(SyntaxError, evaluate, expression)

	def testInfix2Postfix(self):
		def assertInfixPostfixMatch(infixString, postfix):
			self.assertEqual(infix2Postfix(parse(infixString)), postfix)

		assertInfixPostfixMatch("(1_1/4 * 4 + 5) * 1/3", ["1_1/4", "4", "*", "5", "+", "1/3", "*"])
		assertInfixPostfixMatch("(1 + 2) * (3 - 4)", ["1", "2", "+", "3", "4", "-", "*"])
		assertInfixPostfixMatch("(1 + 2) * 3 - (4 - 5) / -6", ["1", "2", "+", "3", "*", "4", "5", "-", "-6", "/", "-"])

	def testConvertMixedFractions(self):
		self.assertEqual(convertMixedFractions("3 * 1_1/2 - 3_4/5"), "3*(1+1/2)-(3+4/5)")

	def testEvaluatePostfix(self):
		self.assertAlmostEqual(evaluatePostfix(["1_1/4", "4", "*", "5", "+", "1/3", "*"]), 10/3)

	def testApproxEvaluate(self):
		self.assertAlmostEqual(approxEvaluate("(1_1/4 * 4 + 5) * 1/3"), 10 / 3)

	def testEvaluate(self):
		self.assertAlmostEqual(evaluate("(1_1/4 * 4 + 5) * 1/3"), 10/3)

		invalid = ["", "2.1 + 14", "(1_1/4 * a + 5) * 1/3"]
		for expression in invalid:
			self.assertRaises(SyntaxError, evaluate, expression)

		expression = "3 * 1_1/2 - 3_4/5"
		exact = evaluate(expression)
		approx = eval(convertMixedFractions(expression))
		self.assertAlmostEqual(exact, approx)

	def testParseMixedFraction(self):
		self.assertEqual(parseMixedFraction("5"), (5, 1, 0))
		self.assertEqual(parseMixedFraction("12/104"), (12, 104, 0))
		self.assertEqual(parseMixedFraction("77_302/43"), (302, 43, 77))

		invalid = ["1/2/3", "978_17", "52/9_1", "3_3_3", "/3", "_12", "_31/5", "0.2_1/2", ""]
		for term in invalid:
			self.assertRaises(SyntaxError, parseMixedFraction, term)