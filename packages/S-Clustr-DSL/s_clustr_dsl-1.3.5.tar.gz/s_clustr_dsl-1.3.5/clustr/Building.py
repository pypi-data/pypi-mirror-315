#!/usr/bin/python3
# @Мартин.
import socket
import selectors
import time
import threading
import logging
import argparse
from colorama import Fore, Style, init

logo = f'''
███████╗███████╗██████╗       ███████╗ ██████╗ ██████╗ ██████╗ 
██╔════╝██╔════╝██╔══██╗      ██╔════╝██╔═══██╗██╔══██╗██╔══██╗
█████╗  ███████╗██████╔╝█████╗█████╗  ██║   ██║██████╔╝██║  ██║
██╔══╝  ╚════██║██╔═══╝ ╚════╝██╔══╝  ██║   ██║██╔══██╗██║  ██║
███████╗███████║██║           ██║     ╚██████╔╝██║  ██║██████╔╝
╚══════╝╚══════╝╚═╝           ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                Github==>https://github.com/MartinxMax
                @Мартин. S-Clustr(ESP FORWARD)
                                                               '''                                             

# Initialize colorama
init(autoreset=True)

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

NUM_CLIENTS = 6
DEFAULT_B_SERVER_PORT = 10001

# Store B region client connections and corresponding BID
b_clients = {}
selector = selectors.DefaultSelector()
b_lock = threading.Lock()  # Used to protect access to b_clients

# Store A region client connections
a_clients = {}

def a_client(aid):
    """A region client"""
    time.sleep(aid - 1)  # Ensure sequential connection
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((A_SERVER_IP, A_SERVER_PORT))
            logger.info(f"{Fore.CYAN}AID={aid}: Connected to {A_SERVER_IP}:{A_SERVER_PORT}{Style.RESET_ALL}")

            # Send specified string
            client.sendall(b'{"TYPE":"ESP8266"}\n')

            # Save AID's connection
            a_clients[aid] = client

            while True:
                # Receive data from AID and forward to BID
                data = client.recv(1024)
                if not data:
                    logger.info(f"{Fore.YELLOW}AID={aid}: Connection closed.{Style.RESET_ALL}")
                    break
                logger.info(f"{Fore.CYAN}AID={aid}: Sending data to BID - {data.decode('utf-8')}{Style.RESET_ALL}")
                forward_to_b_clients(aid, data)
    except Exception as e:
        logger.error(f"{Fore.RED}AID={aid}: Connection failed - {e}{Style.RESET_ALL}")
    finally:
        # Remove AID's connection
        if aid in a_clients:
            del a_clients[aid]

def b_server(b_port):
    """B region server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('', b_port))
        server.listen()
        logger.info(f"{Fore.GREEN}B Server listening on port {b_port}...{Style.RESET_ALL}")
        server.setblocking(False)
        selector.register(server, selectors.EVENT_READ, accept_b_client)

        while True:
            events = selector.select()
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)

def accept_b_client(server):
    """Accept B region client connection"""
    conn, addr = server.accept()
    logger.info(f"{Fore.BLUE}Accepted connection from {addr}{Style.RESET_ALL}")
    conn.setblocking(False)
    with b_lock:
        bid = len(b_clients) + 1
        b_clients[bid] = conn
        selector.register(conn, selectors.EVENT_READ, handle_b_client)

def handle_b_client(conn):
    """Handle B region client data reception and forwarding"""
    try:
        data = conn.recv(1024)
        if not data:
            raise ConnectionError("Connection closed")
        logger.info(f"{Fore.MAGENTA}BID={get_bid(conn)}: Received - {data.decode('utf-8')}{Style.RESET_ALL}")
        # Forward data to corresponding AID
        forward_to_a_clients(data)
    except Exception as e:
        logger.error(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        remove_b_client(conn)

def forward_to_a_clients(data):
    """Forward data to corresponding AID clients"""
    for aid, client_socket in a_clients.items():
        try:
            client_socket.sendall(data)
            logger.info(f"{Fore.CYAN}Forwarding data to AID={aid}: {data.decode('utf-8')}{Style.RESET_ALL}")
        except Exception as e:
            logger.error(f"{Fore.RED}Failed to forward data to AID={aid}: {e}{Style.RESET_ALL}")

def forward_to_b_clients(aid, data):
    """Forward AID's data to corresponding BID client"""
    message = data.decode('utf-8')
    
    if "HP" in message:
        logger.info(f"{Fore.YELLOW}AID={aid}: Data contains 'HP', not forwarding.{Style.RESET_ALL}")
        return  # Do not forward if it contains "HP"

    # Only forward to BID corresponding to AID
    if aid in b_clients:  # Ensure BID exists
        bid = aid  # Assuming AID=1 forwards to BID=1, and so on
        conn = b_clients.get(bid)
        if conn:
            try:
                conn.sendall(data)
                logger.info(f"{Fore.MAGENTA}Forwarding data from AID={aid} to BID={bid}: {message}{Style.RESET_ALL}")
            except Exception as e:
                logger.error(f"{Fore.RED}Failed to forward data from AID={aid} to BID={bid}: {e}{Style.RESET_ALL}")
        else:
            logger.warning(f"{Fore.YELLOW}No connection found for BID={bid}{Style.RESET_ALL}")

def remove_b_client(conn):
    """Remove B region client"""
    with b_lock:
        for bid, client_conn in list(b_clients.items()):
            if client_conn is conn:
                del b_clients[bid]
                logger.info(f"{Fore.RED}BID={bid} disconnected{Style.RESET_ALL}")
                break

def get_bid(conn):
    """Get corresponding BID"""
    with b_lock:
        for bid, client_conn in b_clients.items():
            if client_conn is conn:
                return bid
    return None

def main():
    print(logo)
    parser = argparse.ArgumentParser(description="B region server")
    parser.add_argument('-lp', '--listen-port', type=int, default=DEFAULT_B_SERVER_PORT, help='Server listening port (default: 10001)')
    parser.add_argument('-rhost', '--remote-host', type=str, required=True, help='S-Clustr TCP server address')
    parser.add_argument('-rport', '--remote-port', default=10000, type=int, required=True, help='S-Clustr TCP server port')
    args = parser.parse_args()

    global A_SERVER_IP, A_SERVER_PORT
    A_SERVER_IP = args.remote_host
    A_SERVER_PORT = args.remote_port

    threading.Thread(target=b_server, args=(args.listen_port,), daemon=True).start()

    for i in range(1, NUM_CLIENTS + 1):
        threading.Thread(target=a_client, args=(i,), daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
