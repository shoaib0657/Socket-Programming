# server2.py : Your server program "server2.py " will be a multi-threaded server that will
# create a new thread for every new client request it receives. Multiple clients should be
# able to simultaneously chat with the server.

import socket
import sys
import threading

# Shared flag variable to indicate server running status
server_running = True

def evaluate_expression(expression):
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Invalid expression"
    
def handle_client(connection, client_address):
    
    global server_running
    
    print(f"Connection from {client_address} has been established.")
    try:
        while server_running:
            # Receive the data from the client
            data = connection.recv(1024)
            if not data:  # Blank data means the client has terminated
                # print(f"Connection from {client_address} has been closed.")
                break
            
            if server_running == False:
                break
            
            # Decode the received data
            expression = data.decode('utf-8')
            print(f"Received from client at {client_address}: {expression}")
            
            # Evaluate the expression
            result = evaluate_expression(expression)
            
            # Send back the evaluated expression to the client
            connection.sendall(result.encode('utf-8'))
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    except KeyboardInterrupt:
        print("Server has been terminated.")
        server_running = False
        sys.exit()
    
    finally:
        connection.close()
        print(f"Connection from {client_address} has been closed")
        
def main():
    
    global server_running
    
    # Check command line arguments
    n = len(sys.argv)

    if n != 3:
        print("Usage: python server2.py <SERVER_IP> <SERVER_PORT>")
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
        
    # Main loop of the server
    try:
        while server_running:
            # Wait for a connection
            connection, client_address = server.accept()
            
            # if(threading.active_count() > MAX_CLIENTS):
            #     connection.sendall("Server is busy. Please try again later.".encode('utf-8'))
            #     connection.close()
            #     continue
            
            # Create a new thread for the client
            client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
            client_thread.start()
            
    except KeyboardInterrupt:
        print("Server has been terminated.")
        server_running = False
        sys.exit()
    
    finally:
        server.close()
        sys.exit()
        
if __name__ == "__main__":
    main()