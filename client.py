import socket
import json
import threading

def receive_messages(sock):

    while True:
        try:
            data, _ = sock.recvfrom(1024)
            message = json.loads(data.decode())
            print_message(message)

        except json.JSONDecodeError:
            print("Error: Invalid JSON data received.")
        except Exception as e:
            print(f"Error: {e}")

def print_message(message):

    if 'connection_success' in message:
        print("Connection to the Message Board Server is successful!")
    elif 'connection_closed' in message:
        print("Connection closed. Thank you!")
    elif 'handle_registered' in message:
        print(f"Welcome {message['handle']}!")
    elif 'message_all' in message:
        print(f"{message['handle']}: {message['content']}")
    elif 'message_direct' in message:
        print(f"[To: {message['receiver']}]: {message['content']}")
    elif 'message_received' in message:
        print(f"[From: {message['handle']}] : {message['content']}")
    elif 'error' in message:
        print(f"Error: {message['error']}")
    else:
        print("Error: Invalid message received.")

def main():

    server_ip = ""
    server_port = 0
    handle = ""
    sock = None

    while True:
        command = input()

        if command.startswith('/join'):
            _, server_ip, server_port = command.split()
            try:
                server_port = int(server_port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(json.dumps({'command': '/join'}).encode(), (server_ip, server_port))
                response, _ = sock.recvfrom(1024)
                print_message(json.loads(response.decode()))
                threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
            except ValueError:
                print("Error: Invalid port number.")
            except Exception as e:
                print(f"Error: {e}")

        elif command == '/leave':
            if sock:
                sock.sendto(json.dumps({'command': '/leave'}).encode(), (server_ip, server_port))
                sock.close()
                sock = None
            else:
                print("Error: Disconnection failed. Please connect to the server first.")

        elif command.startswith('/register'):
            _, handle = command.split(maxsplit=1)
            if sock:
                sock.sendto(json.dumps({'command': '/register', 'handle': handle}).encode(), (server_ip, server_port))
            else:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

        elif command.startswith('/all'):
            message = command.split(maxsplit=1)[1]
            if sock:
                sock.sendto(json.dumps({'command': '/all', 'handle': handle, 'content': message}).encode(), (server_ip, server_port))
            else:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

        elif command.startswith('/msg'):
            _, receiver_handle, message = command.split(maxsplit=2)
            if sock:
                sock.sendto(json.dumps({'command': '/msg', 'handle': handle, 'receiver': receiver_handle, 'content': message}).encode(), (server_ip, server_port))
            else:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

        elif command == '/?':
            print("Input Syntax commands:")
            print("/join <server_ip_add> <port>")
            print("/leave")
            print("/register <handle>")
            print("/all <message>")
            print("/msg <handle> <message>")
            print("/?")

        else:
            print("Error: Command not found")

if __name__ == "__main__":
    main()
