from logger import log_info
from prometheus_client import start_http_server
from config import PROMETHEUS_PORT
import asyncio
from trading import main as trading_main
from scheduler import start_scheduler
import threading

def start_scheduler_thread():
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    log_info("Scheduler started in a separate thread.")

def main():
    log_info("Starting trading bot...")
    start_http_server(PROMETHEUS_PORT)
    log_info(f"Prometheus metrics available at http://localhost:{PROMETHEUS_PORT}")

    # Start scheduler in a separate thread
    start_scheduler_thread()

    # Start trading logic
    asyncio.run(trading_main())

if __name__ == "__main__":
    main()


