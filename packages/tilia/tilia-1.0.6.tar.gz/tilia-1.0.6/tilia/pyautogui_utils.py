import time
import pyautogui
import pygetwindow as gw
import pyperclip

def wait_for_window(window_title, timeout=7, wait=0.5):
	"""
	Wait for a window with a specific title to become active.

	Args:
		window_title (str): The title of the window to wait for.
		timeout (float, optional): Maximum time (in seconds) to wait. Default is 7 seconds.
		wait (float, optional): Interval between checks (in seconds). Default is 0.5 seconds.

	Returns:
		bool: True if the window becomes active within the timeout, False otherwise.

	Example:
		>>> wait_for_window("SAP Logon 760")
	"""
	start_time = time.time()
	while time.time() - start_time < timeout:
		active_window_title = gw.getActiveWindow().title
		if active_window_title == window_title:
			return True
		time.sleep(wait)
	return False

def relative_to_absolute(x_rel, y_rel):
	"""
	Convert relative screen coordinates to absolute coordinates based on screen size.

	Args:
		x_rel (float): The relative x-coordinate (0.0 to 1.0).
		y_rel (float): The relative y-coordinate (0.0 to 1.0).

	Returns:
		tuple: The corresponding absolute x and y coordinates.

	Example:
		>>> relative_to_absolute(0.5, 0.5)
		(960, 540)
	"""
	screen_width, screen_height = pyautogui.size()
	x_abs = x_rel * screen_width
	y_abs = y_rel * screen_height
	return x_abs, y_abs

def mouse_click(x, y, absolute=False, wait=0):
	"""
	Simulate a mouse click at the specified coordinates.

	Args:
		x (float): The x-coordinate for the mouse click.
		y (float): The y-coordinate for the mouse click.
		absolute (bool, optional): If True, use absolute coordinates. If False, use relative coordinates. Default is False.
		wait (float, optional): Time to wait before performing the click. Default is 0 seconds.

	Example:
		>>> mouse_click(0.5, 0.5)
	"""
	if not absolute:
		x, y = relative_to_absolute(x, y)
	pyautogui.moveTo(x, y)
	time.sleep(wait)
	pyautogui.click()

def press_key(key, times=1):
	"""
	Simulate pressing a key multiple times.

	Args:
		key (str): The key to press (e.g., 'enter', 'space').
		times (int, optional): The number of times to press the key. Default is 1.

	Example:
		>>> press_key('enter', 2)
	"""
	for _ in range(times):
		pyautogui.press(key)

def enter_value(value, wait=0.2):
	"""
	Type a value and press the Enter key.

	Args:
		value (str): The value to type.
		wait (float, optional): Time to wait after typing before pressing Enter. Default is 0.2 seconds.

	Example:
		>>> enter_value("Hello, World!")
	"""
	pyautogui.typewrite(value)
	time.sleep(wait)
	press_key('enter')

def exit_if_not_window(value, timeout=7, wait=0.5):
	"""
	Exit the program if the specified window is not active within the timeout period.

	Args:
		value (str): The title of the window to check.
		timeout (float, optional): Maximum time (in seconds) to wait for the window. Default is 7 seconds.
		wait (float, optional): Interval between checks (in seconds). Default is 0.5 seconds.

	Example:
		>>> exit_if_not_window("SAP Logon 760")
	"""
	if not wait_for_window(value, timeout, wait):
		exit(f"Couldn't reach {value}")

def save_from_clipboard(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste=False, absolute=False):
	"""
	Simulate selecting a portion of the screen and saving it to the clipboard.

	Args:
		rel_start_x (float): The relative starting x-coordinate of the selection.
		rel_start_y (float): The relative starting y-coordinate of the selection.
		rel_end_x (float): The relative ending x-coordinate of the selection.
		rel_end_y (float): The relative ending y-coordinate of the selection.
		sap_paste (bool, optional): If True, presses ("ctrl" + "y") hotkey before copying the content. Default is False.
		absolute (bool, optional): If True, use absolute coordinates. Default is False.

	Returns:
		str: The text copied to the clipboard.

	Example:
		>>> save_from_clipboard(0.1, 0.1, 0.5, 0.5)
	"""
	pyperclip.copy('0')

	if not absolute:
		abs_start_x, abs_start_y = relative_to_absolute(rel_start_x, rel_start_y)
		abs_end_x, abs_end_y = relative_to_absolute(rel_end_x, rel_end_y)
	else:
		abs_start_x, abs_start_y = rel_start_x, rel_start_y
		abs_end_x, abs_end_y = rel_end_x, rel_end_y

	if sap_paste:
		pyautogui.hotkey("ctrl", "y")
	pyautogui.moveTo(abs_start_x, abs_start_y)
	pyautogui.mouseDown()
	pyautogui.moveTo(abs_end_x, abs_end_y)
	pyautogui.mouseUp()

	pyautogui.hotkey("ctrl", "c")
	time.sleep(0.1)
	return pyperclip.paste()

def force_clipboard_content(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste=False, absolute=False, direction='Down', horizontal=False, ratio=0.008):
	"""
	Force the content of the clipboard by repeatedly trying to copy a portion of the screen.

	Args:
		rel_start_x (float): The relative starting x-coordinate of the selection.
		rel_start_y (float): The relative starting y-coordinate of the selection.
		rel_end_x (float): The relative ending x-coordinate of the selection.
		rel_end_y (float): The relative ending y-coordinate of the selection.
		sap_paste (bool, optional): If True, presses ("ctrl" + "y") hotkey before copying the content. Default is False.
		absolute (bool, optional): If True, use absolute coordinates. Default is False.
		direction (str, optional): Direction to move the selection ('Up' or 'Down'). Default is 'Down'.
		horizontal (bool, optional): If True, adjust selection horizontally instead of vertically. Default is False.
		ratio (float, optional): The ratio for adjusting the selection position. Default is 0.008.

	Returns:
		str: The text copied to the clipboard.

	Example:
		>>> force_clipboard_content(0.1, 0.1, 0.5, 0.5)
	"""
	down = 1
	if direction == 'up':
		down = -1
	message = save_from_clipboard(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste)
	if not message or message == '0':
		if not horizontal:
			return force_clipboard_content(rel_start_x, rel_start_y + (ratio * down), rel_end_x, rel_end_y + (ratio * down), sap_paste, absolute)
		else:
			return force_clipboard_content(rel_start_x + (ratio * down), rel_start_y, rel_end_x + (ratio * down), rel_end_y, sap_paste, absolute)
	else:
		return message
