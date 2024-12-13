#!/usr/bin/env python3

import getpass
import logging
import os
import shutil
import subprocess
import sys

from typing_extensions import override

from jmu_openconnect.argument_parser import parse_args
from jmu_openconnect.auth import Browser, get_dsid_cookie
from jmu_openconnect.exceptions import (
	MissingDSIDError,
	MissingOpenConnectError,
	TimedOutError,
)


class CustomLoggingFormatter(logging.Formatter):
	grey: str = '\x1b[30;1m'
	yellow: str = '\x1b[33;20m'
	red: str = '\x1b[31;20m'
	bold_red: str = '\x1b[31;1m'
	blue: str = '\u001b[34;1m'
	reset: str = '\x1b[0m'
	fmt: str = (
		'%(asctime)s | %(levelname)s | %(module)s:%(module)s:%(lineno)d - %(message)s'
	)

	FORMATS: dict[int, str] = {
		logging.DEBUG: grey + fmt + reset,
		logging.INFO: blue + fmt + reset,
		logging.WARNING: yellow + fmt + reset,
		logging.ERROR: red + fmt + reset,
		logging.CRITICAL: bold_red + fmt + reset,
	}

	@override
	def format(self, record: logging.LogRecord) -> str:
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)


def find_root_program() -> list[str]:
	"""Check whether sudo or doas is installed on the system.

	Returns:
		list[str]: sudo or doas, if installed. Empty list if not.
	"""
	for prog in ('doas', 'sudo'):
		if shutil.which(prog):
			return [prog]
	return []


def start_openconnect(dsid_cookie: str) -> int:
	"""Start openconnect with the specified DSID cookie.

	Args:
		dsid_cookie (str): The DSID cookie to authenticate with

	Raises:
		MissingOpenConnectError: If openconnect couldn't be found on the PATH
		PermissionError: If the user isn't root and sudo/doas couldn't be found

	Returns:
		int: the openconnect return code
	"""
	logging.info('Starting openconnect')

	logging.debug('Checking if openconnect is installed')
	if shutil.which('openconnect') is None:
		raise MissingOpenConnectError

	as_root = find_root_program()
	logging.debug(f'Root program identified: {as_root}')

	# check if the script is running as root or if sudo/doas were not found
	# os.geteuid() will be 0 if root
	if os.geteuid() and not as_root:
		raise PermissionError('sudo/doas were not found')

	oc_command = as_root + [
		'openconnect',
		'--protocol',
		'pulse',
		'--cookie',
		dsid_cookie,
		'https://vpn.jmu.edu',
	]

	logging.debug(f'OC Command: {oc_command}')

	# we use subprocess.call to prompt the user for root if needed, and return the return code
	return subprocess.call(oc_command)


def main():
	# set up custom logging formatting
	handler = logging.StreamHandler()
	handler.setFormatter(CustomLoggingFormatter())
	logging.basicConfig(
		level=os.environ.get('LOGLEVEL', 'INFO').upper(),
		format='%(asctime)s | %(levelname)s | %(module)s:%(module)s:%(lineno)d - %(message)s',
		handlers=[handler],
	)

	logging.warning(
		'This project is based on Ivanti Pulse Secure, which JMU no longer uses as of January 6th, 2025. Now that JMU has switched to GlobalProtect, you can switch to using https://github.com/yuezk/GlobalProtect-openconnect if needed.'
	)

	args = parse_args()

	if not args.only_authenticate:
		# check for openconnect before making the user authenticate
		logging.debug('Checking if openconnect is installed')
		if shutil.which('openconnect') is None:
			print(
				'openconnect was not found on your PATH. Please ensure that openconnect is installed.'
			)
			sys.exit(1)

	# check if we need to prompt the user for a password
	password = args.password
	if args.prompt_password:
		password = getpass.getpass('Password: ')

	# assign the browser to use. argparse guarentees that it will be one of these three
	browser = {
		'firefox': Browser.FIREFOX,
		'chrome': Browser.CHROME,
		'edge': Browser.EDGE,
	}[args.browser]

	try:
		dsid_cookie = get_dsid_cookie(
			username=args.username,
			password=password,
			browser=browser,
			browser_binary=args.browser_binary,
			webdriver_timeout=args.timeout,
			debug_auth_error=args.debug_auth_error,
		)
	except TimedOutError:
		print('webdriver timed out while waiting for authentication')
		sys.exit(1)
	except MissingDSIDError:
		print(
			'DSID Cookie was not found. Ensure that you are not logged in multiple times. See README for details.'
		)
		sys.exit(1)

	if args.only_authenticate:
		print(dsid_cookie)
		sys.exit(0)

	exit_code = 0
	try:
		exit_code = start_openconnect(dsid_cookie=dsid_cookie)
	except MissingOpenConnectError:
		print(
			'openconnect was not found on your PATH. Please ensure that openconnect is installed.'
		)
		exit_code = 1
	except PermissionError:
		print(
			'sudo was not found on your PATH. Please install sudo or run this script as root.'
		)
		exit_code = 1

	sys.exit(exit_code)


if __name__ == '__main__':
	main()
