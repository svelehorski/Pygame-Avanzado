import pygame
import json
from clase_enemigo_1 import *
from clase_jugador import *
from constantes import *
from clase_enemigo_2 import *
from clase_boss import *
from explosion import *
from variables import *

explosion_sprite = pygame.sprite.Group()

def dibujar_texto(superficie, texto, tamaño, x, y, color_texto = COLOR_BLANCO, fondo = False):
    """
    Dibuja texto en una superficie de juego Pygame
    Parametros:
    - superficie (pygame.Surface): La superficie de juego en la que se dibujara el texto
    - texto (str): El texto que se va a dibujar
    - tamaño (int): El tamaño de la fuente del texto
    - x (int): La coordenada x del centro del texto
    - y (int): La coordenada y del centro del texto
    - color_texto (tuple, opcional): El color del texto en formato RGB. Por defecto, es blanco 
    - fondo (bool, opcional): Indica si se debe dibujar un fondo detrás del texto. Por defecto, es False.
    devuelve:
    - pygame.Rect or None: Devuelve un objeto Rect de Pygame que representa el área ocupada por el texto
    si fondo es True, de lo contrario, devuelve None
    """
    font = pygame.font.SysFont("impact", tamaño)
    texto_superficie = font.render(texto, True, color_texto)
    texto_rect = texto_superficie.get_rect()
    texto_rect = texto_rect.move(x - (texto_rect[2] / 2), y - (texto_rect[3] / 2))
    if fondo:
        boton = pygame.draw.rect(superficie, COLOR_BLANCO, (texto_rect[0] - 25, texto_rect[1] - 10, texto_rect[2] + 50, texto_rect[3] + 20))
    superficie.blit(texto_superficie, texto_rect)
    if fondo:
        return boton


def temporizador(tiempo_nivel, estado):
    tiempo_actual = pygame.time.get_ticks() 
    if tiempo_actual >= tiempo_nivel:
        estado = "pantalla ganar"
    return estado

def crear_explosion(golpe, explosion_sonido):
    """
    se crea una explosion en la posición del objeto que ha sufrido el golpe (golpe)
    """
    explosion = Explosion(golpe.rect.center)
    explosion_sprite.add(explosion)
    explosion_sonido.play()

def dibujar_vida(superficie, x, y, porcentaje):
    """
    Dibuja una barra de vida en la superficie especificada
    Parametros:
    - superficie: La superficie de juego en la que se dibujara la barra de vida.
    - x: La coordenada x en la que se posicionara la barra de vida.
    - y: La coordenada y en la que se posicionara la barra de vida.
    - porcentaje: El porcentaje de vida representado por la barra.
    """
    largo_barra = 100
    alto_barra = 10
    fill = (porcentaje / 100) * largo_barra #el ancho se calcula multiplicando el porcentaje de vida (porcentaje) por el ancho total de la barra (largo_barra).
    borde = pygame.Rect(x, y, largo_barra, alto_barra) #Se crean dos rectángulos: uno para la parte llena de la barra (fill) y otro para el borde completo de la barra (borde).Dibujo de la Parte Llena:
    fill = pygame.Rect(x, y, fill, alto_barra)
    pygame.draw.rect(superficie, COLOR_VERDE, fill)
    pygame.draw.rect(superficie, COLOR_VERDE, borde, 2)

def mostrar_pantalla_inicio(pantalla, imagen, nombre_jugador):
    pantalla.blit(imagen, imagen.get_rect())
    dibujar_texto(pantalla, "SHOOTER", 65, ANCHO_VENTANA // 2, ALTO_VENTANA // 4)
    #dibujar_texto(pantalla, "Instrucciones aqui", 27, ANCHO_VENTANA // 2, ALTO_VENTANA // 2)
    dibujar_texto(pantalla, "INGRESE SU NOMBRE (3 CARACTERES):", 20, 850,360)
    dibujar_texto(pantalla, nombre_jugador, 20, ANCHO_VENTANA // 2, ALTO_VENTANA // 2)
    rectangulo_puntaje = dibujar_texto(pantalla, "VER PUNTAJES", 20, 852, 690, BLACK, True)
    return rectangulo_puntaje

def mostrar_pantalla_ganar(pantalla, imagen, puntaje):
    pantalla.blit(imagen, imagen.get_rect())
    dibujar_texto(pantalla, f"PUNTAJE ACTUAL: {puntaje}", 45, ANCHO_VENTANA // 2, ALTO_VENTANA // 4)
    rectangulo_reiniciar = dibujar_texto(pantalla, "SIGUIENTE NIVEL", 20,  ANCHO_VENTANA / 2, ALTO_VENTANA * 3/4, BLACK, True)
    rectangulo_voler = dibujar_texto(pantalla, "RENDIRSE", 20, 852, 510, BLACK, True)
    return rectangulo_reiniciar, rectangulo_voler

def guardar_datos(nombre: str, puntuacion: int, nivel: int, lista: list):
    """
    brief: guarda la informacion de un jugador en una lista y la ordena por puntuacion y nivel
    Parametros:
    - nombre (str): Nombre del jugador
    - puntuacion (int): Puntuacion del jugador
    - nivel (int): Nivel del jugador
    - lista (list): Lista de diccionarios que representan informacion de jugadores
    devuelve:
    - list: Lista ordenada de diccionarios representando informacian de jugadores
    """
    jugador_actual = {"nombre": nombre, "puntuacion": puntuacion, "nivel": nivel}
    lista.append(jugador_actual)
    for puntaje in range(len(lista)):
        for puntaje_dos in range(len(lista)):
            if lista[puntaje]["puntuacion"] > lista[puntaje_dos]["puntuacion"]: #intercambian si es mayor
                auxiliar = lista[puntaje]
                lista[puntaje] = lista[puntaje_dos]
                lista[puntaje_dos] = auxiliar
            if lista[puntaje]["puntuacion"] == lista[puntaje_dos]["puntuacion"]: #se comparan niveles si son la misma puntuacion
                if lista[puntaje]["nivel"] > lista[puntaje_dos]["nivel"]:
                    auxiliar = lista[puntaje]
                    lista[puntaje] = lista[puntaje_dos]
                    lista[puntaje_dos] = auxiliar
                else:
                    auxiliar = lista[puntaje_dos] #no se cambian posiciones si son iguales
                    lista[puntaje_dos] = lista[puntaje]
                    lista[puntaje] = auxiliar
    return lista

def generar_json(lista: list):
    """
    Genera un archivo JSON a partir de una lista de puntuaciones
    Parametros:
    - lista (list): Lista de diccionarios que representan informacion de jugadores
    """
    diccionario = {}
    diccionario["puntajes"] = lista
    with open("puntaje.json", "w") as archivo:
        json.dump(diccionario, archivo, indent=4) #convierte el diccionario a formato JSON y lo escribe en el archivo

def recibir_puntuaciones():
    """
    Lee un archivo JSON que contiene puntuaciones y devuelve la lista de puntuaciones
    Parametros:
    - Ninguno
    Retorna:
    - list: Lista de diccionarios que representan información de jugadores
    """
    with open('puntaje.json', "r") as archivo:
        dict = json.load(archivo)
        lista = dict["puntajes"] # extrae la lista de puntuaciones del diccionario
        return lista

def limpiar_lista_de_grupos(lista:pygame.sprite.Group):
    for i in lista:
        lista.remove(i)

def mostrar_pantalla_puntaje(pantalla, imagen, lista):
    """
    Muestra la pantalla de las mejores puntuaciones en el juego
    Parametros:
    - pantalla (pygame.Surface): Superficie en la que se muestra la pantalla.
    - imagen (pygame.Surface): Imagen de fondo de la pantalla
    - lista (list): Lista de diccionarios que representan informacion de jugadores
    Retorna:
    - pygame.Rect: Rectangulo que representa la posicion y tamaño del boton para volver a la pantalla de inicio
    """
    pantalla.blit(imagen, imagen.get_rect())
    dibujar_texto(pantalla, "MEJORES 10 PUNTAJES", 65, ANCHO_VENTANA // 2, ALTO_VENTANA // 4)
    tamaño_lista = len(lista)
    y = 300
    for i in range(10):
        y += 30
        if tamaño_lista - 1 >= i:
            puntuacion = lista[i]["nombre"]+"       "+str(lista[i]["puntuacion"])
        else:
            puntuacion = "Jugador inexistente        ----"
        dibujar_texto(pantalla, puntuacion,20, 850, y, COLOR_BLANCO)
    rectangulo_inicio = dibujar_texto(pantalla, "VOLVER A INICIO", 20, 850, 730, BLACK, True)
    return rectangulo_inicio

def mostrar_pantalla_final(pantalla, imagen, puntaje, lista):
    pantalla.blit(imagen, imagen.get_rect())
    dibujar_texto(pantalla, f"PUNTAJE FINAL: {puntaje}", 45, ANCHO_VENTANA // 2, ALTO_VENTANA // 4)
    rectangulo_reiniciar = dibujar_texto(pantalla, "REINICIAR", 20,  ANCHO_VENTANA / 2, ALTO_VENTANA * 3/4, BLACK, True)
    rectangulo_voler = dibujar_texto(pantalla, "VOLVER A INICIO", 20, 852, 510, BLACK, True)
        #base de datos de puntuacion
    dibujar_texto(pantalla, "NOMBRE     PUNTAJE", 20, 500, 305, COLOR_BLANCO)
    tamaño_lista = len(lista)
    y = 300
    for i in range(3):
        y += 30
        if tamaño_lista - 1 >= i:
            puntuacion = lista[i]["nombre"]+"       "+str(lista[i]["puntuacion"])
        else:
            puntuacion = "Jugador inexistente        ----"
        dibujar_texto(pantalla, puntuacion,20, 500, y, COLOR_BLANCO)
    return rectangulo_reiniciar, rectangulo_voler

def disparo_boss(disparo_jefe, jefe):
    disparo_jefe += 1
    if disparo_jefe >= 60:
        jefe.disparar()
        disparo_jefe = 0
    return disparo_jefe

def limpiar_todos_grupos_sprites():
    limpiar_lista_de_grupos(all_sprites)
    limpiar_lista_de_grupos(enemigo_list)
    limpiar_lista_de_grupos(bullets)
    limpiar_lista_de_grupos(sprite_boss)

def checar_colisiones(lista_player, lista_bala, jefe, player, explosion_sonido, puntaje, enemigo_actual):
    gano = False
    bandera = False
    for i in range(len(lista_bala)):
        if i == 1:
            bandera = True
        golpes = pygame.sprite.groupcollide(lista_bala[i], bullets, bandera, True)
        for golpe in golpes:
            if i == 0:
                gano = jefe.recibir_disparo()
                jefe.chequeo_segunda_fase(enemigo_actual)
            else:
                puntaje += 10
                crear_enemigo(enemigo_actual)
            crear_explosion(golpe, explosion_sonido)
        #Verificar colisiones choque a jugador
        golpes = pygame.sprite.spritecollide(player, lista_player[i], True)
        for golpe in golpes:
            player.shield -= 25
            crear_explosion(golpe, explosion_sonido)
            if i == 0:
                crear_enemigo(enemigo_actual)
    return gano, puntaje