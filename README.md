# BASIC-PORT-SCANNER
This is a basic port scanner that scans open TCP ports using the systems IP address.

Purpose-
This code is intended to scan for any vulnerable open ports on systems for which i have permissions. the intent is just for educational purposes and basic network exploration.

Features-
1. Scanning the specified IP address.
2. Scanning TCP ports.
3. Generating output.
4. If the ports are closed it will generates "closed : Port".
5. Users can scan for multiple ports at a time.

Terminology
1. Socket- this is a python module that provides a low level interface to the network socket APIs (Application programming interfaces) that are a part of most modern operating systems.These APIs allow you to create and manipulate networks connections.
2. Scan Port- The scan_port function in the Python code I provided is designed to perform a single attempt to connect to a specific port on a given IP address.
3. Port-In the context of computer networking, specifically within the TCP/IP (Transmission Control Protocol/Internet Protocol) model, a port serves as a logical communication endpoint.
4. TCP-The Transmission Control Protocol (TCP) is one of the core protocols of the Internet Protocol suite (TCP/IP). It operates at the transport layer and provides reliable, ordered, and error-checked delivery of a stream of bytes between applications running on hosts communicating 1  over an IP network.
5. IP Address-An IP address (Internet Protocol address) is a numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication.

Limitations
1. Performs basic, easily detectable TCP connect scans.
2. Scans ports sequentially, making it inefficient for large ranges.
3. Has limited error handling beyond basic connection failures and hostname resolution.
4. Doesn't perform service detection beyond identifying open ports.
5. Lacks operating system detection capabilities.
6. Features rudimentary input handling without extensive validation.
7. Doesn't implement rate limiting or intrusion detection evasion.
8. Relies on the underlying network connectivity of the executing machine.
9. Basic TCP connect scan usually doesn't need special privileges, but more advanced scans would.
10. Provides only console output without reporting or logging functionality.
11. Uses a fixed timeout value that might not be optimal in all situations.
12. Currently only supports IPv4 addresses, not IPv6.

Ethical Considerations
This script is intended for educational purposes and for scanning systems that you have explicit permission to test. Scanning networks or systems without authorization is illegal and unethical. The author is not responsible for any misuse of this tool.

Addition-
# BASIC STEALTH SCAN (SYN Scan - Requires Root/Admin Privileges) 
A stealth scan is a type of port scanning technique designed to be less detectable by the target system's security measures, such as firewalls and intrusion detection systems (IDS). Unlike a standard TCP connect scan, which completes the full three-way handshake to establish a connection, stealth scans often employ methods to avoid this, thus reducing the chances of being logged.

Features-
1. TCP Connect Scan:** The default scanning method, attempting a full TCP connection to each specified port.
2. SYN Stealth Scan:** Sends SYN packets and analyzes responses (SYN-ACK for open, RST for closed) without completing the TCP handshake. This method is generally less detectable but requires elevated privileges.
3. User-Friendly Input:** Prompts the user for the target IP address and a comma-separated list of ports to scan.
4. Clear Output:** Displays the status (Open or Closed) for each scanned port, indicating the scan method used.
5. Privilege Detection:** Checks if the script is run with root/administrator privileges for SYN scanning.
6. Fallback Mechanism:** Automatically reverts to TCP connect scan if SYN scan is requested but privileges are insufficient.

# SYN Scan (-sS): 
This is often referred to as a "half-open" scan. The scanner sends a SYN packet and analyzes the response (SYN-ACK for open, RST for closed). It doesn't send the final ACK to complete the connection. Your basic SYN scan code implements this.   




