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
                print("Connected to the server.\n")
                break  
            except Exception as e:
                print(f"Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number {e}")               
        elif parts[0].lower() == "/?":
            print("Input Syntax commands:")
            print("/join <server_ip_add> <port>")
            print("/leave")
            print("/quit")
            print("/register <handle>")
            print("/all <message>")
            print("/msg <handle> <message>")
            print("/?\n\n")
        elif parts[0].lower() == "/leave":
            print("Error: Disconnection failed. Please connect to the server first")
        elif parts[0].lower() =="/quit":
            print("Disconnecting...")
            client_socket.close()
        else:
            print("Error: Command parameters do not match or is not allowed. Usage: /join <ip_address> <port> or /?\n")
            
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    #receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    #receive_thread.start()

    try:
        while True:
            message = input()
            client_socket.sendall(message.encode('utf-8'))
            if message == "/quit":
                break
            elif message == "/?": 
                print("Input Syntax commands:")
                print("/join <server_ip_add> <port>")
                print("/leave")
                print("/quit")
                print("/register <handle>")
                print("/all <message>")
                print("/msg <handle> <message>")
                print("/?\n\n")
            elif message == "/leave": 
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
                            print(f"Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number {e}")               
                    elif parts[0].lower() == "/?":
                        print("Input Syntax commands:")
                        print("/join <server_ip_add> <port>")
                        print("/leave")
                        print("/register <handle>")
                        print("/all <message>")
                        print("/msg <handle> <message>")
                        print("/?\n\n")
                    elif parts[0].lower() == "/leave":
                        print("Error: Disconnection failed. Please connect to the server first")
                    else:
                        print("Error: Command parameters do not match or is not allowed. Usage: /join <ip_address> <port> or /?\n")                        
                receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
                receive_thread.start()

                receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
                receive_thread.start()
                
    except KeyboardInterrupt:
        pass

    print("Disconnecting...")
    client_socket.close()

if __name__ == "__main__":
    main()
