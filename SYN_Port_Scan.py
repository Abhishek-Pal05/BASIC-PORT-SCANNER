import socket
import struct
from scapy.all import IP, TCP, send

def is_root():
    """Checks if the script is run with root/administrator privileges."""
    import os
    return os.geteuid() == 0

def scan_port(ip_address, port):
    """
    Attempts to connect to the specified IP address and port.
    Returns True if the port is open, False otherwise.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip_address, port))
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
        if 'sock' in locals():
            sock.close()

def syn_scan_port(target_ip, port):
    """
    Performs a SYN scan on the specified port.
    Returns True if SYN-ACK is received (port is likely open), False otherwise, or None for permission issues.
    Requires root/administrator privileges.
    """
    try:
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    except PermissionError:
        print("Error: Raw socket creation requires root/administrator privileges.")
        return None

    try:
        src_port = 54321
        ip_header = struct.pack('!BBHHHBBH4s4s',
                                0x45, 0, 40, 0, 0, 0, 0, 0,
                                socket.inet_aton('127.0.0.1'),
                                socket.inet_aton(target_ip))

        tcp_header = struct.pack('!HHLLBBHHH',
                                 src_port, port, 0, 0, 0x02, 0, 0, 0, 0)

        # Placeholder checksum (implement proper calculation)
        checksum = 0
        packet = ip_header + tcp_header
        for i in range(0, len(packet), 2):
            word = (packet[i] << 8) + (packet[i+1] if i+1 < len(packet) else 0)
            checksum += word
            checksum &= 0xffff
        tcp_header = tcp_header[:16] + struct.pack('!H', socket.htons(~checksum & 0xffff)) + tcp_header[18:]

        packet = ip_header + tcp_header
        raw_socket.sendto(packet, (target_ip, port))
        raw_socket.settimeout(0.5)

        while True:
            try:
                recv_packet, addr = raw_socket.recvfrom(65535)
                ip_header_len = (recv_packet[0] & 0x0F) * 4
                tcp_header_len = (recv_packet[ip_header_len + 12] >> 4) * 4
                tcp_flags = recv_packet[ip_header_len + 13]

                if addr[0] == target_ip and recv_packet[ip_header_len + 2:ip_header_len + 4] == struct.pack('!H', src_port):
                    if tcp_flags & 0x12:
                        return True
                    elif tcp_flags & 0x04:
                        return False
            except socket.timeout:
                return False

    except socket.error as e:
        print(f"Socket error during SYN scan: {e}")
        return False
    finally:
        if 'raw_socket' in locals():
            raw_socket.close()

def basic_port_scanner(target_ip, port_list, use_syn_scan=False):
    """
    Scans a list of ports on a given IP address using either connect or SYN scan.
    Prints whether each port is open or closed.
    """
    print(f"Scanning ports on {target_ip} using {'SYN' if use_syn_scan else 'connect'} scan...")
    for port in port_list:
        if use_syn_scan:
            if is_root():
                result = syn_scan_port(target_ip, port)
                if result is True:
                    print(f"Port {port}: Open (SYN-ACK)")
                elif result is False:
                    print(f"Port {port}: Closed (RST)")
                elif result is None:
                    print(f"Port {port}: Scan skipped due to insufficient privileges for SYN scan.")
                    break # Stop scanning if no root privileges
            else:
                print("Error: SYN scan requires root/administrator privileges. Falling back to connect scan.")
                if scan_port(target_ip, port): # Ensure scan_port is called here
                    print(f"Port {port}: Open")
                else:
                    print(f"Port {port}: Closed")
        else:
            if scan_port(target_ip, port):
                print(f"Port {port}: Open")
            else:
                print(f"Port {port}: Closed")
    print("Scan complete.")

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    ports_to_scan_str = input("Enter the ports to scan (comma-separated, e.g., 80,443,22): ")
    use_stealth_scan = input("Use SYN stealth scan? (yes/no): ").lower() == 'yes'

    try:
        ports_to_scan = [int(port.strip()) for port in ports_to_scan_str.split(',')]
        basic_port_scanner(target_ip, ports_to_scan, use_syn_scan=use_stealth_scan)
    except ValueError:
        print("Invalid port number entered.")
    except Exception as e:
        print(f"An error occurred: {e}")
