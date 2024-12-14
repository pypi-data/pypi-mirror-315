# ducknotify/__init__.py
# python setup.py sdist bdist_wheel
# twine upload dist/*

import os
import platform
import subprocess

def notify(title, message, icon=None):
    system = platform.system()

    if system == "Darwin": 
        command = f'osascript -e \'display notification "{message}" with title "{title}"\''
        subprocess.run(command, shell=True)
    elif system == "Linux":
        command = ["notify-send", title, message]
        if icon:
            command.extend(["-i", icon])
        subprocess.run(command)
    elif system == "Windows":
        try:
            from plyer import notification
            notification.notify(
                title=title,
                message=message,
                app_icon=icon, 
                timeout=5,  
            )
        except ImportError:
            pass
    else:
        raise NotImplementedError(f"DuckNotify are not supported on {system}.")