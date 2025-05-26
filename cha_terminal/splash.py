import pyfiglet
import time
import sys

def typewriter(text, delay=0.005, beep=False):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if beep and char not in [' ', '\n']:
            sys.stdout.write('\a')  # ASCII bell
            sys.stdout.flush()
        time.sleep(delay)
    print()

def splash():
    banner = pyfiglet.figlet_format("ChaTerminal", font="slant")
    print("\033[1;32m", end="")  # Green
    typewriter(banner, delay=0.002, beep=True)

    print("\033[1;34m", end="")  # Blue
    typewriter("[ secure terminal chat • \033[1;35mChaTerminal\033[1;34m ]", delay=0.01, beep=True)

    print("\033[0m")  # Reset color
