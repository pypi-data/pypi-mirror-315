This library provides a set of utilities designed to automate repetitive human interactions on a computer. By leveraging the power of the `pyautogui` library, this package allows for easy automation of simple tasks such as mouse movements, clicks, keyboard presses, window focus checks, and clipboard operations. The library is especially helpful in scenarios where you need to automate SAP interactions or other desktop applications without manually repeating actions across different projects.

---

### `SAPAutomation` Class (in `sap_utils.py`)

This class provides an interface for automating SAP tasks, allowing you to perform common actions such as logging into SAP, navigating through menus, and copying data to the clipboard. It uses the `pyautogui_utils` functions to simulate user actions in SAP.

**Example usage:**
```python
from sap_utils import SAPAutomation

sap = SAPAutomation()
sap.login("username", "password")
sap.select_item("item_name")
sap.copy_data()

## Installation

To install the package, simply clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/automation-utils.git
cd automation-utils
pip install -r requirements.txt

## Requirements
- Python 3.x
- pyautogui
- pygetwindow
- pyperclip
- Other dependencies listed in `requirements.txt`

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
