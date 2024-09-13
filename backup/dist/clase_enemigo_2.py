from typing import Any
import pygame
from constantes import *
from clase_bala import *
from clase_jugador import *
import random 

class Enemigo(pygame.sprite.Sprite):
    """
    Clase que representa a un enemigo en el juego
    Atributos:
    - image (pygame.Surface): Imagen del enemigo
    - rect (pygame.Rect): Rectangulo que representa la posición y tamaño del enemigo en la pantalla
    - velocidad (int): Velocidad vertical del enemigo
    Métodos:
    - __init__: Inicializa la instancia del enemigo
    - dibujar: Dibuja el enemigo en una superficie
    - update: Actualiza la posición del enemigo y reinicia su posicion si sale de la pantalla
    """
    def __init__(self):
        """
        configura la imagen, posicion inicial y velocidad del enemigo
        """
        super().__init__()
        self.image = pygame.image.load("imagenes/enemigo2.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.velocidad = 7
        self.rect.top = random.randrange(-160, 0)
        self.rect.left = random.randrange(ANCHO_VENTANA - self.rect.width)

    def dibujar(self, superficie):
        """
        Dibuja el enemigo en una superficie
        Parametros:
        - superficie (pygame.Surface): Superficie en la que se dibujara el enemigo
        """
        superficie.blit(self.image, self.rect)

    def update(self):
        """
        Actualiza la posicion del enemigo y reinicia su posicion si sale de la pantalla
        """
        self.rect.move_ip(0, self.velocidad) #Mueve el rectangulo en el eje Y (vertical) por una cantidad especificada por self.velocidad,lo utilizo para cambiar de posicion el rectangulo 
        if self.rect.top > ALTO_VENTANA + 10 or self.rect.left < -40 or self.rect.right > ANCHO_VENTANA + 25:
            self.rect.x = random.randrange(ANCHO_VENTANA - self.rect.width) #horizontal
            self.rect.y = random.randrange(-100, -40) #elige una posiciOn Y aleatoria por encima de la ventana, proporcionando una apariencia de reinicio desde la parte superior de la pantalla
