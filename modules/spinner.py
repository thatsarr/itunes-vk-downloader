import time
import sys


def spin(one_spin_time=0.5, spinner_array="|/-\\"):
    for char in spinner_array:
        print(char, end="")
        sys.stdout.flush()
        time.sleep(one_spin_time / len(spinner_array))
        print("\b", end="")
