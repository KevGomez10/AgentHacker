import psutil
import os
import time
import threading
import shutil
import ctypes
import subprocess
import json
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


# ==========================
# JSON LOG PRO
# ==========================
def log_json(event, data=None):
    entry = {
        "timestamp": str(datetime.now()),
        "event": event,
        "data": data
    }

    with open("agent_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ==========================
# ADMIN CHECK
# ==========================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# ==========================
# STEALTH MODE (optional)
# ==========================
def enable_stealth():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass


# ==========================
# ANIMACION
# ==========================
def slow_print(text, delay=0.02):
    for c in text:
        print(Fore.GREEN + c, end="", flush=True)
        time.sleep(delay)
    print()


# ==========================
# BANNER MATRIX
# ==========================
def show_banner():
    os.system("cls" if os.name == "nt" else "clear")

    banner = r"""
██████╗  ██████╗  ██████╗ ███████╗████████╗██╗  ██╗
██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝╚██╗██╔╝
██████╔╝██║   ██║██║   ██║███████╗   ██║    ╚███╔╝ 
██╔══██╗██║   ██║██║   ██║╚════██║   ██║    ██╔██╗ 
██████╔╝╚██████╔╝╚██████╔╝███████║   ██║   ██╔╝ ██╗
╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
     SISTMA DE OPTIMIZACIÓN AUTOMÁTICA
    """

    print(Fore.GREEN + banner)
    print(Fore.GREEN + "      By Kevin Gomez")
    print(Fore.GREEN + "      Año: 2026")
    print(Fore.GREEN + "=====================================\n")


# ==========================
# MONITOR AUTOMÁTICO
# ==========================
stop_monitor = False

def background_monitor():
    while not stop_monitor:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent

        if cpu > 85 or ram > 90:
            log_json("alert", {"cpu": cpu, "ram": ram})
            print(Fore.GREEN + "\n⚠ Rendimiento alto detectado")
            print(Fore.GREEN + f"CPU: {cpu}%  RAM: {ram}%")

            c = input(Fore.GREEN + "\n¿Optimizar ahora? (s/n): ")
            if c.lower() == "s":
                optimize_system()

        time.sleep(4)


# ==========================
# LIMPIEZAS
# ==========================
def clean_temp():
    deleted = 0
    for path in [os.getenv("TEMP"), os.getenv("TMP"), "C:\\Windows\\Temp"]:
        if path and os.path.exists(path):
            for root, _, files in os.walk(path):
                for f in files:
                    try:
                        os.remove(os.path.join(root, f))
                        deleted += 1
                    except:
                        pass

    slow_print(f"Eliminados {deleted} temporales")
    log_json("temp_clean", {"deleted": deleted})


def empty_recycle():
    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
        slow_print("♻ Papelera vaciada")
        log_json("recycle_bin", "emptied")
    except:
        pass


# ==========================
# PROCESOS PESADOS
# ==========================
def close_heavy():
    slow_print("\nBuscando procesos pesados...\n")

    heavy = []
    for p in psutil.process_iter(['name', 'cpu_percent']):
        try:
            if p.info['cpu_percent'] > 25:
                heavy.append(p)
        except:
            pass

    if not heavy:
        slow_print("Nada grave")
        return

    for p in heavy:
        print(Fore.GREEN + f"{p.info['name']} — {p.info['cpu_percent']}% CPU")

    c = input(Fore.GREEN + "\nCerrar? (s/n): ")
    if c.lower() == "s":
        for p in heavy:
            try:
                p.terminate()
            except:
                pass
        slow_print("✔ Procesos cerrados")
        log_json("heavy_processes_closed")


# ==========================
# OPTIMIZACIÓN TOTAL
# ==========================
def optimize_system():
    slow_print("\nOPTIMIZACIÓN EN CURSO\n", 0.01)

    log_json("optimize_start")

    clean_temp()
    empty_recycle()
    close_heavy()

    slow_print("\nOptimización completada")

    if is_admin():
        c = input(Fore.GREEN + "\n¿Reiniciar ahora? (s/n): ")
        if c.lower() == "s":
            os.system("shutdown /r /t 5")
    else:
        slow_print("\n⚠ Ejecuta como administrador para reinicio automático")


# ==========================
# SCAN
# ==========================
def scan():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    slow_print(f"\nCPU: {cpu}%")
    slow_print(f"RAM: {ram}%")
    slow_print(f"DISCO: {disk}%")

    log_json("scan", {"cpu": cpu, "ram": ram, "disk": disk})


# ==========================
# MENU
# ==========================
def main():
    global stop_monitor

    if "--stealth" in os.sys.argv:
        enable_stealth()

    monitor = threading.Thread(target=background_monitor, daemon=True)
    monitor.start()

    while True:
        show_banner()

        print(Fore.GREEN + "[1] Escanear sistema")
        print(Fore.GREEN + "[2] Optimización total")
        print(Fore.GREEN + "[3] Salir\n")

        c = input(Fore.GREEN + "Selecciona: ")

        if c == "1":
            scan()
            input("\nENTER...")
        elif c == "2":
            optimize_system()
        elif c == "3":
            stop_monitor = True
            break


if __name__ == "__main__":
    main()
