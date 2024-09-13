import pygame
from constantes import *
from clase_enemigo_1 import *
from clase_bala import *
from clase_jugador import *
from funciones import *
from explosion import *
from clase_enemigo_2 import *
from variables import *

pygame.init()
pygame.mixer.init()

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("SHOOTER")
tiempo = pygame.time.Clock()

imagen = pygame.image.load("imagenes/fondo1.png")
imagen = pygame.transform.scale(imagen, (ANCHO_VENTANA, ALTO_VENTANA))
fondo = pygame.image.load("imagenes/fondo3.png")
fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA, ALTO_VENTANA))
sonido = pygame.image.load("imagenes/sonido.png")
sonido = pygame.transform.scale(sonido, (50,50))
perdio = pygame.image.load("imagenes/fin2.png")
perdio = pygame.transform.scale(perdio, (100,120))

pygame.mixer.music.load('sonidos\musica.mp3')
pygame.mixer.music.play(-1) #utilizo -1 para reproducir la musica en bucle infinito 
pygame.mixer.music.set_volume(0.4)
explosion_sonido = pygame.mixer.Sound("sonidos/explosion_enemigo.mp3")

lista_puntuaciones = recibir_puntuaciones()
while flag_ejecutar:
    match estado:
        case "pantalla inicio":
            rectangulo_puntaje = mostrar_pantalla_inicio(pantalla, fondo, nombre_jugador)
            limpiar_todos_grupos_sprites()
        case "pantalla final":
            ternario = mostrar_pantalla_final(pantalla, fondo, puntaje, lista_puntuaciones)
            rectangulo_reiniciar = ternario[0] 
            rectangulo_voler = ternario[1]
            if not(guardado):
                guardar_datos(nombre_jugador, puntaje, niveles, lista_puntuaciones)
                guardado = True
            if player.shield == 0: pantalla.blit(perdio, (800,45))
        case "pantalla ganar":
            ternario = mostrar_pantalla_ganar(pantalla, fondo, puntaje)
            rectangulo_siguiente = ternario[0] 
            rectangulo_rendirse = ternario[1]
        case "pantalla puntajes":
            rectangulo_inicio = mostrar_pantalla_puntaje(pantalla, fondo, lista_puntuaciones)

        case "niveles":
            tiempo_restante = (tiempo_nivel - pygame.time.get_ticks()) / 1000
            match niveles:
                case 1:
                    if bandera:
                        enemigo_actual = "asteroide"
                        crear_enemigos(8, enemigo_actual)
                        bandera = False
                    estado = temporizador(tiempo_nivel, estado)

                case 2:
                    enemigo_actual = "nave_e"
                    if bandera:
                        crear_enemigos(10, enemigo_actual)
                        bandera = False
                    estado = temporizador(tiempo_nivel, estado)

                case 3:
                    if bandera:
                        enemigo_actual = "boss"
                        jefe = crear_enemigo(enemigo_actual)
                        enemigo_actual = "asteroide"
                        bandera = False # La bandera se establece en falso para que este bloque de codigo no se ejecute nuevamente
                    disparo_jefe = disparo_boss(disparo_jefe, jefe)
                    if gano:
                        puntaje += 250
                        estado = "pantalla final"
                        gano = False

            lista_colision_player = [enemigo_list, bullets_boss]
            lista_colision_bala = [sprite_boss, enemigo_list]
            ternario = checar_colisiones(lista_colision_player, lista_colision_bala, jefe, player, explosion_sonido, puntaje, enemigo_actual)
            gano = ternario[0]
            puntaje = ternario[1]

            if player.shield <= 0: estado = "pantalla final"

            pantalla.blit(imagen, imagen.get_rect())
            all_sprites.draw(pantalla)
            explosion_sprite.draw(pantalla)
            if niveles == 3:
                sprite_boss.draw(pantalla)
                explosion_sprite.draw(pantalla)

            #marcador y temporizador
            if niveles != 3: dibujar_texto(pantalla, f"TIEMPO RESTANTE: {tiempo_restante:.2f}", 20, 1200, 10, COLOR_BLANCO)
            dibujar_texto(pantalla, str(puntaje), 25, ANCHO_VENTANA//2, 10) #puntaje en pantalla
            dibujar_vida(pantalla, 5, 5, player.shield)#vida del jugador

    ternario = None
    tiempo.tick(60)
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT: flag_ejecutar = False

        if evento.type == pygame.MOUSEBUTTONDOWN: posicion_click = list(evento.pos) #lo casteo a lista porq evento.pos esuna tupla

        if estado == "pantalla inicio":
            #verifico el tipo de evento de teclas para que el usuario se registre, solo puede registrarse con un nombre de hasta 3 caracteres
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                else:
                    if len(nombre_jugador) <= 2:
                        nombre_jugador += evento.unicode
                if len(nombre_jugador) == 3:
                        if evento.key == pygame.K_RETURN: procedimiento_reinicio = True
            if posicion_click != None:
                if rectangulo_puntaje.collidepoint(posicion_click): estado = "pantalla puntajes"

        elif estado == "pantalla final":
            if posicion_click != None: 
                limpiar_todos_grupos_sprites()
                if rectangulo_reiniciar.collidepoint(posicion_click): 
                    procedimiento_reinicio = True
                elif rectangulo_voler.collidepoint(posicion_click):
                    estado = "pantalla inicio"
                    nombre_jugador = ""

        elif estado == "pantalla ganar":
            if posicion_click != None: 
                if rectangulo_siguiente.collidepoint(posicion_click):
                    bandera = True
                    if niveles < 3: niveles += 1
                    estado = "niveles"
                    limpiar_todos_grupos_sprites()
                    player = Jugador(all_sprites)
                    tiempo_nivel = pygame.time.get_ticks() + 30000
                elif rectangulo_rendirse.collidepoint(posicion_click): estado = "pantalla final"

        elif estado == "pantalla puntajes":
            if posicion_click != None:
                if rectangulo_inicio.collidepoint(posicion_click): estado = "pantalla inicio"

        #Verifico la tecla del disparo del jugador
        elif estado == "niveles":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if player.colldown <= pygame.time.get_ticks(): player.disparar()

                #Silenciar/Reacticar Musica
                elif evento.key == pygame.K_s:
                    if mute:
                        pygame.mixer.music.set_volume(0.4)
                        mute = False
                    else:
                        pygame.mixer.music.set_volume(0.0)
                        mute = True

    if procedimiento_reinicio:
        niveles = 1
        estado = "niveles"
        puntaje = 0
        player = Jugador(all_sprites)
        bandera = True
        gano = False
        tiempo_nivel = pygame.time.get_ticks() + 30000
        procedimiento_reinicio = False 

    if mute: pantalla.blit(sonido, (1650, 10))

    posicion_click = None
    all_sprites.update()
    explosion_sprite.update()

    if niveles == 3: sprite_boss.update()
    pygame.display.flip()

generar_json(lista_puntuaciones)
pygame.quit()