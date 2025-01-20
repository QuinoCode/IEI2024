# Lanzado del proyecto
## Introducción
Dado que el proyecto contiene un número considerable de APIs su lanzado individual se hace molesto por lo que se ha decidido crear un archivo que las encapsule todas y sean lanzadas por él, este archivo se llama **wrapper.py**
## Ejecución
El archivo se ejecuta en terminal desde la carpeta raíz mediante el comando
- *python .\wrapper.py*
En caso de que un API caiga, el programa comprueba si un API ha cerrado cada 5 segundos e intenta reiniciarlo.
Todas las API's han sido hosteadas en localhost, las más importantes son la de búsqueda y la de carga que están en los puertos 5007 y 5008(esto se puede ver en la documentación de las distintas APIs que se especifica su ubicación más adelante)

# Ubicación de los distintos servicios
Teniendo en cuenta siempre paths relativos desde la raiz del proyecto.
Los APIs usados en la ejecución son: 
## API busqueda
**init_busqueda** y **busqueda_controller**, ubicados en *APIs\\busqueda\\*, y documentados en la carpeta *documentacion* bajo **initBusqueda_documentacion.md** y **busquedaController_documentacion.md** 

## API carga
**interfaz_carga** y **carga_controller**, ubicados en *APIs\\carga\\*, y documentados en la carpeta *documentacion* bajo **interfazCarga_documentacion.md** y **cargaController_documentacion.md**

## API CLE(xml)
**wrapperCLE**, ubicado en *APIs\\wrapperCLE*, y documentado en la carpeta *documentacion* bajo **wrapperCLE_documentacion.md**

## API CV(csv)
**wrapperCV**, ubicado en *APIs\\wrapperCV*, y documentado en la carpeta *documentacion* bajo **wrapperCV_documentacion.md**

## API EUS(json)
**wrapperEUS**, ubicado en *APIs\\wrapperEUS*, y documentado en la carpeta *documentacion* bajo **wrapperEUS_documentacion.md**