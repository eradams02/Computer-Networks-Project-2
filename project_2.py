import sys
import socket
import random

class MainServer:
    def __init__(self):
        # Step 1: read command line arguments
        if len(sys.argv) != 5:
            print("Usage: python myserver.py -p [port] -l [log file destination]")
            sys.exit(1)

        if sys.argv[1] != '-p':
            print("Error: Invalid option for port number.")
            sys.exit(1)

        try:
            self.port = int(sys.argv[2])
        except ValueError:
            print("Error: Port number must be an integer.")
            sys.exit(1)

        if sys.argv[3] != '-l':
            print("Error: Invalid option for log file destination.")
            sys.exit(1)

        self.logFileDestination = str(sys.argv[4])

        # Step 2: create a socket object
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        # Step 3: bind and listen
        try:
            self.serverSocket.bind(('', self.port))
            self.serverSocket.listen(5)
            print(f"Server listening on port {self.port}")
        except socket.error as e:
            print("Error binding or listening:", e)
            sys.exit(1)

        while True:
            # Step 4: receive a message from the client
            clientSocket, address = self.serverSocket.accept()
            data = clientSocket.recv(1024).decode().strip()

           # Step 5: send a random quote
            if "network" in data.lower():
                with open("quotes.txt", "r") as f:
                    quotes = f.read().splitlines()
                response = random.choice(quotes)
                clientSocket.send(response.encode())

                # Step 6: log all interactions
                with open(self.logFileDestination, "a") as f:
                    f.write(f"Client {address[0]}:{address[1]} requested quote: {data}, response: {response}\n")


            else:
                response = "Please send a message containing the word 'network'."
                clientSocket.send(response.encode())

                # Step 6: log all interactions
                with open(self.logFileDestination, "a") as f:
                    f.write(f"Client {address[0]}:{address[1]} sent invalid message: {data}, response: {response}\n")

            clientSocket.close()

if __name__ == "__main__":
    server = MainServer()
    server.start()