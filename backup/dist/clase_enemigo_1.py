from typing import Any
import pygame
import random
from constantes import *

asteroid_images = []
asteroid_list = ["imagenes/asteroide1.png","imagenes/asteroide2.png", "imagenes/asteroide3.png"]
for img in asteroid_list:
    asteroid_images.append(pygame.image.load(img))

class Asteroide(pygame.sprite.Sprite):
    """
    Clase que representa un asteroide en el juego
    Atributos:
    - image (pygame.Surface): Imagen del asteroide
    - rect (pygame.Rect): Rectángulo que representa la posición y tamaño del asteroide en la pantalla
    - velocidad (int): Velocidad vertical del asteroide
    - velocidadx (int): Velocidad horizontal del asteroide
    Métodos:
    - __init__: Inicializa la instancia del asteroide
    - update: Actualiza la posicion del asteroide y reinicia su posicion si sale de la pantalla
    """
    def __init__(self):
        """
        Configura la imagen, posicion inicial y velocidad del asteroide
        """
        super().__init__()
        self.image = random.choice(asteroid_images)
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO_VENTANA - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.velocidad = random.randrange(1, 10)
        self.velocidadx = random.randrange(-5, 5)

    def update(self):
        """
        Actualiza la posicion del asteroide y reinicia su posición si sale de la pantalla
        Si el asteroide sale de la pantalla por la parte inferior, izquierda o derecha, se reposiciona aleatoriamente arriba de la pantalla 
        y se eligen nuevas velocidades vertical y horizontal
        """
        self.rect.y += self.velocidad #se incrementa la velocidad vertical
        self.rect.x += self.velocidadx#se incrementa la velocidad horizontal
        if self.rect.top > ALTO_VENTANA + 10 or self.rect.left < -40 or self.rect.right > ANCHO_VENTANA + 25:
            self.rect.x = random.randrange(ANCHO_VENTANA - self.rect.width) #se reposiciona aleatoriamente arriba de la pantalla 
            self.rect.y = random.randrange(-100, -40)
            self.velocidad = random.randrange(1, 10)#se eligen nuevas velocidades vertical y horizontal