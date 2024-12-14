# setup.py

from setuptools import setup, find_packages

setup(
    name="ducknotify",  
    version="1.0.0",  
    packages=find_packages(),  
    install_requires=["osascript", "notify-send", "plyer"],  
    description="**DuckNotify** is a lightweight, cross-platform Python library for sending desktop notifications effortlessly. It works on **Windows**, **macOS**, and **Linux**, providing a simple API to notify users with custom messages.",
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown", 
    author="freeutka",
    author_email="freeutka@inbox.lv",
    url="https://github.com/freeutka/DuckNotify", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)