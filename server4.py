# server4.py : Your server program "server4.py" will be an echo server (that replies the
# same message to the client that was received from the same client); it will be a single
# process server that uses the "select" method to handle multiple clients concurrently

import socket
import select
import sys

def main():
    
    # Check command line arguments
    n = len(sys.argv)

    if n != 3:
        print("Usage: python server4.py <SERVER_IP> <SERVER_PORT>")
        sys.exit()

    SERVER_IP = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
    
    # Create a TCP/IP socket
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Server started on %s:%d\n' % (SERVER_IP, SERVER_PORT))

        # Bind the socket to the port
        server.bind((SERVER_IP, SERVER_PORT))

        # Listen for incoming connections
        server.listen(5)

        print('Server is listening for incoming connections...')

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()
        
    inputs = [server]
    outputs = []
        
    # Main loop of the server
    try:
        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for s in readable:  
                if s is server: # New connection
                    connection, client_address = s.accept()
                    print(f'Connection from {client_address} has been established.')
                    connection.setblocking(0)
                    inputs.append(connection)
                else:
                    # Data received from a client
                    data = s.recv(1024)
                    if data:
                        print(f"Received data from {s.getpeername()}: {data.decode('utf-8')}")
                        s.sendall(data)
                    else:
                        print(f"Connection from {s.getpeername()} has been closed.")
                        inputs.remove(s)
                        s.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()
    except KeyboardInterrupt:
        print("Server has been terminated.")
    finally:
        # Close all client sockets and the server socket
        for s in inputs:
            s.close()
        server.close()
        
if __name__ == "__main__":
    main()    