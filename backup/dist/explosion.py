import pygame
import os
from constantes import *
from clase_jugador import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, centro):
        super().__init__()
        self.image = explosion_animacion[0] #la lista en la posicion del primer fotograma 
        self.rect = self.image.get_rect()#es el rectangulo que rodea la imagen. Se coloca en el centro especificado al crear la instancia.
        self.rect.center = centro
        self.frame = 0 #mantiene el indice del fotograma actual de la animacion
        self.last_update = pygame.time.get_ticks() #guarda el tiempo del ultimo cambio de fotograma
        self.frame_rate = 50 #velocidad de la animacion de la explosion

    def update(self):
        """
        Actualiza la animación de la explosion en cada fotograma
        Si ha alcanzado el final de la animación, elimina la instancia de la explosion 
        En caso contrario, actualiza la imagen y el rectangulo para mostrar el siguiente fotograma de la animacion
        """
        ahora = pygame.time.get_ticks()
        if ahora - self.last_update > self.frame_rate:
            self.last_update = ahora
            self.frame += 1
            if self.frame == len(explosion_animacion):
                self.kill()
            else:
                centro = self.rect.center
                self.image = explosion_animacion[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = centro

explosion_animacion = []
for i in range(9):
    fila = "imagenes/explosion/explosion0{}.png".format(i)
    imagen = pygame.image.load(fila)
    imagen.set_colorkey(BLACK)
    imagen = pygame.transform.scale(imagen, (70, 70))
    explosion_animacion.append(imagen)

