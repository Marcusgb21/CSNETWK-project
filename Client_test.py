import socket
import threading

BUFFER_SIZE = 1024

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            print(data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def main():
    while True:
        command = input()
        parts = command.strip().split()

        if len(parts) == 3 and parts[0].lower() == "/join":
            ip_address = parts[1]
            port = int(parts[2])
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((ip_address, port))
                print("Connected to the server.")
                break  
            except Exception as e:
                print(f"Error connecting to the server: {e}")
        elif parts[0].lower() == "/?":
            print("Input Syntax commands:")
            print("/join <server_ip_add> <port>")
            print("/leave")
            print("/register <handle>")
            print("/all <message>")
            print("/msg <handle> <message>")
            print("/?")
        else:
            print("Invalid command format. Usage: /join <ip_address> <port> or /?")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            message = input()
            client_socket.sendall(message.encode('utf-8'))
            if message == "/leave":
                break
    except KeyboardInterrupt:
        pass

    print("Disconnecting...")
    client_socket.close()

if __name__ == "__main__":
    main()
