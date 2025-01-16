import subprocess
import time
import os
from subprocess import call
from APIs.carga import *
from APIs.busqueda import *
from APIs.wrapperCV import *
from APIs.wrapperCLE import *
from APIs.wrapperEUS import *

root_path = os.path.abspath(os.path.dirname(__file__))

# List of scripts to run
modules = [
    # 'APIs.carga.carga_controller', Cuando esté el archivo main de transformar geocodificación
    'APIs.wrapperCV.wrapperCV_controller',
    'APIs.wrapperCLE.wrapperCLE_controller',
    'APIs.wrapperEUS.wrapperEUS_controller',
    'APIs.busqueda.busqueda_controller'
]

# Dictionary to hold process objects
processes = {}

def start_script(module):
    print(f"[+] Arrancando {module}...")
    return subprocess.Popen(['python','-m', module], stdout=None, stderr=None)

def monitor_processes():
    while True:
        for module, process in list(processes.items()):
            # Comprobar si los procesos están activos en este momento o alguno ha parado
            if process.poll() is not None:  # Proceso paró
                print(f"[!] {module} se ha detenido. Va a reiniciarse.")
                processes[module] = start_script(module)
        time.sleep(5)  # Monitor interval

if __name__ == '__main__':
    # Start all scripts
    for module in modules:
        processes[module] = start_script(module)
    try:
        monitor_processes()
    except KeyboardInterrupt:
        print("[!] Interrumpido por teclado")
        for process in processes.values():
            process.terminate()

