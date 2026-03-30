import os
import time
import json
import ctypes
import threading
import logging
from datetime import datetime
from typing import List

import psutil
from colorama import Fore, init

init(autoreset=True)

LOG_FILE = "agent_log.json"
stop_monitor = False


# ==========================
# LOGGER CONFIG
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================
# UTILIDADES
# ==========================
def green(text: str) -> None:
    """Print text in green."""
    print(Fore.GREEN + text)


def slow_print(text: str, delay: float = 0.02) -> None:
    """Print text slowly for animation."""
    for char in text:
        print(Fore.GREEN + char, end="", flush=True)
        time.sleep(delay)
    print()


# ==========================
# JSON LOGGING
# ==========================
def log_json(event: str, data=None) -> None:
    """Write structured event logs."""
    entry = {
        "timestamp": str(datetime.now()),
        "event": event,
        "data": data
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as error:
        logging.error("Failed to write log: %s", error)


# ==========================
# ADMIN CHECK
# ==========================
def is_admin() -> bool:
    """Check if program runs with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        return False


# ==========================
# SYSTEM METRICS
# ==========================
def get_system_metrics() -> dict:
    """Return CPU, RAM and Disk usage."""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    return {
        "cpu": cpu,
        "ram": ram,
        "disk": disk
    }


# ==========================
# CLEAN TEMP FILES
# ==========================
def clean_temp_files() -> int:
    """Delete temporary files."""
    temp_paths = [
        os.getenv("TEMP"),
        os.getenv("TMP"),
        "C:\\Windows\\Temp"
    ]

    deleted = 0

    for path in temp_paths:
        if not path or not os.path.exists(path):
            continue

        for root, _, files in os.walk(path):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    deleted += 1
                except OSError:
                    continue

    log_json("temp_clean", {"deleted": deleted})
    return deleted


# ==========================
# EMPTY RECYCLE BIN
# ==========================
def empty_recycle_bin() -> None:
    """Empty Windows recycle bin."""
    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
        log_json("recycle_bin", "emptied")
        green("♻ Papelera vaciada")
    except Exception as error:
        logging.warning("Recycle bin clean failed: %s", error)


# ==========================
# HEAVY PROCESS DETECTION
# ==========================
def find_heavy_processes(limit: int = 25) -> List[psutil.Process]:
    """Return processes using high CPU."""
    heavy_processes = []

    for process in psutil.process_iter(['name', 'cpu_percent']):
        try:
            if process.info['cpu_percent'] > limit:
                heavy_processes.append(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return heavy_processes


def close_processes(processes: List[psutil.Process]) -> None:
    """Terminate selected processes."""
    for process in processes:
        try:
            process.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    log_json("heavy_processes_closed", len(processes))


# ==========================
# SYSTEM OPTIMIZATION
# ==========================
def optimize_system() -> None:
    """Run full system optimization."""
    slow_print("\nOPTIMIZACIÓN EN CURSO\n", 0.01)

    log_json("optimize_start")

    deleted = clean_temp_files()
    green(f"Temporales eliminados: {deleted}")

    empty_recycle_bin()

    heavy = find_heavy_processes()

    if heavy:
        green("\nProcesos pesados detectados:")

        for process in heavy:
            green(f"{process.info['name']} — {process.info['cpu_percent']}% CPU")

        confirm = input("\nCerrar procesos? (s/n): ")

        if confirm.lower() == "s":
            close_processes(heavy)
            green("✔ Procesos cerrados")

    slow_print("\nOptimización completada")


# ==========================
# SYSTEM SCAN
# ==========================
def scan_system() -> None:
    """Display system usage."""
    metrics = get_system_metrics()

    green(f"\nCPU: {metrics['cpu']}%")
    green(f"RAM: {metrics['ram']}%")
    green(f"DISCO: {metrics['disk']}%")

    log_json("scan", metrics)


# ==========================
# BACKGROUND MONITOR
# ==========================
def monitor_system() -> None:
    """Monitor system performance."""
    global stop_monitor

    while not stop_monitor:
        metrics = get_system_metrics()

        if metrics["cpu"] > 85 or metrics["ram"] > 90:
            log_json("alert", metrics)

            green("\n⚠ Rendimiento alto detectado")
            green(f"CPU: {metrics['cpu']}% RAM: {metrics['ram']}%")

        time.sleep(5)


# ==========================
# UI
# ==========================
def show_banner() -> None:
    """Display banner."""
    os.system("cls" if os.name == "nt" else "clear")

    banner = r"""
██████╗  ██████╗  ██████╗ ███████╗████████╗██╗  ██╗
██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝╚██╗██╔╝
██████╔╝██║   ██║██║   ██║███████╗   ██║    ╚███╔╝ 
██╔══██╗██║   ██║██║   ██║╚════██║   ██║    ██╔██╗ 
██████╔╝╚██████╔╝╚██████╔╝███████║   ██║   ██╔╝ ██╗
╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
SISTEMA DE OPTIMIZACIÓN AUTOMÁTICA
"""

    green(banner)
    green("By Kevin Gomez - 2026\n")


def main_menu() -> None:
    """Display program menu."""
    global stop_monitor

    monitor = threading.Thread(target=monitor_system, daemon=True)
    monitor.start()

    while True:
        show_banner()

        green("[1] Escanear sistema")
        green("[2] Optimización total")
        green("[3] Salir\n")

        option = input("Selecciona: ")

        if option == "1":
            scan_system()
            input("\nENTER...")
        elif option == "2":
            optimize_system()
            input("\nENTER...")
        elif option == "3":
            stop_monitor = True
            break
        else:
            green("Opción inválida")


# ==========================
# ENTRY POINT
# ==========================
if __name__ == "__main__":
    main_menu()