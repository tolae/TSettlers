import argparse
import socket
from time import sleep

from messages import MessageFactory


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


def qlearned_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((args.host, args.port))
        print("Bound and listening...")
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            sleep(3)
            while True:
                length = int.from_bytes(conn.recv(2), byteorder='big', signed=False)
                message = MessageFactory.build({'length': length,
                                         'type': int.from_bytes(conn.recv(1), byteorder='big', signed=False),
                                         'data': conn.recv(length)
                                         })
                print("Received: " + message.__str__())


if __name__ == '__main__':
    args = parse_cli()
    if 'echo' in args.mode:
        echo_server()
    else:
        qlearned_server()
