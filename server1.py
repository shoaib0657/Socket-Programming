# Part1: Server handling single connection at a time
# First, you will write a simple server in a file called "server1.py". The server1 program should
# take the ip address and port number from the command line, and start a listening socket on that
# command line. Whenever a client request arrives on that socket, the server should accept the
# connection, read the client's request, and return the result. After replying to one message, the
# server should then wait to read the next message from the client, as long as the client wishes to
# chat. Once the client is terminated (socket read fails), the server should go back to waiting for
# another client. The server should terminate on Ctrl+C.
# Your simple server1 should NOT handle multiple clients concurrently (only one after the other).
# That is, when server1 is engaged with a client, another client that tries to chat with the same
# server must see an error message. However, the second client should succeed if the first client
# has terminated.

import socket
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
        print("Usage: python server1.py <SERVER_IP> <SERVER_PORT>")
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
        server.listen(1)                  # Allow up to 1 connections before refusing new ones

        print('Server is listening for incoming connections...')

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()
    
    # Main loop of the server
    try:
        while True:
            # Wait for a connection
            connection, client_address = server.accept()

            print(f'Connection from {client_address} has been established.')

            # Serve the client - Calculator Server
            try:
                while True:
                    # Receive the data from the client
                    data = connection.recv(1024)
                    if not data:  # Blank data means the client has terminated
                        print(f"Connection from {client_address} has been closed.")
                        break
                    
                    print(f"Received from client: {data.decode('utf-8')}")
                    
                    expression = data.decode('utf-8')
                    result = evaluate_expression(expression)
                    connection.sendall(result.encode('utf-8'))
                    print(f"Sent to client: {result}")
            except Exception as e:
                print(f"An error occurred while serving the client: {e}")
            except KeyboardInterrupt:
                print("Server has been terminated.")
                connection.close()
                server.close()
                sys.exit()
            finally:
                # Close the connection and wait for another connection
                connection.close()             
                
    except KeyboardInterrupt:
        print("Server has been terminated.")

    finally:
        # Close the server socket
        server.close()

if __name__ == "__main__":
    main()