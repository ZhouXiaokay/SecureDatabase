import socket
import multiprocessing
from multiprocessing import Pool

def single_process_scan_ports(host, num_ports):
    """
    :param host: IP.
    :return: opened TCP ports.
    """
    opened_ports = []
    for port in range(num_ports):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            status = s.connect_ex((host, port))
            if status == 0:
                opened_ports.append(port)
            s.close()
        except Exception as e:
            pass
    if len(opened_ports) != 0:
        print(opened_ports)
    else:
        print("All ports are closed.")

    return opened_ports

def multi_process_scan_ports(host, ports):
    for port in range(ports, ports + 4096):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        status = s.connect_ex((host, port))
        if status == 0:
            print(f"{multiprocessing.current_process().pid}: {port} can be connected by TCP.")
        s.close()


def run_multi_process_scan_ports(host, max_process):
    """
    :param host: IP
    :param max_process: Process pool configuration
    :return: None
    """
    process_pool = Pool(max_process)
    for index in range(max_process):
        process_pool.apply_async(multi_process_scan_ports, args=(host, index*4096))
    process_pool.close()
    process_pool.join()

    print("All process finished.")

#Debug
if __name__ == '__main__':
    # run_multi_process_scan_ports('localhost', 10)
    single_process_scan_ports('localhost', 40960)