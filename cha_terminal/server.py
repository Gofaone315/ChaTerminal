import socket
import threading
from datetime import datetime
from .crypto_utils import encrypt_msg, decrypt_msg
from .splash import splash

HOST = '0.0.0.0'
PORT = None
ADMIN_USERNAME = None
clients = {}
usernames = {}

def broadcast(message, exclude_socket=None):
    for client in list(clients):
        if client != exclude_socket:
            try:
                client.sendall(encrypt_msg(message))
            except:
                remove_client(client)

def remove_client(sock):
    try:
        if sock in clients:
            username = clients[sock]
            del usernames[username]
            del clients[sock]
            sock.close()
            broadcast(f"[-] {username} has left the chat.")
    except Exception as e:
        print(f"[ERROR: remove_client] {e}")

def handle_client(client):
    try:
        username = decrypt_msg(client.recv(1024))
        if username in usernames:
            client.sendall(encrypt_msg("[!] Username already taken."))
            client.close()
            return

        clients[client] = username
        usernames[username] = client
        broadcast(f"[+] {username} joined the chat.")

        while True:
            raw = client.recv(2048)
            if not raw:
                break
            msg = decrypt_msg(raw)
            timestamp = datetime.now().strftime("[%H:%M]")

            if msg.startswith("/dm "):
                _, to_user, *message = msg.split()
                message = " ".join(message)
                if to_user in usernames:
                    target_socket = usernames[to_user]
                    target_socket.sendall(encrypt_msg(f"{timestamp} [DM from {username}] {message}"))
                    client.sendall(encrypt_msg(f"{timestamp} [DM to {to_user}] {message}"))
                else:
                    client.sendall(encrypt_msg("[!] User not found."))

            elif msg.startswith("/kick ") and username == ADMIN_USERNAME:
                _, to_kick = msg.split()
                if to_kick in usernames:
                    kick_socket = usernames[to_kick]
                    kick_socket.sendall(encrypt_msg("[!] You have been kicked by admin."))
                    remove_client(kick_socket)
                    broadcast(f"[!] {to_kick} was kicked by admin.")
                else:
                    client.sendall(encrypt_msg("[!] User not found."))

            elif msg.startswith("/list"):
                active_users = ", ".join(usernames.keys())
                client.sendall(encrypt_msg(f"[Users Online] {active_users}"))

            elif msg.startswith("/rename "):
                newname = msg.split()[1]
                if newname in usernames:
                    client.sendall(encrypt_msg("[!] Username already taken."))
                else:
                    broadcast(f"[!] {username} changed name to {newname}")
                    del usernames[username]
                    usernames[newname] = client
                    clients[client] = newname
                    username = newname

            elif msg.startswith("/help"):
                help_text = (
                    "\033[1;36m[ChaTerminal Help Menu]\033[0m\n"
                    "\033[1;33m/dm <user> <msg>\033[0m   - Send a private message\n"
                    "\033[1;33m/kick <user>\033[0m       - Kick a user (admin only)\n"
                    "\033[1;33m/list\033[0m              - List online users\n"
                    "\033[1;33m/rename <newname>\033[0m  - Change your username\n"
                    "\033[1;33m/me <action>\033[0m       - Perform an action\n"
                    "\033[1;33m/help\033[0m              - Show this help menu\n"
                )
                client.sendall(encrypt_msg(help_text))

            else:
                broadcast(f"{timestamp} {username}: {msg}", exclude_socket=client)

    except Exception as e:
        print(f"[ERROR: handle_client] {e}")
    finally:
        remove_client(client)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unavailable"

def print_colored_box(lines, border_color="\033[96m", text_color="\033[97m"):
    reset = "\033[0m"
    width = max(len(line) for line in lines) + 4
    print(f"{border_color}┌{'─' * width}┐{reset}")
    for line in lines:
        print(f"{border_color}│{reset} {text_color}{line.ljust(width - 2)}{reset} {border_color}│{reset}")
    print(f"{border_color}└{'─' * width}┘{reset}")

def main():
    global PORT, ADMIN_USERNAME
    splash()
    PORT = int(input("Port: "))
    ADMIN_USERNAME = input("Admin Username: ")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    local_ip = get_local_ip()
    info_lines = [
        f"ChaTerminal running on local IP: {local_ip}:{PORT}",
        "Other users on the same Wi-Fi/LAN can connect using this IP.",
        "",
        "To allow others to connect over the internet:",
        f" - Use Ngrok:      ngrok tcp {PORT}",
        f" - Or LocalXpose:  ./lx tcp {PORT}",
        f" - Or port forward your router to {local_ip}",
        "",
        "Then share the public IP/URL and port with clients."
    ]
    print_colored_box(info_lines)

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
