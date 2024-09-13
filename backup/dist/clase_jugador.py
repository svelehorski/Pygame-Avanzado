from typing import Any
import pygame
from constantes import *
from clase_bala import *

pygame.init()
pygame.mixer.init()

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
laser_sonido = pygame.mixer.Sound('sonidos\disparo.mp3')

jugador_izquierda = pygame.image.load("imagenes/jugador/nave00.png")
jugador_izquierda = pygame.transform.scale(jugador_izquierda, (120, 132))
jugador_centro = pygame.image.load("imagenes/jugador/nave01.png")
jugador_centro = pygame.transform.scale(jugador_centro, (120, 132))
jugador_derecha = pygame.image.load("imagenes/jugador/nave02.png")
jugador_derecha = pygame.transform.scale(jugador_derecha, (120, 132))

jugador_animacion = {"izquierda": jugador_izquierda,
                    "centro": jugador_centro,
                    "derecha": jugador_derecha}

class Jugador(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__()
        """
        Configura la imagen, posicion inicial, velocidad y escudo del jugador
        """
        self.image = jugador_animacion["centro"]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO_VENTANA // 2
        self.rect.bottom = ALTO_VENTANA - 10
        self.velocidad_x = 0
        self.shield = 100
        self.colldown = 0
        all_sprites.add(self)

    def update(self):
        self.velocidad_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            direccion = "izquierda"
            self.velocidad_x = -6
        elif keystate[pygame.K_RIGHT]:
            direccion = "derecha"
            self.velocidad_x = 6 
        else:
            direccion = "centro"
        self.rect.x += self.velocidad_x
        #verifico cuando el jugador choca con los bordes de la pantalla, para que no se salga
        if self.rect.right > ANCHO_VENTANA:
            self.rect.right = ANCHO_VENTANA
        if self.rect.left < 0:
            self.rect.left = 0
        self.image = jugador_animacion[direccion]

    def disparar(self):
        self.colldown = pygame.time.get_ticks() + 500
        bala = Bala(self.rect.centerx, self.rect.top, True)
        all_sprites.add(bala)
        bullets.add(bala)
        laser_sonido.play()