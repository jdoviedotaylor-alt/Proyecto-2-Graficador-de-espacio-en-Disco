from easygui import *
import os
import sys
import pygame

def solicitarCarpeta():
    """
    Solicita una carpeta válida al usuario.
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


# ==================================================
# DATOS DE PRUEBA
# ==================================================

def crearArbolPrueba(nombre):
    """
    Árbol falso para probar la interfaz.
    """

    return {"nombre": nombre, "tamano": 100,"hijos":[{"nombre": "Prueba","tamano": 40,"hijos": [
                    {
                        "nombre": "PDF",
                        "tamano": 15,
                        "hijos": []
                    },
                    {
                        "nombre": "Tareas",
                        "tamano": 25,
                        "hijos": []
                    }
                ]
            },
            {
                "nombre": "Videos",
                "tamano": 35,
                "hijos": [
                    {
                        "nombre": "Peliculas",
                        "tamano": 20,
                        "hijos": []
                    },
                    {
                        "nombre": "Series",
                        "tamano": 15,
                        "hijos": []
                    }
                ]
            },
            {
                "nombre": "Musica",
                "tamano": 25,
                "hijos": []
            }
        ]
    }


COLORES = [
    (255, 182, 193),
    (173, 216, 230),
    (144, 238, 144),
    (255, 255, 153),
    (221, 160, 221),
    (255, 204, 153)
]


def dibujarNodo(pantalla, fuente, nodo, x, y, ancho, nivel):

    alto = 45
    color = COLORES[nivel % len(COLORES)]
    rectangulo = pygame.Rect(int(x),int(y),int(ancho),alto)
    pygame.draw.rect(
        pantalla,
        color,
        rectangulo)
    pygame.draw.rect(pantalla,(0, 0, 0),rectangulo,1)
    if ancho > 70:
        texto = fuente.render(nodo["nombre"],True,(0, 0, 0))
        pantalla.blit(texto,(x + 5, y + 5))
    if len(nodo["hijos"]) == 0:
        return
    xActual = x
    for hijo in nodo["hijos"]:
        proporcion = hijo["tamano"] / nodo["tamano"]
        anchoHijo = ancho * proporcion
        dibujarNodo(
            pantalla,
            fuente,
            hijo,
            xActual,
            y + alto,
            anchoHijo,
            nivel + 1)
        xActual += anchoHijo

def main():
    carpeta = solicitarCarpeta()
    nombreCarpeta = os.path.basename(carpeta)
    if nombreCarpeta == "":
        nombreCarpeta = carpeta
    arbol = crearArbolPrueba(nombreCarpeta)
    pygame.init()
    ANCHO = 1300
    ALTO = 700
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Graficador de Espacio en Disco")
    fuente = pygame.font.SysFont("Arial",14)
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        # Fondo blanco
        pantalla.fill((255, 255, 255))
        # Árbol
        dibujarNodo(pantalla,fuente,arbol,20,20,1200,0)
        pygame.display.flip()
    pygame.quit()
main()

