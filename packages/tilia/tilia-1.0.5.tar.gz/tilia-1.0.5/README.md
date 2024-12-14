This library provides a set of utilities designed to automate repetitive human interactions on a computer. By leveraging the power of the `pyautogui` library, this package allows for easy automation of simple tasks such as mouse movements, clicks, keyboard presses, window focus checks, and clipboard operations.

---

## What’s Included

### `pyautogui_utils` Functions

`mouse_click(x, y, absolute=False, wait=0)`
Simulate a mouse click at the specified coordinates.

`press_key(key, times=1)`
Simulate pressing a key multiple times.

`enter_value(value, wait=0.2)`
Type a value, wait a bit and press Enter.

`wait_for_window(window_title, timeout=7, wait=0.5)`
Wait for a window with a specific title to become active.

**Example usage:**
```python
press_key('winleft')
wait_for_window("Search")
```

`exit_if_not_window(value, timeout=7, wait=0.5)`
Calls wait_for_window() and exits the program if it returns False.

`relative_to_absolute(x_rel, y_rel)`
Convert relative screen coordinates to absolute coordinates based on screen size.

**Example usage:**
```python
relative_to_absolute(0.5, 0.5)
# Output: (960, 540) -- for a screen resolution of 2560 x 1440
```

`save_from_clipboard(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste=False, absolute=False)`
Simulate selecting a portion of the screen and saving it to the clipboard.
Per default works with relative coordinates.

`force_clipboard_content(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste=False, absolute=False, direction='Down', horizontal=False, ratio=0.008)`
Force the clipboard content by repeatedly calling save_from_clipboard() with slightly varying coordinates.

### `SAPAutomation` Class (in `sap_utils.py`)

This class provides an interface for automating SAP tasks, allowing you to perform common actions such as logging into SAP, navigating through menus, and copying data to the clipboard. It uses the `pyautogui_utils` functions to simulate user actions in SAP.

**Example usage:**
```python
from sap_utils import SAPAutomation

sap = SAPAutomation("username", "password")
sap.open_sap() # Opens SAP GUI Interface and logs with username and password
...
sap.go_to_main_page()
sap.close_sap()
```

## Installation

To install the package, simply clone the repository and install the required dependencies:

```bash
git clone https://github.com/rafonsomartins/tilia
cd tilia
pip install -r requirements.txt
```
---

## License

This project is licensed under the MIT License.

---

## Next Steps and Potential Vulnerabilities

### Error Handling
Implement structured exception handling (try/except) to ensure better error recovery and debugging.

### Testing
Implement unit tests for all utility functions and mock interactions to allow testing without relying on real-world systems.

### Dynamic Window Titles
Enhance window title-finding logic using regex or partial matches.

### Performance Optimization
Avoid using `time.sleep()` and explore event-driven approaches to improve performance. Ensure that `force_clipboard_content()` doesn't loop infinitely by adding a maximum retry count or exit condition.

### Robustness and Safety
Implement input validation for user inputs and add logging for events and errors to make debugging easier.
