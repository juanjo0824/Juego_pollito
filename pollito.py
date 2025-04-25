import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Constantes
ANCHO = 800
ALTO = 600
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
GRIS_CLARO = (169, 169, 169)
VERDE = (34, 139, 34)
MARRON = (139, 69, 19)
AMARILLO = (255, 255, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
CELESTE = (135, 206, 250)
FPS = 60

# Crear ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("El Pollito Cruza la Ciudad")

# Reloj
clock = pygame.time.Clock()

# Pollito
pollito = pygame.Rect(380, 540, 40, 40)
vidas = 3

# Crear coches (2 carriles por calle)
coches_calle1_izq = [pygame.Rect(random.randint(0, ANCHO), 170, 60, 30) for _ in range(3)]
coches_calle1_der = [pygame.Rect(random.randint(0, ANCHO), 210, 60, 30) for _ in range(3)]
coches_calle2_izq = [pygame.Rect(random.randint(0, ANCHO), 370, 60, 30) for _ in range(3)]
coches_calle2_der = [pygame.Rect(random.randint(0, ANCHO), 410, 60, 30) for _ in range(3)]

# Velocidades
vel_izq = [random.randint(3, 5) for _ in range(6)]
vel_der = [random.randint(3, 5) for _ in range(6)]

# Mostrar mensaje
def mostrar_mensaje(texto):
    fuente = pygame.font.SysFont(None, 55)
    mensaje = fuente.render(texto, True, ROJO)
    rect = mensaje.get_rect(center=(ANCHO // 2, ALTO // 2))
    ventana.blit(mensaje, rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Dibujar casa
def dibujar_casa(x, y):
    pygame.draw.rect(ventana, MARRON, (x, y + 20, 100, 80))              # Pared
    pygame.draw.polygon(ventana, ROJO, [(x, y + 20), (x + 50, y), (x + 100, y + 20)])  # Techo
    pygame.draw.rect(ventana, NEGRO, (x + 40, y + 60, 20, 40))           # Puerta
    pygame.draw.rect(ventana, CELESTE, (x + 10, y + 40, 20, 20))         # Ventana 1
    pygame.draw.rect(ventana, CELESTE, (x + 70, y + 40, 20, 20))         # Ventana 2

# Dibujar las lineas de la calle 
def dibujar_lineas(calle_y):
    for i in range(0, ANCHO, 80):
        pygame.draw.rect(ventana, BLANCO, (i, calle_y, 40,5))

# Loop del juego
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento del pollito
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and pollito.left > 0:
        pollito.x -= 5
    if teclas[pygame.K_RIGHT] and pollito.right < ANCHO:
        pollito.x += 5
    if teclas[pygame.K_UP] and pollito.top > 0:
        pollito.y -= 5
    if teclas[pygame.K_DOWN] and pollito.bottom < ALTO:
        pollito.y += 5

    # Movimiento coches (izquierda)
    for i, coche in enumerate(coches_calle1_izq + coches_calle2_izq):
        coche.x -= vel_izq[i % len(vel_izq)]
        if coche.right < 0:
            coche.x = ANCHO

    # Movimiento coches (derecha)
    for i, coche in enumerate(coches_calle1_der + coches_calle2_der):
        coche.x += vel_der[i % len(vel_der)]
        if coche.left > ANCHO:
            coche.x = -60

    # Colisiones
    for coche in coches_calle1_izq + coches_calle1_der + coches_calle2_izq + coches_calle2_der:
        if pollito.colliderect(coche):
            vidas -= 1
            if vidas == 0:
                mostrar_mensaje("¡Te quedaste sin vidas!")
                vidas = 3
            else:
                    mostrar_mensaje(f"¡Cuidado! Te quedan {vidas} vidas")
                    pollito.x, pollito.y = 380, 540
                    break

    # ¿Ganó?
    if pollito.top <= 60:
        mostrar_mensaje("¡El pollito llegó a casa!")
        pollito.x, pollito.y = 380, 540

    # === DIBUJAR ESCENA ===
    ventana.fill(BLANCO)

    # Calles
    pygame.draw.rect(ventana, GRIS, (0, 160, ANCHO, 100))   # Calle 1
    pygame.draw.line(ventana, GRIS_CLARO, (0, 190), (ANCHO, 190), 4)
    dibujar_lineas(185)

    pygame.draw.rect(ventana, GRIS, (0, 360, ANCHO, 100))   # Calle 2
    pygame.draw.line(ventana, GRIS_CLARO, (0, 390), (ANCHO, 390), 4)
    dibujar_lineas(385)

    # Zona verde entre calles
    pygame.draw.rect(ventana, VERDE, (0, 260, ANCHO, 100))

    # Casas arriba 
    for x in range(100, 701, 150):
        dibujar_casa(x, 0)

    # Casas abajo
    for x in range(100, 701, 150):
        dibujar_casa(x, 500)

    # Pollito
    pygame.draw.ellipse(ventana, AMARILLO, pollito)

    # Coches
    for coche in coches_calle1_izq + coches_calle2_izq + coches_calle1_der + coches_calle2_der:
        pygame.draw.rect(ventana, AZUL, coche)
    
    # Dibujar vidas 
    fuente = pygame.font.SysFont(None, 30)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, NEGRO)
    ventana.blit(texto_vidas, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)