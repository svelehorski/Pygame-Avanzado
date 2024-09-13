import pygame
from funciones import *

posicion_click = None
player = None
jefe = None
estado = "pantalla inicio"
puntaje = 0
enemigo_actual = ""
nombre_jugador = ""
niveles = 0
bandera = True
jugador_sprite = True
flag_ejecutar = True
guardado = False
gano = False
tiempo_restante = pygame.time.get_ticks() 
mute = False
disparo_jefe = 0
procedimiento_reinicio = False