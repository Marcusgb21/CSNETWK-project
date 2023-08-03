import socket
import threading
import json

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024

# List to store client sockets and usernames
clients = {}
client_lock = threading.Lock()

def handle_client(client_socket, addr):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not data:
                break
            # Handle commands sent by the client
            handle_command(data, client_socket)
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break

    with client_lock:
        if client_socket in clients:
            del clients[client_socket]
            client_socket.close()

def handle_command(command, client_socket):
    # Split command into parts
    parts = command.strip().split()
    if not parts:
        return

    if parts[0].startswith("/"):
        # Parse command      
        if parts[0] == "/join":
            if len(parts) == 3:
                client_socket.sendall("Error: You have already joined a server, leave to join a new one\n".encode('utf-8'))
            else:
                client_socket.sendall("Error: Command paramaters do not match, the format is: /join <IP address> <port>\n".encode('utf-8'))     
        elif parts[0] == "/register":
            if len(parts) == 2:
                username = parts[1]
                with client_lock:
                    if any(username == value for value in clients.values()):
                        client_socket.sendall("Error: Handle or alias already exists\n".encode('utf-8'))
                    else:
                        clients[client_socket] = username
                        client_socket.sendall(f"Welcome {username}!\n".encode('utf-8'))
            else:
                client_socket.sendall("Error: Command paramaters do not match, the format is: /register <username>\n".encode('utf-8'))
        elif parts[0] == "/msg":
            if len(parts) >= 3:
                to_username = parts[1]
                message = ' '.join(parts[2:])
                with client_lock:
                    for client, username in clients.items():
                        if username == to_username:
                            client.sendall(f"[From {clients[client_socket]}]: {message}\n".encode('utf-8'))
                            break
                    else:
                        client_socket.sendall(f"Error: Handle or alias not found\n".encode('utf-8'))
            else:
                client_socket.sendall("Error: Command paramaters do not match, the format is: /msg <username> <message>\n".encode('utf-8'))
        elif parts[0] == "/all":
            if len(parts) >= 2:
                # Broadcast the message to all connected clients
                message = ' '.join(parts[1:])
                with client_lock:
                    for client in clients.keys():
                        client.sendall(f"{clients[client_socket]}: {message}\n".encode('utf-8'))
            else:
                client_socket.sendall("Error: Command parameters do not match or is not allowed. The format is: /all <message>\n".encode('utf-8'))
        elif parts[0] == "/?":
            return
        elif parts[0] == "/leave":
            client_socket.sendall("Error: Command parameters do not match or is not allowed.\n".encode('utf-8'))
        elif parts[0] == "/quit":
            return
        else:
                client_socket.sendall("Error: Command syntax doesn't exist\n".encode('utf-8'))
    else:
        with client_lock:
            username = clients.get(client_socket, "Unknown User")
            message = f"[{username}]: {command}\n"
            for client in clients.keys():
                if client != client_socket:
                    client.sendall(message.encode('utf-8'))

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

    except KeyboardInterrupt:
        server_socket.close()
        print("Connection closed. Thank you!")

if __name__ == "__main__":
    main()
