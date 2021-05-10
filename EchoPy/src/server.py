import argparse
import socket
from time import sleep

from servers.qlearning import QServer


def print_help():
    print("Help")


def parse_cli():
    parser = argparse.ArgumentParser(description="Launch TSettlers Python Brain")
    parser.add_argument('host', type=str,
                        help="IP Address to start the server on.")
    parser.add_argument('port', type=int,
                        help="Port to listen to.")
    parser.add_argument('--mode', '-m', dest='mode',
                        choices=['echo'],
                        default=[],
                        help="Run non-default server")

    return parser.parse_args()


def echo_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((args.host, args.port))
        print("Bound and listening...")
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            sleep(3)
            while True:
                print("Sending data...")
                conn.sendall("Ping!".encode('utf-8'))
                sleep(1)
                data = conn.recv(5)
                print("Received: ", end='')
                print(data.decode('utf-8'))
                sleep(1)


if __name__ == '__main__':
    args = parse_cli()
    if 'echo' in args.mode:
        echo_server()
    else:
        qserver = QServer(args.host, args.port)
        qserver.run()
