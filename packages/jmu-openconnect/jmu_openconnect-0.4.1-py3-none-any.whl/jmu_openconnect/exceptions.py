"""This module contains custom exceptions that are used throughout the program."""

from typing import Any


class MissingDSIDError(Exception):
	"""Raised if DSID cooke was not found."""

	def __init__(
		self,
		msg: str = 'DSID Cookie was not found',
		*args: tuple[Any, ...],
		**kwargs: Any,  # pyright: ignore[reportAny]
	):
		super().__init__(msg, *args, **kwargs)


class TimedOutError(Exception):
	"""Raised if the webdriver timed out while waiting for authentication."""

	def __init__(
		self,
		msg: str = 'webdriver timed out while waiting for authentication',
		*args: tuple[Any, ...],
		**kwargs: Any,  # pyright: ignore[reportAny]
	):
		super().__init__(msg, *args, **kwargs)


class MissingOpenConnectError(Exception):
	"""If openconnect could not be found on the PATH."""

	def __init__(
		self,
		msg: str = "openconnect binary could not be found. make sure it's installed and on your PATH",
		*args: tuple[Any, ...],
		**kwargs: Any,  # pyright: ignore[reportAny]
	):
		super().__init__(msg, *args, **kwargs)
