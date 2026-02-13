from pywinauto import Application
import win32gui


def get_browser_url():
    try:
        # Get handle of the active window
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd).lower()

        # Check if active window is a browser
        if "google chrome" in window_title or "microsoft edge" in window_title:
            app = Application(backend="uia").connect(handle=hwnd)
            window = app.window(handle=hwnd)

            # Find the address bar element
            # This works for Chrome and Edge (Chromium based)
            url_wrapper = window.child_window(title="Address and search bar", control_type="Edit")
            return url_wrapper.get_value()
    except Exception:
        return None
    return None