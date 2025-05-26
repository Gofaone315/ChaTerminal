# ChaTerminal

**ChaTerminal** is a cross-platform terminal-based encrypted chat system built with Python. It supports multiple users on a local network or via tunneling tools like Ngrok or LocalXpose, providing a lightweight and interactive chat experience — right from the terminal.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/github/license/Gofaone315/ChaTerminal)
![Platform](https://img.shields.io/badge/Platform-Terminal-informational)

## Features

- **Encrypted communication** using custom crypto utilities
- **Multi-user chat** over LAN or tunneled internet
- **Color-coded messages** with timestamp formatting
- **Auto-complete** for commands via `readline` and TAB
- **Direct messaging** using `/dm <user> <message>`
- **Username renaming** with `/rename <new_name>`
- **List online users** using `/list`
- **Admin controls**: `/kick <user>` (admin-only)
- **Emote support**: `/me <action>`
- **Help menu**: `/help` displays command reference
- **User join/leave notifications**
- **Sound alert** for DMs and admin actions
- **Graceful client disconnect and server feedback**
- **Color personalization** based on username hash

## Getting Started

### Requirements

- Python 3.9+
- pip packages: `colorama`, `pyfiglet`, `readline` (Linux/macOS), `pyreadline3` (Windows)

### Installation

```bash
pip install ChaTerminal
```

### Running the Server

```bash
ChaTerminal init server
```

- Enter a port (e.g., `5555`) and the admin username
- Displays local IP with instructions for LAN or tunneled access

### Running the Client

In a **new terminal window**:

```bash
ChaTerminal init client
```

- Enter the server IP, port, and a unique username

## Commands

| Command             | Description                              |
|---------------------|------------------------------------------|
| `/dm <user> <msg>`  | Send a private message                   |
| `/kick <user>`      | Kick a user (admin only)                 |
| `/list`             | View online users                        |
| `/rename <name>`    | Change your username                     |
| `/me <action>`      | Send an action/emote (e.g., waves)       |
| `/help`             | Show all available commands              |

## Networking Tips

To let others join:

- **Local network**: Share the IP and port printed on server start
- **Ngrok**: `ngrok tcp <port>`
- **LocalXpose**: `./lx tcp <port>`
- **Port Forwarding**: Map the server's port on your router

## Example

```bash
# Start server
$ ChaTerminal init server
Port: 5555
Admin Username: admin

# Start client
$ ChaTerminal init client
Server IP: 192.168.1.100
Server Port: 5555
Username: myname
```

## Security Note

All messages are encrypted using the `crypto_utils` module before transmission. Ensure that this module uses secure encryption practices for production deployments.

## License

This project is licensed under the MIT License. See `LICENSE` for more info.

## Author

**Gofaone Tlalang**  
GitHub: [@Gofaone315](https://github.com/Gofaone315)

---

**ChaTerminal** – Real-time encrypted chat, right from your terminal.
