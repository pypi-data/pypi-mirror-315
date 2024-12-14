Here’s the description for **DuckNotify**:

---

# DuckNotify

**DuckNotify** is a lightweight, cross-platform Python library for sending desktop notifications effortlessly. It works on **Windows**, **macOS**, and **Linux**, providing a simple API to notify users with custom messages.

---

## Features
- **Cross-Platform Support**: Works on Windows, macOS, and Linux.
- **Custom Notifications**: Set a title, message, and optional icon for your notifications.
- **Lightweight**: Minimal dependencies and easy to use.

---

## Installation
Install DuckNotify using pip:

```bash
pip install ducknotify  
```

---

## Usage
Here’s how you can use DuckNotify to send notifications:

```python
import ducknotify

# Send a simple notification
ducknotify.notify("DuckNotify Alert", "This is your notification message!")

# Send a notification with an icon (optional)
ducknotify.notify("DuckNotify", "Message with an icon!", icon="icon.png")
```

---

## Supported Platforms
- **macOS**
- **Linux**
- **Windows**

---

## License
DuckNotify is licensed under the MIT License, making it free and open-source for everyone.