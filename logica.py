import os

archivos = []
tamañoArchivos = []
carpetas = []
tamañoCarpetas = []

def obtenerTamaño(rutaArchivo):
    """Esta es una funcion que va a recibir una ruta de un archivo y va a devolver el tamaño del archivo
       en la unidad de medida mas adecuada
       Entradas: Una ruta de un archivo o carpeta
       Salidas: Tamaño en la unidad de medida mas adecuada
       Restricciones: rutaArchivo debe ser una ruta válida
    """
    if type(rutaArchivo) != str:
        raise Exception("La ruta debe ser un string")
    if not os.path.exists(rutaArchivo):
        raise Exception("Debe ingresar una ruta que exista")
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
    
def obtenerMedidaTamaño(tamaño):
    """
    Esta funcion recibe un tamaño en bytes y lo convierte a la unidad mas adecuada
    Entradas: Un valor numérico en bytes
    Salidas: String con el tamaño en la unidad mas adecuada
    Restricciones: tamaño debe ser un valor numérico positivo
    """
    if type(tamaño) not in (int, float):
        raise Exception("El tamaño debe ser un valor numérico")
    if tamaño < 0:
        raise Exception("El tamaño debe ser positivo")
    tamaño = float(tamaño)
    if tamaño < 1024:
        return f"{tamaño:.2f} B"
    elif tamaño < 1024**2:
        return f"{tamaño / 1024:.2f} KB"
    elif tamaño < 1024**3:
        return f"{tamaño / 1024**2:.2f} MB"
    elif tamaño < 1024**4:
        return f"{tamaño / 1024**3:.2f} GB"
    else:
        return f"{tamaño / 1024**4:.2f} TB"

def informacionCarpeta(ruta):
    """ 
    Esta es la funcion principal de una función recursiva, recibe una ruta de una carpeta y llama
    la función auxiliar
    Entradas: Una ruta de una carpeta
    Salidas: Diccionario que devuelve la función auxiliar
    Restricciones: ruta debe ser una ruta válda    
    """
    if type(ruta) != str:
        raise Exception("La ruta debe ser un string")
    if not os.path.exists(ruta):
        raise Exception("Debe ingresar una ruta que exista")
    if not os.path.isdir(ruta):
        raise Exception("Debe ingresar una ruta de una carpeta")
    return  informacionCarpetaAux(ruta)

def informacionCarpetaAux(ruta):
    """ 
    Esta es la funcion auxiliar de una función recursiva, recibe una ruta de una carpeta y devuelve
    un diccionario con la información de la carpeta
    Entradas: Una ruta de una carpeta
    Salidas: Diccionario con la información de la carpeta
    Restricciones: ruta debe ser una ruta válda (se chequea en la función principal)   
    """
    global archivos, tamañoArchivos, carpetas, tamañoCarpetas
    nombre = os.path.basename(ruta)
    tamaño = os.path.getsize(ruta)
    hijos = []
    if os.path.isfile(ruta):
        archivos.append(ruta)
        tamañoArchivos.append(tamaño)
        return {"nombre":nombre, "tamaño": tamaño, "ruta": ruta, "hijos":hijos}
    elementos = os.listdir(ruta)
    carpetas.append(ruta)
    tamañoCarpetas.append(len([arc for arc in elementos if os.path.isfile(os.path.join(ruta, arc))]))
    tamaño = 0
    for elemento in elementos:
        rutaElemento = os.path.join(ruta, elemento)
        infoElemento = informacionCarpetaAux(rutaElemento)
        hijos.append(infoElemento)
        tamaño += infoElemento["tamaño"]
    return {"nombre":nombre, "tamaño": tamaño, "ruta": ruta, "hijos":hijos}

def topTamañoArchivos(listaTamañoArchivos):
    """ 
    Esta funcion retorna una lista con los 10 elementos mas grandes de una lista
    Entradas: Una lista con valores numéricos
    Salidas: Los 10 elementos mas grandes ordenados de mayor a menor
    Restricciones: Tiene que ser una lista numérica
    """
    if type(listaTamañoArchivos) != list:
        raise Exception("Debe ingresar una lista.")
    if not all(type(x) in (int, float) for x in listaTamañoArchivos):
        raise Exception("Debe ingresar una lista numérica.")
    listaArchivos = []
    tamañoArchivosOrdenado = listaTamañoArchivos.copy()
    contador = 0
    while contador < 10 and tamañoArchivosOrdenado != []:
        listaArchivos.append(tamañoArchivosOrdenado.pop(tamañoArchivosOrdenado.index(max(tamañoArchivosOrdenado))))
        contador += 1
    return listaArchivos

def topTamañoCarpetas(listaTamañoCarpetas):
    """ 
    Esta funcion retorna una lista con los 10 elementos mas grandes de una lista
    Entradas: Una lista con valores numéricos
    Salidas: Los 10 elementos mas grandes ordenados de mayor a menor
    Restricciones: Tiene que ser una lista numérica
    """
    if type(listaTamañoCarpetas) != list:
        raise Exception("Debe ingresar una lista.")
    if not all(type(x) in (int, float) for x in listaTamañoCarpetas):
        raise Exception("Debe ingresar una lista numérica.")
    listaCarpetas = []
    tamañoCarpetasOrdenado = listaTamañoCarpetas.copy()
    contador = 0
    while contador < 10 and tamañoCarpetasOrdenado != []:
        listaCarpetas.append(tamañoCarpetasOrdenado.pop(tamañoCarpetasOrdenado.index(max(tamañoCarpetasOrdenado))))
        contador += 1
    return listaCarpetas

def topArchivos(listaArchivos):
    """
    Esta funcion retorna un diccionario con los 10 archivos de mayor tamaño y su tamaño legible
    Entradas: Una lista con los 10 tamaños de archivos mas grandes en bytes
    Salidas: Un diccionario con la ruta del archivo como llave y su tamaño legible como valor
    Restricciones: Tiene que ser una lista numérica
    """
    if type(listaArchivos) != list:
        raise Exception("Debe ingresar una lista.")
    if not all(type(x) in (int, float) for x in listaArchivos):
        raise Exception("Debe ingresar una lista numérica.")
    copiaTamaño = tamañoArchivos.copy()
    copiaArchivos = archivos.copy()
    archivosFinal = {}
    for elemento in listaArchivos:
        posicionArchivo = copiaTamaño.index(elemento)
        del copiaTamaño[posicionArchivo]
        elementoFinal = copiaArchivos.pop(posicionArchivo)
        archivosFinal[elementoFinal] = obtenerTamaño(elementoFinal)
    return archivosFinal

def topCarpetas(listaCarpetas):
    """
    Esta funcion retorna un diccionario con las 10 carpetas con mayor cantidad de elementos
    Entradas: Una lista con los 10 mayores conteos de elementos de carpetas
    Salidas: Un diccionario con la ruta de la carpeta como llave y su cantidad de elementos como valor
    Restricciones: Tiene que ser una lista numérica
    """
    if type(listaCarpetas) != list:
        raise Exception("Debe ingresar una lista.")
    if not all(type(x) in (int, float) for x in listaCarpetas):
        raise Exception("Debe ingresar una lista numérica.")
    copiaTamaño = tamañoCarpetas.copy()
    copiaCarpetas = carpetas.copy()
    carpetasFinal = {}
    for elemento in listaCarpetas:
        posicionArchivo = copiaTamaño.index(elemento)
        del copiaTamaño[posicionArchivo]
        elementoFinal = copiaCarpetas.pop(posicionArchivo)
        carpetasFinal[elementoFinal] = elemento
    return carpetasFinal