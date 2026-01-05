import psutil
import os
import time
import threading
import shutil
import ctypes
from datetime import datetime


# ==========================
# LOG
# ==========================
def log(message):
    with open("agent_log.txt", "a", encoding="utf-8") as file:
        file.write(f"[{datetime.now()}] {message}\n")


# ==========================
# BANNER
# ==========================
def show_banner():
    os.system("cls" if os.name == "nt" else "clear")

    banner = r"""
   █████╗  ██████╗ ███████╗ ████████╗
  ██╔══██╗██╔════╝ ██╔════╝ ╚══██╔══╝
  ███████║██║  ███╗█████╗      ██║   
  ██╔══██║██║   ██║██╔══╝      ██║   
  ██║  ██║╚██████╔╝███████╗    ██║   
  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═╝   
     Windows Optimization Agent
    """

    print(banner)
    print("   By: Kevin Gómez")
    print("   Año: 2026\n")
    print("======================================\n")


# ==========================
# MONITOR
# ==========================
stop_monitor = False


def background_monitor():
    while not stop_monitor:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent

        if cpu > 85 or ram > 90:
            log(f"ALERTA — CPU {cpu}% RAM {ram}%")

            print("\n\nHe notado que tu PC está un poco lenta...")
            print(f"   CPU: {cpu}%   RAM: {ram}%")

            choice = input("\n¿Quieres que intente optimizarla? (s/n): ")

            if choice.lower() == "s":
                optimize_system()

        time.sleep(3)


# ==========================
# LIMPIAR TEMPORALES
# ==========================
def clean_temp():
    temp_paths = [
        os.getenv("TEMP"),
        os.getenv("TMP"),
        "C:\\Windows\\Temp"
    ]

    deleted = 0

    for path in temp_paths:
        if path and os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                        deleted += 1
                    except:
                        pass

    log(f"Archivos temporales eliminados: {deleted}")
    print(f"Archivos temporales eliminados: {deleted}")


# ==========================
# VACIAR PAPELERA
# ==========================
def empty_recycle_bin():
    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
        log("♻ Papelera vaciada")
        print("♻ Papelera vaciada")
    except:
        print("⚠ No se pudo vaciar la papelera (permiso denegado)")


# ==========================
# MOSTRAR PROCESOS PESADOS
# ==========================
def close_heavy_processes():
    print("\nBuscando procesos pesados...\n")

    heavy = []

    for p in psutil.process_iter(['name', 'cpu_percent']):
        try:
            if p.info['cpu_percent'] > 20:
                heavy.append(p)
        except:
            pass

    if not heavy:
        print("No hay procesos pesados.")
        return

    for p in heavy:
        print(f"⚠ {p.info['name']} — {p.info['cpu_percent']}% CPU")

    choice = input("\n¿Deseas cerrar estos procesos? (s/n): ")

    if choice.lower() == "s":
        for p in heavy:
            try:
                p.terminate()
            except:
                pass

        log("Procesos pesados cerrados")
        print("\nProcesos cerrados")


# ==========================
# OPTIMIZACIÓN REAL
# ==========================
def optimize_system():
    print("\nIniciando optimización segura...\n")
    log("Optimización iniciada por el usuario")

    clean_temp()
    empty_recycle_bin()
    close_heavy_processes()

    print("\nOptimización completada")
    input("\nPresiona ENTER para volver...")


# ==========================
# ESCANEO
# ==========================
def scan_system():
    os.system("cls" if os.name == "nt" else "clear")
    print("\n[!] Escaneando el sistema...\n")

    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    log(f"CPU: {cpu_usage}%  RAM: {ram.percent}%  DISK: {disk.percent}%")

    print(f"Uso CPU: {cpu_usage}%")
    print(f"RAM usada: {ram.percent}%")
    print(f"Uso del disco: {disk.percent}%")

    input("\nPresiona ENTER para volver...")


# ==========================
# LOGS
# ==========================
def show_logs():
    os.system("cls" if os.name == "nt" else "clear")

    try:
        with open("agent_log.txt", "r", encoding="utf-8") as file:
            print(file.read())
    except:
        print("No hay logs aún.")

    input("\nENTER para volver...")


# ==========================
# MENU
# ==========================
def main_menu():
    global stop_monitor
    monitor = threading.Thread(target=background_monitor, daemon=True)
    monitor.start()

    while True:
        show_banner()

        print("[1] Escanear rendimiento del sistema")
        print("[2] Optimizar sistema (real)")
        print("[3] Ver logs")
        print("[4] Salir\n")

        choice = input("Selecciona una opción: ")

        if choice == "1":
            scan_system()
        elif choice == "2":
            optimize_system()
        elif choice == "3":
            show_logs()
        elif choice == "4":
            stop_monitor = True
            break


# ==========================
# START
# ==========================
if __name__ == "__main__":
    main_menu()
    print("\n¡Hasta luego! Gracias por usar el Agente de Optimización.")