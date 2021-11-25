import unittest

from evaluation import parse, infix2Postfix, convertMixedFractions, evaluate, approxEvaluate, evaluatePostfix


class TestEvaluation(unittest.TestCase):
	def testParse(self):
		expression = "(1_1/4 * 4 + 5) * 1/3"
		lst = list(parse(expression))
		self.assertEqual(lst, ["(", "1_1/4", "*", "4", "+", "5", ")", "*", "1/3"])

	def testInfix2Postfix(self):
		def assertInfixPostfixMatch(infixString, postfix):
			self.assertEqual(infix2Postfix(parse(infixString)), postfix)

		assertInfixPostfixMatch("(1_1/4 * 4 + 5) * 1/3", ["1_1/4", "4", "*", "5", "+", "1/3", "*"])
		assertInfixPostfixMatch("(A + B) * (C - D)", ["A", "B", "+", "C", "D", "-", "*"])
		assertInfixPostfixMatch("(A + B) * C - (D - E) / F", ["A", "B", "+", "C", "*", "D", "E", "-", "F", "/", "-"])

	def testConvertMixedFractions(self):
		self.assertEqual(convertMixedFractions("3 * 1_1/2 - 3_4/5"), "3*(1+1/2)-(3+4/5)")

	def testEvaluatePostfix(self):
		self.assertAlmostEqual(evaluatePostfix(["1_1/4", "4", "*", "5", "+", "1/3", "*"]), 10/3)

	def testApproxEvaluate(self):
		self.assertAlmostEqual(approxEvaluate("(1_1/4 * 4 + 5) * 1/3"), 10 / 3)

	def testEvaluate(self):
		self.assertAlmostEqual(evaluate("(1_1/4 * 4 + 5) * 1/3"), 10/3)

		expression = "3 * 1_1/2 - 3_4/5"
		exact = evaluate(expression)
		approx = eval(convertMixedFractions(expression))
		self.assertAlmostEqual(exact, approx)

# def evaluatePostfixTest(self):
