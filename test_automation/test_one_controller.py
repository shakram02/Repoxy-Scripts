from automation_functions import *


def main():
    ip = "192.168.1.244"
    messenger_port = 6934
    controller_port = 6834
    controller_id = 0

    client_socket = start_tcp_messenger(ip, messenger_port)
    launch_controller(controller_id, client_socket)

    network = create_network(proxy_ip=ip, proxy_port=controller_port, switch_count=3)
    start_network(network)

    ping_all(network)

    stop_network(network)

    stop_controller(controller_id, client_socket)
    stop_tcp_messenger(controller_id, client_socket)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except Exception:
        mininet_clean()
