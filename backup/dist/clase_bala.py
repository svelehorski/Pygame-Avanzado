import pygame
from constantes import *


bala_animacion = []
y = 40
for i in range(14):
    fila = "imagenes/balas/bala0{}.png".format(i)
    imagen = pygame.image.load(fila)
    imagen.set_colorkey(BLACK)
    if i <= 6:
        y += 15
    imagen = pygame.transform.scale(imagen, (50, y))
    bala_animacion.append(imagen)

class Bala(pygame.sprite.Sprite):
    """
    Clase que representa una bala en el juego
    Atributos:
    - image (pygame.Surface): Imagen de la bala
    - rect (pygame.Rect): Rectángulo que representa la posicion y tamaño de la bala en la pantalla
    - velocidad (int): Velocidad vertical de la bala
    - personaje (bool): True si la bala es disparada por el personaje, False si es disparada por el jefe
    Métodos:
    - __init__: Inicializa la instancia de la bala
    - update: Actualiza la posicion de la bala y la elimina si sale de la pantalla
    """
    def __init__(self, x, y, personaje = False):
        """
        Inicializa la instancia de la bala
        Configura la imagen, posicion inicial, velocidad y tipo de la bala
        Parametros:
        - x (int): Coordenada x inicial de la bala
        - y (int): Coordenada y inicial de la bala
        - personaje (bool): True si la bala es disparada por el personaje, False si es disparada por el jefe
        """
        super().__init__()
        if personaje:
            self.frame = 0 
            self.image = bala_animacion[self.frame]
            self.last_update = pygame.time.get_ticks() #guarda el tiempo del ultimo cambio de fotograma
            self.frame_rate = 50
        else:
            self.image = pygame.image.load("imagenes/bala_boss.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidad = -10
        self.personaje = personaje
        

    def update(self):
        """
        Actualiza la posicion de la bala y la elimina si sale de la pantalla.
        """
        if self.personaje:
            self.rect.y += self.velocidad
            if self.rect.bottom < 0:
                self.kill()
            ahora = pygame.time.get_ticks()
            if ahora - self.last_update > self.frame_rate:
                if self.frame == len(bala_animacion) - 1:
                    self.frame = 6
                self.last_update = ahora
                self.frame += 1
                self.image = bala_animacion[self.frame]
        else:
            self.rect.y -= self.velocidad
            if self.rect.bottom < 0:
                self.kill()