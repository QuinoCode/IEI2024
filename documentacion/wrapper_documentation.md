Cómo lanzar a ejecución el servicio mediante wrapper.py

Wrapper.py existe para lanzar todas las APIs desde un archivo para simplificar la demostración.
El archivo se ejecuta en terminal desde la carpeta raíz mediante el comando
    python .\wrapper.py
En caso de que un API caiga, el programa comprueba si un API ha cerrado cada 5 segundos e intenta reiniciarlo.

Los APIs usados en la ejecución son: 

init_busqueda y busqueda_controller, ubicados en APIs\busqueda\, y documentados en la carpeta documentacion bajo initBusqueda_documentacion.md y busquedaController_documentacion.md 

interfaz_carga y carga_controller, ubicados en APIs\carga\, y documentados en la carpeta documentacion bajo interfazCarga_documentacion.md y cargaController_documentacion.md

wrapperCLE, ubicado en APIs\wrapperCLE, y documentado en la carpeta documentacion bajo wrapperCLE_documentacion.md

wrapperCV, ubicado en APIs\wrapperCV, y documentado en la carpeta documentacion bajo wrapperCV_documentacion.md

wrapperEUS, ubicado en APIs\wrapperEUS, y documentado en la carpeta documentacion bajo wrapperEUS_documentacion.md