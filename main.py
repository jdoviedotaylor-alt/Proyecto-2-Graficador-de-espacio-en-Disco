from easygui import *
import os
import sys
import pygame
from logica import *

def solicitarCarpeta():
    """
    Esta función solicita una carpeta válida al usuario.
    """
    continuar = buttonbox(msg="Bienvenido al Graficador de Espacio en Disco\n\nHecho por Zack Rojas y Jose Oviedo",title="Graficador de Espacio en Disco",
                          choices=["Continuar"])
    if continuar is None:
        sys.exit()
    continuar = buttonbox(msg="Selecciona una carpeta", title="Graficador de Espacio en Disco", choices = ["Continuar"])
    if continuar == None:
        sys.exit()
    carpeta = diropenbox(msg="Seleccione la carpeta que desea analizar", title="Graficador de Espacio en Disco")
    if not carpeta:
        msgbox(msg="No se seleccionó ninguna carpeta.", title= "ERROR", ok_button= "Cerrar")
        sys.exit()
    if not os.path.isdir(carpeta):
        msgbox(msg="La carpeta seleccionada no es válida.", title= "ERROR", ok_button= "Cerrar")
        sys.exit()
    return carpeta

def crearDiccionario(ruta):
    """
    Esta función se encarga de hacer un diccionario a partir de una ruta que el usuario selecciona
    Entradas: Ruta de una carpeta
    Salidas: Diccionario con la información de la carpeta
    Restricciones: ruta tiene que ser una ruta válida
    """
    if type(ruta) != str:
        raise Exception("La ruta debe ser un string")
    if not os.path.exists(ruta):
        raise Exception("Debe ingresar una ruta que exista")
    if not os.path.isdir(ruta):
        raise Exception("Debe ingresar una ruta de una carpeta")
    return informacionCarpeta(ruta)


colores = [
    (255, 182, 193),
    (173, 216, 230),
    (144, 238, 144),
    (255, 255, 153),
    (221, 160, 221),
    (255, 204, 153)
]

def graficarNodo(pantalla, fuente, nodo, x, y, ancho, nivel):
    """ 
    Esta funcion se encarga de graficar un nodo del diccionario, llega hasta el nivel de profundidad 6
    Entradas: pantalla: superficie de pygame donde se dibuja
              fuente: fuente de texto de pygame
              nodo: diccionario con la información del elemento a graficar
              x: coordenada horizontal donde inicia el rectángulo
              y: coordenada vertical donde inicia el rectángulo
              ancho: ancho del rectángulo
              nivel: nivel de profundidad actual en el árbol
    Salidas: No retorna nada, dibuja directamente sobre la pantalla
    Restricciones: nodo debe ser un diccionario con las llaves "nombre", "tamaño", "ruta" e "hijos"
                   nivel debe ser un entero entre 0 y 6
                   ancho debe ser un valor numérico positivo
    """
    if nivel == 6:
        return
    alto = 45
    color = colores[nivel % len(colores)]
    rectangulo = pygame.Rect(int(x),int(y),int(ancho),alto)
    pygame.draw.rect(pantalla, color, rectangulo)
    pygame.draw.rect(pantalla, (0, 0, 0), rectangulo, 1)
    if ancho > 70:
        texto = fuente.render(nodo["nombre"], True, (0, 0, 0))
        pantalla.blit(texto, (x + 5, y + 5))
        tamaño = obtenerTamaño(nodo["ruta"]) if os.path.isfile(nodo["ruta"]) else obtenerMedidaTamaño(nodo["tamaño"])
        textoTamaño = fuente.render(tamaño, True, (0, 0, 0))
        pantalla.blit(textoTamaño, (x + 5, y + 25))
    if len(nodo["hijos"]) == 0:
        return
    xActual = x
    for hijo in nodo["hijos"]:
        if nodo["tamaño"] == 0:
            break
        proporcion = hijo["tamaño"] / nodo["tamaño"]
        anchoHijo = ancho * proporcion
        graficarNodo(pantalla, fuente, hijo, xActual, y + alto, anchoHijo, nivel + 1)
        xActual += anchoHijo

def main():
    """ 
    Esta es la función principal del programa, primero se encarga de pedir la carpeta, luego realiza el
    gráfico, y al cerrar el gráfico muestra los tops de los archivos mas grandes y las carpetas con mas
    archivos
    Entradas: No tiene
    Salidas: No tiene, solo hace el gráfico y los tops
    Restricciones: Se requiere una carpeta válida seleccionada por el usuario
                   Se requiere que pygame y easygui estén instalados 
    """
    carpeta = solicitarCarpeta()
    nombreCarpeta = os.path.basename(carpeta)
    if nombreCarpeta == "":
        nombreCarpeta = carpeta
    try:
        diccionario = crearDiccionario(carpeta)
    except PermissionError:
        msgbox(msg="No se tienen permisos para acceder a la carpeta seleccionada.", title="ERROR", ok_button="Cerrar")
        sys.exit()
    except Exception as e:
        msgbox(msg=f"Error al analizar la carpeta: {e}", title="ERROR", ok_button="Cerrar")
        sys.exit()
    pygame.init()
    ANCHO = 1600
    ALTO = 800
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Graficador de Espacio en Disco")
    fuente = pygame.font.SysFont("Arial",14)
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        pantalla.fill((255, 255, 255))
        graficarNodo(pantalla,fuente,diccionario,20,20,1200,0)
        pygame.display.flip()
    pygame.quit()
    top10Archivos = topArchivos(topTamañoArchivos(tamañoArchivos))
    top10Carpetas = topCarpetas(topTamañoCarpetas(tamañoCarpetas))
    mensaje = "Top 10 archivos mas grandes\n"
    mensaje += "=" * 80 + "\n"
    for ruta, tamaño in top10Archivos.items():
        mensaje += f"{ruta:<70} {tamaño:>10}\n"
    mensaje += "\n\nTop 10 directorios con mas archivos\n"
    mensaje += "=" * 80 + "\n"
    for ruta, cantidad in top10Carpetas.items():
        mensaje += f"{ruta:<70} {cantidad:>10} archivos\n"
    textbox(msg="Tops del análisis", title="Graficador de Espacio en Disco", text=mensaje)
    
if __name__ == "__main__":
    main()