from typing import Tuple


class InputError(Exception):
	"""Exception raised for errors in the input expression."""

	def __init__(self, message: str = None, span: Tuple[int, int] = None):
		self.message: str = message
		self.span: Tuple[int, int] = span

	def __str__(self):
		msg = "input error"
		if self.message:
			msg += f": {self.message}"

		return msg
