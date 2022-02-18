"""Greet someone.

Usage:
    package NAME
    
"""
import sys


def greet(name: str):
    message = f"Hello {name}!"
    print(message)
    return message


def run():
    greet(sys.argv[1])
