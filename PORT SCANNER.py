import socket

def scan_port(ip_address, port):
   
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt (in seconds)
        sock.settimeout(1)
        # Attempt to connect to the target IP and port
        result = sock.connect_ex((ip_address, port))
        # If connect_ex returns 0, the connection was successful (port is open)
        if result == 0:
            return True
        else:
            return False
    except socket.gaierror:
        print(f"Error: Could not resolve hostname '{ip_address}'")
        return False
    except socket.error as e:
        print(f"Error connecting to {ip_address}:{port} - {e}")
        return False
    finally:
        # Close the socket in either case
        if 'sock' in locals():
            sock.close()

def basic_port_scanner(ip_address, port_list):

  \    print(f"Scanning ports on {ip_address}...")
    for port in port_list:
        if scan_port(ip_address, port):
            print(f"Port {port}: Open")
        else:
            print(f"Port {port}: Closed")
    print("Scan complete.")

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    ports_to_scan_str = input("Enter the ports to scan (comma-separated, e.g., 80,443,22): ")
    try:
        ports_to_scan = [int(port.strip()) for port in ports_to_scan_str.split(',')]
        basic_port_scanner(target_ip, ports_to_scan)
    except ValueError:
        print("Invalid port number entered.")
    except Exception as e:
        print(f"An error occurred: {e}")
