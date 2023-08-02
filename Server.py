import socket

def main():
    
    host = '192.168.254.104'  
    port = 12345  

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        serverSocket.bind((host, port))
        serverSocket.listen(5) 

        print(f"Server connected to {host}:{port}")
        print(f"Running message program.....") # insert lahat ng functions after this 

    except Exception as e:
        print(f"Error: {e}")
    finally:
        serverSocket.close()
        print("Server closed.")

if __name__ == "__main__":
    main()