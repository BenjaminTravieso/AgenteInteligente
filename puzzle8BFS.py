import pygame
import time
import random
from collections import deque

# Configuración de pantalla
ANCHO, ALTO = 300, 400
TAMANO_CASILLA = 100
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 150, 255)

# Estado meta acordado
estado_meta = [[1, 2, 3],  
               [8, 0, 4],  
               [7, 6, 5]]

# Funciones del puzzle
def contar_inversiones(estado):
    numeros = [num for fila in estado for num in fila if num != 0]
    return sum(1 for i in range(len(numeros)) for j in range(i + 1, len(numeros)) if numeros[i] > numeros[j])

def es_resoluble(estado):
    return contar_inversiones(estado) % 2 == contar_inversiones(estado_meta) % 2

def generar_estado_resoluble():
    while True:
        numeros = list(range(9))
        random.shuffle(numeros)
        estado_inicial = [numeros[i:i+3] for i in range(0, 9, 3)]
        if es_resoluble(estado_inicial):
            return estado_inicial

def encontrar_vacio(estado):
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                return i, j

def mover(estado, i, j, direccion):
    nuevo_estado = [fila[:] for fila in estado]
    if direccion == "arriba" and i > 0:
        nuevo_estado[i][j], nuevo_estado[i-1][j] = nuevo_estado[i-1][j], nuevo_estado[i][j]
    elif direccion == "abajo" and i < 2:
        nuevo_estado[i][j], nuevo_estado[i+1][j] = nuevo_estado[i+1][j], nuevo_estado[i][j]
    elif direccion == "izquierda" and j > 0:
        nuevo_estado[i][j], nuevo_estado[i][j-1] = nuevo_estado[i][j-1], nuevo_estado[i][j]
    elif direccion == "derecha" and j < 2:
        nuevo_estado[i][j], nuevo_estado[i][j+1] = nuevo_estado[i][j+1], nuevo_estado[i][j]
    else:
        return None
    return nuevo_estado if nuevo_estado != estado else None

def generar_sucesores(estado):
    movimientos = ["arriba", "abajo", "izquierda", "derecha"]
    sucesores = []
    i, j = encontrar_vacio(estado)
    for mov in movimientos:
        nuevo_estado = mover(estado, i, j, mov)
        if nuevo_estado:
            sucesores.append((mov, nuevo_estado))
    return sucesores

def bfs(estado_inicial):
    tiempo_inicio = time.time()
    cola = deque([(estado_inicial, [])])
    visitados = set()
    while cola:
        estado_actual, camino = cola.popleft()
        estado_tuple = tuple(map(tuple, estado_actual))
        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)
        if estado_actual == estado_meta:
            tiempo_final = time.time() - tiempo_inicio
            return camino, tiempo_final, len(camino)  
        for mov, nuevo_estado in generar_sucesores(estado_actual):
            cola.append((nuevo_estado, camino + [mov]))
    return None, 0, 0

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Puzzle 8 - Agente BFS")

estado_actual = generar_estado_resoluble()
solucion = None
tiempo_resolucion = 0  
contador_movimientos = 0  

def dibujar_tablero(estado, tiempo, movimientos):
    pantalla.fill(BLANCO)
    for i in range(3):
        for j in range(3):
            numero = estado[i][j]
            rect = pygame.Rect(j * TAMANO_CASILLA, i * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA)
            pygame.draw.rect(pantalla, AZUL if numero == 0 else NEGRO, rect)
            if numero != 0:
                fuente = pygame.font.Font(None, 50)
                texto = fuente.render(str(numero), True, BLANCO)
                pantalla.blit(texto, rect.move(30, 30))
    
    pygame.draw.rect(pantalla, NEGRO, (50, 310, 100, 40))  
    pygame.draw.rect(pantalla, NEGRO, (170, 310, 100, 40))  
    fuente = pygame.font.Font(None, 30)
    pantalla.blit(fuente.render("Empezar", True, BLANCO), (60, 320))
    pantalla.blit(fuente.render("Reiniciar", True, BLANCO), (180, 320))

    pantalla.blit(fuente.render(f"Tiempo: {tiempo:.2f} s", True, NEGRO), (90, 360))  
    pantalla.blit(fuente.render(f"Movimientos: {movimientos}", True, NEGRO), (90, 380))  

corriendo = True
movimiento_indice = 0

while corriendo:
    dibujar_tablero(estado_actual, tiempo_resolucion, contador_movimientos)
    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            if 50 <= x <= 170 and 310 <= y <= 350:  
                if not solucion:
                    solucion, tiempo_resolucion, contador_movimientos = bfs(estado_actual)
                    movimiento_indice = 0
            elif 170 <= x <= 290 and 310 <= y <= 350:  
                estado_actual = generar_estado_resoluble()
                solucion = None
                tiempo_resolucion = 0
                contador_movimientos = 0

    if solucion and movimiento_indice < len(solucion):
        estado_actual = mover(estado_actual, *encontrar_vacio(estado_actual), solucion[movimiento_indice])
        movimiento_indice += 1
        pygame.time.delay(500)

pygame.quit()