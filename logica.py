import os

archivos = []
tamañoArchivos = []
carpetas = []
tamañoCarpetas = []


def obtenerTamaño(rutaArchivo):
    """Esta es una funcion que va a recibir una ruta de un archivo y va a devolver el tamaño del archivo
       en la unidad de medida mas adecuada
    """
    tamaño = float(os.path.getsize(rutaArchivo))
    if tamaño < 1024:
        return f"{tamaño:.2f} B"
    elif tamaño < 1024**2:
        tamaño /= 1024
        return f"{tamaño:.2f} KB"
    elif tamaño < 1024**3:
        tamaño /= 1024**2
        return f"{tamaño:.2f} MB"
    elif tamaño < 1024**4:
        tamaño /= 1024**3
        return f"{tamaño:.2f} GB"
    else:
        tamaño /= 1024**4
        return f"{tamaño:.2f} TB"
    

def informacionCarpeta(ruta):
    if type(ruta) != str:
        raise Exception("La ruta debe ser un string")
    if not os.path.exists(ruta):
        raise Exception("Debe ingresar una ruta que exista")
    if not os.path.isdir(ruta):
        raise Exception("Debe ingresar una ruta de una carpeta")
    return  informacionCarpetaAux(ruta)

def informacionCarpetaAux(ruta):
    global archivos, tamañoArchivos, carpetas, tamañoCarpetas
    nombre = os.path.basename(ruta)
    tamaño = os.path.getsize(ruta)
    hijos = []
    if os.path.isfile(ruta):
        archivos.append(ruta)
        tamañoArchivos.append(tamaño)
        return {"Nombre":nombre, "Tamaño": tamaño, "Ruta": ruta, "Hijos":hijos}
    elementos = os.listdir(ruta)
    carpetas.append(ruta)
    tamañoCarpetas.append(len(elementos))
    for elemento in elementos:
        rutaElemento = os.path.join(ruta, elemento)
        infoElemento = informacionCarpetaAux(rutaElemento)
        hijos.append(infoElemento)
    return {"Nombre":nombre, "Tamaño": tamaño, "Ruta": ruta, "Hijos":hijos}

def topTamañoArchivos(archivos):
    listaArchivos = []
    tamañoArchivosOrdenado = archivos.copy()
    contador = 0
    while contador < 10 and tamañoArchivosOrdenado != []:
        listaArchivos.append(tamañoArchivosOrdenado.pop(tamañoArchivosOrdenado.index(max(tamañoArchivosOrdenado))))
        contador += 1
    return listaArchivos

def topTamañoCarpetas(carpetas):
    listaCarpetas = []
    tamañoCarpetasOrdenado = carpetas.copy()
    contador = 0
    while contador < 10 and tamañoCarpetasOrdenado != []:
        listaCarpetas.append(tamañoCarpetasOrdenado.pop(tamañoCarpetasOrdenado.index(max(tamañoCarpetasOrdenado))))
        contador += 1
    return listaCarpetas

def topArchivos(listaArchivos):
    archivosFinal = {}
    for elemento in listaArchivos:
        archivosFinal[archivos[tamañoArchivos.index(elemento)]] = obtenerTamaño(archivos[tamañoArchivos.index(elemento)])
    return archivosFinal

def topCarpetas(listaCarpetas):
    carpetasFinal = {}
    for elemento in listaCarpetas:
        carpetasFinal[carpetas[tamañoCarpetas.index(elemento)]] = elemento
    return carpetasFinal