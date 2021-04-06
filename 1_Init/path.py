import os
import sys


def get_current_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

def get_const_dir():
    return os.path.join(get_current_dir(1),"Const")