import socket
import threading
import hashlib
import readline
import platform
import time
import sys
from .crypto_utils import encrypt_msg, decrypt_msg
from .splash import splash
from colorama import init, Fore, Style

COMMANDS = ["/dm", "/kick", "/list", "/me", "/rename", "/help"]
client = None

def completer(text, state):
    options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    return options[state] if state < len(options) else None

def get_user_color(name):
    hash_val = int(hashlib.sha256(name.encode()).hexdigest(), 16)
    colors = [Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.YELLOW, Fore.BLUE, Fore.WHITE]
    return colors[hash_val % len(colors)]

def sound_alert():
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(800, 150)
        else:
            import os
            os.system('printf "\\a"')
    except:
        pass

def receive():
    while True:
        try:
            msg = client.recv(2048)
            if not msg:
                print("\n[!] Server disconnected.")
                break
            text = decrypt_msg(msg)
            if "[DM from" in text or "kicked" in text:
                sound_alert()

            if "[DM" in text:
                print(f"\r{Fore.MAGENTA}{text}{Style.RESET_ALL}\n> ", end="")
            elif "[+]" in text:
                print(f"\r{Fore.GREEN}{text}{Style.RESET_ALL}\n> ", end="")
            elif "[-]" in text:
                print(f"\r{Fore.YELLOW}{text}{Style.RESET_ALL}\n> ", end="")
            elif "[!]" in text:
                print(f"\r{Fore.RED}{text}{Style.RESET_ALL}\n> ", end="")
            elif "* " in text:
                print(f"\r{Fore.BLUE}{text}{Style.RESET_ALL}\n> ", end="")
            elif ": " in text:
                timestamp, rest = text.split("] ", 1)
                timestamp += "]"
                name, msg = rest.split(": ", 1)
                color = get_user_color(name.strip())
                print(f"\r{timestamp} {color}{name}{Style.RESET_ALL}: {msg}\n> ", end="")
            else:
                print(f"\r{text}\n> ", end="")
        except Exception as e:
            print(f"\n[!] Connection lost: {e}")
            break

    try:
        client.close()
    except:
        pass

def send():
    while True:
        try:
            msg = input("> ")
            client.sendall(encrypt_msg(msg))
        except:
            break

def main():
    global client
    splash()
    init(autoreset=True)
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    SERVER = input("Server IP: ")
    PORT = int(input("Server Port: "))
    username = input("Username: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER, PORT))
        client.sendall(encrypt_msg(username))
    except Exception as e:
        print(f"[!] Could not connect: {e}")
        return

    threading.Thread(target=receive, daemon=True).start()
    send()
