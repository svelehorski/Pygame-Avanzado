Shooter "Galaga" - Pygame Avanzado 

Este proyecto es un videojuego de disparos espacial desarrollado en Python utilizando la librería Pygame. El enfoque principal del desarrollo fue aplicar principios de Programación Orientada a Objetos (POO) y una arquitectura modular para garantizar un código escalable, organizado y eficiente.

Características Técnicas

Arquitectura Modular: Separación clara de responsabilidades entre lógica de juego, constantes, variables y funciones auxiliares.

Programación Orientada a Objetos (POO): Implementación de clases independientes para cada entidad del juego:

Jugador: Gestión de movimiento y estados de la nave.

Enemigos (Tipo 1 y 2): Patrones de movimiento y ataque diferenciados.

Boss: Lógica de jefe final con mayor resistencia y patrones complejos.

Balas: Gestión de proyectiles y trayectorias.

Explosión: Sistema de animaciones mediante secuencias de imágenes.

Persistencia de Datos: Implementación de un sistema de High Scores utilizando archivos JSON para guardar y recuperar los puntajes de los jugadores.

Gestión Multimedia: Integración de assets visuales (PNG) y sonoros (MP3) con optimización de carga.

Lógica de Colisiones: Sistema preciso de detección de impactos entre múltiples entidades.

Estructura del Proyecto

El código se divide en módulos especializados para facilitar el mantenimiento:

main.py: Punto de entrada y loop principal del juego.

clase_*.py: Definiciones de las entidades (Jugador, Enemigos, Balas, etc.).

funciones.py: Lógica reutilizable y procesos de soporte.

constantes.py / variables.py: Centralización de configuraciones y estados globales.

puntaje.json: Almacenamiento persistente de datos de usuario.

/imagenes & /sonidos: Repositorio de recursos multimedia.
