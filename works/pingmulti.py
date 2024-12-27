from dataclasses import dataclass
from datetime import datetime
from queue import Queue
import subprocess
from threading import Thread
import time
import argparse
import sys

@dataclass
class PingResult:
    """A class to store a ping test result."""
    ip: str
    is_up: bool
    rtt_ms: float = None

def ping_thread(addrs_q: Queue, results_q: Queue) -> None:
    """Thread code to process (i.e. ping) addresses in addrs_q queue, append result to results_q queue."""
    while True:
        ip = addrs_q.get()
        try:
            args = ['ping', '-c', '1', '-W', '1', str(ip)]
            p_ping = subprocess.run(args, capture_output=True, text=True)
            if p_ping.returncode == 0:
                search = re.search(r'time=(\d+.\d+)', p_ping.stdout)
                if search:
                    ping_rtt = float(search.group(1))
                    results_q.put(PingResult(ip=ip, is_up=True, rtt_ms=ping_rtt))
                else:
                    results_q.put(PingResult(ip=ip, is_up=False))
            else:
                results_q.put(PingResult(ip=ip, is_up=False))
        except Exception as e:
            print(f"Error pinging {ip}: {e}", file=sys.stderr)
        finally:
            addrs_q.task_done()

def main(num_threads: int, subnet: str):
    addrs_q: Queue[str] = Queue()
    results_q: Queue[PingResult] = Queue()

    for _ in range(num_threads):
        Thread(target=ping_thread, args=(addrs_q, results_q), daemon=True).start()

    while True:
        for lsb in range(1, 255):
            addrs_q.put(f'{subnet}.{lsb}')
        
        addrs_q.join()

        print(f'some IPs up at {datetime.now().isoformat()}:')
        while not results_q.empty():
            ping_result = results_q.get_nowait()
            if ping_result.is_up:
                print(ping_result)
        
        time.sleep(60.0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ping multiple IPs in a subnet using multiple threads.")
    parser.add_argument('--threads', type=int, default=50, help='Number of threads to use')
    parser.add_argument('--subnet', type=str, default='192.168.1', help='The subnet to ping')
    args = parser.parse_args()

    main(args.threads, args.subnet)