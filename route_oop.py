import heapq
import math
from colorama import init, Fore, Style

# Inicializar colorama
init()

class Mapa:
    def __init__(self, tamano):
        # Inicializar la matriz de tamaño especificado llena de puntos
        self.tamano = tamano
        self.matriz = [["[]" for _ in range(tamano)] for _ in range(tamano)]
    
    def agregar_obstaculo(self, fila, columna):
        # Agregar un obstáculo en la posición especificada
        self.matriz[fila][columna] = "#"
    
    def quitar_obstaculo(self, fila, columna):
        # Quitar un obstáculo de la posición especificada
        self.matriz[fila][columna] = "[]"
    
    def es_accesible(self, fila, columna):
        # Verificar si la celda es accesible y está dentro de los límites de la matriz
        return 0 <= fila < self.tamano and 0 <= columna < self.tamano and self.matriz[fila][columna] == "[]"
    
    def imprimir(self):
        # Imprimir los números de columna
        encabezado_columnas = "  " + " ".join(str(i) for i in range(self.tamano))
        print(encabezado_columnas)
        
        # Imprimir la matriz con los números de fila y colores
        for indice, fila in enumerate(self.matriz):
            print(f"{indice} ", end="")
            for elemento in fila:
                if elemento == "#":
                    print(Fore.RED + elemento + Style.RESET_ALL, end=" ")
                elif elemento == "I":
                    print(Fore.GREEN + elemento + Style.RESET_ALL, end=" ")
                elif elemento == "F":
                    print(Fore.BLUE + elemento + Style.RESET_ALL, end=" ")
                elif elemento == "*":
                    print(Fore.YELLOW + elemento + Style.RESET_ALL, end=" ")
                else:
                    print(elemento, end=" ")
            print()

    def solicitar_obstaculos(self):
        # Solicitar al usuario que ingrese los obstáculos
        while True:
            accion = input("Ingrese 'a' para agregar un obstáculo, 'r' para quitar un obstáculo, o presione Enter para terminar: ")
            if accion == "":
                break
            posicion = input("Ingrese la posición del obstáculo (fila,columna): ")
            fila, columna = map(int, posicion.split(","))
            if accion == 'a':
                self.agregar_obstaculo(fila, columna)
            elif accion == 'r':
                self.quitar_obstaculo(fila, columna)
            self.imprimir()
    
    def solicitar_punto(self, mensaje, simbolo):
        # Solicitar al usuario que ingrese el punto de inicio o final
        while True:
            punto = input(f"Ingrese la posición del {mensaje} (fila,columna): ")
            fila, columna = map(int, punto.split(","))
            if self.es_accesible(fila, columna):
                self.matriz[fila][columna] = simbolo
                self.imprimir()
                return fila, columna
            else:
                print("La posición está ocupada, elija otra.")

class CalculadoraRutas:
    def __init__(self, mapa):
        # Inicializar con el mapa proporcionado
        self.mapa = mapa
    
    def heuristica(self, a, b):
        # Calcular la distancia euclidiana entre dos puntos
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    
    def a_estrella(self, inicio, fin):
        tamano = self.mapa.tamano
        # Movimientos en las ocho direcciones posibles (incluyendo diagonales)
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        # Inicializar la lista de nodos a explorar
        open_set = []
        heapq.heappush(open_set, (0, inicio))
        # Diccionario para almacenar nodos y sus padres
        came_from = {}
        # Inicializar g_score y f_score con el punto de inicio
        g_score = {inicio: 0}
        f_score = {inicio: self.heuristica(inicio, fin)}
        
        while open_set:
            # Tomar el nodo con el menor f_score
            _, current = heapq.heappop(open_set)
            
            if current == fin:
                # Reconstruir el camino
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(inicio)  # Agregar el inicio al final del camino
                return path[::-1]  # Retornar el camino ya ordenado
            
            # Explorar los vecinos
            for movimiento in movimientos:
                vecino = (current[0] + movimiento[0], current[1] + movimiento[1])
                # Verificar que el vecino esté dentro de la matriz y no sea un obstáculo
                if self.mapa.es_accesible(vecino[0], vecino[1]) or vecino == fin:
                    tent_g_score = g_score[current] + self.heuristica(current, vecino)
                    
                    if vecino not in g_score or tent_g_score < g_score[vecino]:
                        came_from[vecino] = current
                        g_score[vecino] = tent_g_score
                        f_score[vecino] = tent_g_score + self.heuristica(vecino, fin)
                        if vecino not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (f_score[vecino], vecino))
        
        return []
    
    def mostrar_ruta(self, ruta):
        # Marcar la ruta en la matriz con asteriscos
        for paso in ruta:
            if self.mapa.matriz[paso[0]][paso[1]] == "[]":
                self.mapa.matriz[paso[0]][paso[1]] = "*"
        self.mapa.imprimir()

def main():
    # Solicitar al usuario que ingrese el tamaño de la matriz
    tamano = int(input("Ingrese el tamaño de la matriz: "))
    
    # Crear la matriz
    mapa = Mapa(tamano)
    mapa.imprimir()
    
    # Solicitar obstáculos
    mapa.solicitar_obstaculos()
    
    # Solicitar punto de inicio
    inicio = mapa.solicitar_punto("punto de inicio (I)", "I")
    
    # Solicitar punto final
    fin = mapa.solicitar_punto("punto final (F)", "F")
    
    # Buscar la ruta más corta con A*
    calculadora = CalculadoraRutas(mapa)
    ruta = calculadora.a_estrella(inicio, fin)
    
    if ruta:
        # Mostrar la ruta en la matriz
        calculadora.mostrar_ruta(ruta)
    else:
        print("No se encontró una ruta.")

if __name__ == "__main__":
    main()
