import os

archivos = []
carpetas = []


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
    global archivos, carpetas
    nombre = os.path.basename(ruta)
    tamaño = os.path.getsize(ruta)
    hijos = []
    if os.path.isfile(ruta):
        archivos.append({"Nombre": nombre, "Tamaño": tamaño})
        return {"Nombre":nombre, "Tamaño": tamaño, "Ruta": ruta, "Hijos":hijos}
    carpetas.append({"Nombre": nombre, "Tamaño": len})
    elementos = os.listdir(ruta)
    for elemento in elementos:
        rutaElemento = os.path.join(ruta, elemento)
        infoElemento = informacionCarpetaAux(rutaElemento)
        hijos.append(infoElemento)
    return {"Nombre":nombre, "Tamaño": tamaño, "Ruta": ruta, "Hijos":hijos}
