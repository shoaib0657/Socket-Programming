import socket
import sys

def main():
    
    # Check command line arguments
    n = len(sys.argv)
    if n != 3:
        print("Usage: python3 client.py <SERVER_IP> <SERVER_PORT>")
        sys.exit()
        
    SERVER_IP = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
    
    try:
        # Create a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Client times out if server does not respond within 2 seconds
        client_socket.settimeout(2)
        
        # Connect the socket to the port where the server is listening
        server_address = (SERVER_IP, SERVER_PORT)
        client_socket.connect(server_address)
        print("Connected to server at {}:{}".format(SERVER_IP, SERVER_PORT))
        
        while True:
            # Get user input for expression
            expression = input("Enter an expression: ")
            if not expression:
                break
            # Send data to the server
            client_socket.send(expression.encode())
            
            # Receive the result from the server
            result = client_socket.recv(1024).decode()
            if not result:
                break
            
            #Display the result
            print("Result: ", result)
    
    except KeyboardInterrupt:
        print("\nClient terminated.")
    
    except Exception as e:
        print("Error:", e)
        
    finally:
        # Close the connection
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()