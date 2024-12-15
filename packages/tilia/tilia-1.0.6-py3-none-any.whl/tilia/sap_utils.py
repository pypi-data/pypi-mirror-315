import pyautogui
import time
from .pyautogui_utils import exit_if_not_window, enter_value, wait_for_window, press_key

class SAPAutomation:
	"""
    A class to encapsulate SAP GUI automation tasks.

    Methods:
        navigate_to_transaction(transaction): Navigates to a specific SAP transaction.
        enter_data(field_data): Enters data into specified fields in SAP.
    """
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def open_sap(self):
		"""Opens the SAP application and logs in."""
		press_key('winleft')
		time.sleep(0.2)
		exit_if_not_window("Search")
		enter_value("SAP")

		exit_if_not_window("SAP Logon 740")

		press_key('enter')

		exit_if_not_window("SAP")

		pyautogui.typewrite(str(self.username))
		time.sleep(0.1)
		press_key('down')
		enter_value(str(self.password))

		exit_if_not_window("SAP Easy Access")

		pyautogui.hotkey("alt", "space")
		press_key("x")

		time.sleep(0.2)
		print("Successfully logged into SAP.")
		return True

	def go_to_main_page(self):
		"""Navigates to the main SAP page."""
		for _ in range(5):
			if wait_for_window("SAP Easy Access", timeout=0.5):
				return True
			press_key('esc')
		raise RuntimeError("Couldn't reach SAP main page.")

	def close_sap(self):
		"""Closes the SAP application."""
		pyautogui.hotkey("alt", "f4")
		time.sleep(0.2)
		press_key("tab")
		press_key("enter")
		print("SAP closed successfully.")
		return True
