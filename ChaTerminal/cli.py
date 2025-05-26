from cha_terminal import server, client
import sys

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "init":
        print("Usage: ChaTerminal init [server|client]")
        sys.exit(1)

    mode = sys.argv[2]
    if mode == "server":
        server.main()
    elif mode == "client":
        client.main()
    else:
        print("Usage: ChaTerminal init [server|client]")
