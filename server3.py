# server3.py : Your server program "server3.py " will be a single process server that uses
# the "select" method to handle multiple clients concurrently.

import socket
import select
import sys

def evaluate_expression(expression):
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Invalid expression"
    
def main():
    
    # Check command line arguments
    n = len(sys.argv)

    if n != 3:
        print("Usage: python server3.py <SERVER_IP> <SERVER_PORT>")
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
                        expression = data.decode('utf-8')
                        print(f"Received from client at {client_address}: {expression}")
                        result = evaluate_expression(expression)
                        s.sendall(result.encode('utf-8'))
                    else:
                        print(f"Connection from {client_address} has been closed.")
                        inputs.remove(s)
                        s.close()
    except KeyboardInterrupt:
        print("Server has been terminated.")
        
    finally:
        # Close all client sockets and the server socket
        for s in inputs:
            s.close()
        server.close()
    
if __name__ == "__main__":
    main()