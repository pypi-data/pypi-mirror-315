"""Module for user authenticate with selenium.

This module contains utilities related to authenticating the user with selenium,
such as the Browser enum as well as the function for fetching the DSID cookie.
"""

import json
import logging
import sys
import time
from enum import Enum
from typing import Any
from urllib import request

from selenium import webdriver
from selenium.common.exceptions import (
	NoSuchElementException,
	TimeoutException,
	WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.wait import WebDriverWait

from jmu_openconnect.exceptions import MissingDSIDError, TimedOutError


class Browser(Enum):
	"""Specify a browser to use"""

	FIREFOX = {'driver': webdriver.Firefox, 'options': webdriver.FirefoxOptions}
	CHROME = {'driver': webdriver.Chrome, 'options': webdriver.ChromeOptions}
	EDGE = {'driver': webdriver.Edge, 'options': webdriver.EdgeOptions}


def fetch_latest_browser_version(browser: Browser) -> str:
	"""Fetches the latest firefox/chromium version from mozilla's/google's API.

	Args:
		browser (Browser): The browser to fetch the version number

	Returns:
		str: The version number as a string. Empty string if something went wrong
	"""
	if browser == Browser.FIREFOX:  # noqa: RET503
		firefox_ver = request.urlopen(  # pyright: ignore[reportAny]
			'https://product-details.mozilla.org/1.0/firefox_history_major_releases.json'
		)
		if firefox_ver.getcode() == 200:  # pyright: ignore[reportAny]
			try:
				# load firefox version info
				firefox_data: dict[str, str] = json.loads(firefox_ver.read())  # pyright: ignore[reportAny]
				# sort firefox version info by most recent release first
				ver = sorted(
					firefox_data.keys(), key=lambda ver: int(ver.split('.')[0])
				)
				# return the greatest version number (last in the list)
				return ver[-1]
			except json.JSONDecodeError:
				return ''
		else:
			return ''

	elif browser == Browser.CHROME:
		chrome_ver = request.urlopen(  # pyright: ignore[reportAny]
			'https://versionhistory.googleapis.com/v1/chrome/platforms/win/channels/stable/versions'
		)
		if chrome_ver.getcode() == 200:  # pyright: ignore[reportAny]
			try:
				# load chrome version info
				chrome_data: dict[str, list[dict[str, str]]] = json.loads(
					chrome_ver.read()  # pyright: ignore[reportAny]
				)
				# return the greatest version number (first in the list)
				return chrome_data['versions'][0]['version']
			except json.JSONDecodeError:
				return ''
		else:
			return ''
	elif browser == Browser.EDGE:
		edge_ver = request.urlopen(  # pyright: ignore[reportAny]
			'https://edgeupdates.microsoft.com/api/products/?view=enterprise'
		)
		if edge_ver.getcode() == 200:  # pyright: ignore[reportAny]
			try:
				# load edge version info
				edge_data: list[dict[str, Any]] = json.loads(edge_ver.read())  # pyright: ignore[reportAny]
				# find the latest stable release
				stable_rel = next(
					item for item in edge_data if item['Product'] == 'Stable'
				)
				# return the greatest version number (first in the list)
				return stable_rel['Releases'][0]['ProductVersion']  # pyright: ignore[reportAny]
			except json.JSONDecodeError:
				return ''
		else:
			return ''


def get_dsid_cookie(
	username: str = '',
	password: str = '',
	browser: Browser = Browser.FIREFOX,
	browser_binary: str | None = None,
	webdriver_timeout: int = 300,
	debug_auth_error: bool = False,
) -> str:
	"""Use selenium to fetch the user's DSID cookie after authentication.

	If both a username and password are provided, the "Log in" button will automatically be clicked.

	Args:
		username (str, optional): Automatically type in a username.
		password (str, optional): Automatically type in a password.
		browser (Browser, optional): Specify a browser to use. Defaults to FIREFOX.
		browser_binary: (str | None, optional): Specify a path to your browser's binary. Defaults to None.
		webdriver_timeout (int, optional): The amount of time before the webdriver times out. Defaults to 300.
		debug_auth_error (bool, optional): Whether or not to pause after authentication for debugging. Defaults to False.

	Raises:
		TimedOutError: If the webdriver timed out while waiting for authentication
		MissingDSIDError: If the DSID cookie was not found after authentication

	Returns:
		str: The DSID cookie
	"""
	logging.info("Fetching user's DSID cookie")

	# create browser specific options
	options = browser.value['options']()

	# set the path to the browser's binary if set
	if browser_binary is not None:
		logging.debug(f'Setting browser binary path to `{browser_binary}`')
		options.binary_location = browser_binary  # pyright: ignore[reportAttributeAccessIssue]

	# dynamically select the browser to use
	logging.debug('Launching browser')
	try:
		driver: webdriver.Firefox | webdriver.Chrome | webdriver.Edge = browser.value[  # pyright: ignore[reportRedeclaration, reportAssignmentType]
			'driver'
		](options=options)  # pyright: ignore[reportArgumentType, reportCallIssue]
	except WebDriverException as e:
		# catch invalid host header error
		if e.msg and 'Invalid Host header' in e.msg:
			logging.error(e)
			logging.info(
				'If running Linux, try adding `127.0.0.1 localhost` to your /etc/hosts'
			)
			sys.exit(1)

		# the browser version probably wasn't detected correctly, try to fetch it from the web
		logging.warning('Browser version incorrectly detected')
		logging.debug(e, exc_info=True)
		logging.info(f'Trying to retreieve latest browser version for {browser}')
		options.browser_version = fetch_latest_browser_version(browser)  # pyright: ignore[reportAttributeAccessIssue]
		logging.info(f'Latest browser version: {options.browser_version!r}')  # pyright: ignore[reportAttributeAccessIssue]
		logging.info('Relaunching browser')
		# retry launching
		driver: webdriver.Firefox | webdriver.Chrome | webdriver.Edge = browser.value[
			'driver'
		](options=options)  # pyright: ignore[reportArgumentType, reportCallIssue, reportAssignmentType]

	# driver has been successfully started
	logging.debug('Launching vpn.jmu.edu for authentication')
	driver.get('https://vpn.jmu.edu')

	# wait for the Duo prompt to show up
	WebDriverWait(driver, webdriver_timeout).until(
		EC.url_contains('itfederation.jmu.edu')
	)

	# try to input username
	if username:
		try:
			logging.debug('Inputting username')
			username_input = driver.find_element(By.NAME, 'j_username')
			username_input.send_keys(username)
		except NoSuchElementException:
			logging.warning('Username input not found')

	# try to input password
	if password:
		try:
			logging.debug('Inputting password')
			password_input = driver.find_element(By.NAME, 'j_password')
			password_input.send_keys(password)
		except NoSuchElementException:
			logging.warning('Password input not found')

	# automatically click the log in button if username and password were
	# both provided
	if username and password:
		try:
			logging.debug('Attempting to click the log in button')
			submit_button = driver.find_element(
				By.CSS_SELECTOR, "button[type='submit']"
			)
			submit_button.click()
		except NoSuchElementException:
			logging.warning('Log in button not found')

	try:
		# wait until the user authenticates, where they will then be redirected
		# to vpn.jmu.edu
		WebDriverWait(driver, webdriver_timeout).until(EC.url_contains('vpn.jmu.edu'))
	except TimeoutException as e:
		logging.debug('Quitting webdriver')
		driver.quit()

		raise TimedOutError from e

	# try to grab the DSID cookie from the user's storage
	dsid_cookie: dict[str, str] | None = driver.get_cookie('DSID')  # pyright: ignore[reportUnknownMemberType]

	# check if the DSID cookie was found
	if dsid_cookie is None:
		logging.error(
			"DSID cookie not found. Make sure that you're only signed in once. See README"
		)

		logging.debug('Quitting webdriver')
		driver.quit()

		raise MissingDSIDError

	if debug_auth_error:
		logging.debug('Pausing for 10 seconds since debug_auth_error is set')
		time.sleep(10)

	logging.debug('Quitting webdriver')
	driver.quit()

	return dsid_cookie['value']
