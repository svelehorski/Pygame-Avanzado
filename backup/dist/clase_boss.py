import pygame
from constantes import *
from clase_jugador import *
from clase_bala import *
from clase_enemigo_1 import *
from clase_enemigo_2 import *


bullets_boss = pygame.sprite.Group()
enemigo_list = pygame.sprite.Group()
sprite_boss = pygame.sprite.Group()


def crear_enemigos(enemigos: int, tipo_e:str):
        for i in range(enemigos):
            crear_enemigo(tipo_e)

def crear_enemigo(enemigo:str):
    """
    añade un enemigo especifico a su respectivo grupo de sprite, dependiendo que enemigo sea
    """
    if enemigo == "boss":
        nuevo_enemigo = Boss()
        sprite_boss.add(nuevo_enemigo)
    else:
        if enemigo == "asteroide":
            nuevo_enemigo = Asteroide()
        elif enemigo == "nave_e":
            nuevo_enemigo = Enemigo()
        enemigo_list.add(nuevo_enemigo)
        all_sprites.add(nuevo_enemigo)
    return nuevo_enemigo 

class Boss(pygame.sprite.Sprite):
    """
    Clase que representa al jefe en el juego
    Atributos:
    - image (pygame.Surface): Imagen del jefe
    - rect (pygame.Rect): Rectángulo que representa la posición y tamaño del jefe en la pantalla
    - velocidad (int): Velocidad horizontal del jefe
    - vida (int): Puntos de vida del jefe
    - lado (str): Direccion actual del movimiento del jefe "derecha" o "izquierda"
    Metodos:
    - __init__: Inicializa la instancia del jefe
    - dibujar: Dibuja el jefe en una superficie
    - update: Actualiza la posición del jefe y cambia de direccion cuando alcanza los limites de la pantalla
    - disparar: Crea y dispara una bala desde la posicion del jefe
    - recibir_disparo: Reduce los puntos de vida del jefe y devuelve True si el jefe ha sido derrotado
    """
    def __init__(self):
        """
        Configura la imagen, posicion inicial, velocidad y puntos de vida del jefe
        """
        super().__init__()
        self.image = pygame.image.load("imagenes/boss.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.velocidad = 2
        self.rect.top = 0
        self.vida = 20
        self.lado = "derecha"

    def chequeo_segunda_fase(self, enemigo_actual):
        if self.vida == 10:
            crear_enemigos(8, enemigo_actual)
            self.velocidad = 5

    def update(self):
        """
        Actualiza la posicion del jefe y cambia de direccion cuando alcanza los limites de la pantalla
        """
        match self.lado:
            case "derecha":
                self.rect.move_ip(self.velocidad, 0)
            case "izquierda":
                self.rect.move_ip(-self.velocidad, 0)
        if self.rect.right >= ANCHO_VENTANA:
            self.lado = "izquierda"
        elif (self.rect.left <= 0):
            self.lado = "derecha"


    def dibujar(self, superficie):
        """
        Dibuja el jefe en una superficie
        Parametros:
        - superficie (pygame.Surface): Superficie en la que se dibujara el jefe
        """
        superficie.blit(self.image, self.rect)

    def disparar(self):
        """
        Crea y dispara una bala desde la posicion del jefe
        Crea una instancia de la clase Bala y la agrega a los grupos de sprites correspondientes
        """
        bala = Bala(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bala)
        bullets_boss.add(bala)

    def recibir_disparo(self):
        """
        Reduce los puntos de vida del jefe y devuelve True si el jefe ha sido derrotado
        Returns:
        - bool: True si el jefe ha sido derrotado, False de lo contrario
        """
        self.vida -= 1
        if self.vida == 0:
            return True
        else:
            return False

