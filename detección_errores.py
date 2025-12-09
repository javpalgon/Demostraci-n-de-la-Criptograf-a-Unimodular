import numpy as np
import sys
import time

# Configuración de colores ANSI para consola
class Colores:
    HEADER = '\033[95m'
    AZUL = '\033[94m'
    CYAN = '\033[96m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    ROJO = '\033[91m'
    NEGRITA = '\033[1m'
    SUBRAYADO = '\033[4m'
    RESET = '\033[0m'

def imprimir_titulo(texto):
    print("\n" + Colores.HEADER + "="*60)
    print(f" {texto.center(58)} ")
    print("="*60 + Colores.RESET)

def imprimir_subtitulo(texto):
    print("\n" + Colores.CYAN + "-"*60)
    print(f" {texto}")
    print("-" * 60 + Colores.RESET)

def imprimir_matriz_bonita(titulo, M, color=Colores.RESET):
    """Imprime una matriz 2x2 con bordes ASCII y alineación perfecta"""
    print(f"\n{color}{Colores.NEGRITA}{titulo}:{Colores.RESET}")
    print(f"{color}┌{' '*25}┐")
    print(f"│ {M[0,0]:^10}   {M[0,1]:^10} │")
    print(f"│ {M[1,0]:^10}   {M[1,1]:^10} │")
    print(f"└{' '*25}┘{Colores.RESET}")

class DetectiveVisual:
    def __init__(self):
        # Configuración por defecto (Fibonacci) para la demo visual
        self.U = np.array([[1, 1], [1, 0]], dtype=int)
        self.n = 6 # Potencia suficiente para números interesantes
        
        # Generar Clave
        U_pow = np.linalg.matrix_power(self.U, self.n)
        self.M0 = np.eye(2, dtype=int)
        self.Mn = np.dot(U_pow, self.M0)
        self.det_Mn = int(round(np.linalg.det(self.Mn)))
        
        # Calcular Phi
        tr = np.trace(self.U)
        det = int(round(np.linalg.det(self.U)))
        self.phi = (tr + np.sqrt(tr**2 - 4*det)) / 2

    def inicio(self):
        imprimir_titulo("🕵️ SIMULADOR DE DETECCIÓN DE ERRORES 🕵️")
        print(f"{Colores.AZUL}Configuración del Sistema:{Colores.RESET}")
        print(f" > Matriz Base: Fibonacci")
        print(f" > Potencia (n): {self.n}")
        print(f" > Ratio Unimodular Esperado (φ): {Colores.VERDE}{self.phi:.5f}{Colores.RESET}")
        print(f" > Determinante Clave: {self.det_Mn}")

    def generar_envio(self):
        imprimir_subtitulo("1️⃣  FASE DE EMISIÓN (El Mensaje Original)")
        
        # Mensaje predefinido para la demo
        texto = "HOLA"
        nums = [ord(c) for c in texto]
        P = np.array(nums[:4]).reshape(2, 2)
        det_P = int(round(np.linalg.det(P)))
        
        imprimir_matriz_bonita("Matriz de Texto Plano (P)", P, Colores.VERDE)
        print(f"\n📦 {Colores.NEGRITA}METADATOS ADJUNTOS:{Colores.RESET}")
        print(f"   [CHECKSUM] Determinante Original = {Colores.AMARILLO}{det_P}{Colores.RESET}")
        
        # Cifrar
        C = np.dot(P, self.Mn)
        imprimir_matriz_bonita("Matriz Cifrada (C)", C, Colores.AZUL)
        
        return C, det_P

    def sabotaje(self, C):
        imprimir_subtitulo("2️⃣  FASE DE INTERCEPCIÓN (El Hacker)")
        print(f"{Colores.ROJO}😈 ¡ALERTA! Un hacker ha interceptado el paquete...{Colores.RESET}")
        
        C_bad = C.copy()
        original = C[0,0]
        
        print("\nEl hacker decide destruir el primer valor (Arriba-Izquierda).")
        print(f"Valor Original: {original}")
        nuevo_val = input(f"{Colores.ROJO}Introduce un número falso para romper el mensaje: {Colores.RESET}")
        
        try:
            nuevo_val = int(nuevo_val)
        except:
            nuevo_val = 0
            
        C_bad[0,0] = nuevo_val
        
        imprimir_matriz_bonita("Matriz Corrupta que viaja por la red", C_bad, Colores.ROJO)
        return C_bad

    def diagnostico(self, C_recibida, det_P):
        imprimir_subtitulo("3️⃣  FASE DE RECEPCIÓN Y DIAGNÓSTICO")
        
        # --- TEST 1: DETERMINANTE ---
        det_esperado = det_P * self.det_Mn
        det_recibido = int(round(np.linalg.det(C_recibida)))
        
        print(f"\n{Colores.NEGRITA}--- [TEST A] INTEGRIDAD GLOBAL (Determinante) ---{Colores.RESET}")
        print(f"Calculado: {det_recibido:>10}")
        print(f"Esperado:  {det_esperado:>10}")
        
        if det_recibido != det_esperado:
            print(f"Resultado: {Colores.ROJO}🚨 FALLO DETECTADO{Colores.RESET}")
        else:
            print(f"Resultado: {Colores.VERDE}✅ OK{Colores.RESET}")
            return # Fin si todo está bien

        # --- TEST 2: RATIO UNIMODULAR ---
        print(f"\n{Colores.NEGRITA}--- [TEST B] ESCÁNER DE FILAS (Ratio φ) ---{Colores.RESET}")
        print(f"Objetivo: Converger a {self.phi:.4f}")
        print("-" * 50)
        print(f"{'Fila':^10} | {'Ratio Calc':^15} | {'Diferencia':^15} | {'Estado'}")
        print("-" * 50)

        # Fila 1
        r1 = C_recibida[0,0] / C_recibida[0,1]
        diff1 = abs(r1 - self.phi)
        estado1 = f"{Colores.ROJO}SOSPECHOSA{Colores.RESET}" if diff1 > 0.1 else f"{Colores.VERDE}OK{Colores.RESET}"
        print(f"{'1':^10} | {r1:^15.4f} | {diff1:^15.4f} | {estado1}")

        # Fila 2
        r2 = C_recibida[1,0] / C_recibida[1,1]
        diff2 = abs(r2 - self.phi)
        estado2 = f"{Colores.ROJO}SOSPECHOSA{Colores.RESET}" if diff2 > 0.1 else f"{Colores.VERDE}OK{Colores.RESET}"
        print(f"{'2':^10} | {r2:^15.4f} | {diff2:^15.4f} | {estado2}")
        print("-" * 50)
        
        # Devolver fila mala (0 o 1)
        return 0 if diff1 > diff2 else 1

    def reparacion(self, C_recibida, fila_mala, det_P):
        imprimir_subtitulo("4️⃣  FASE DE RECUPERACIÓN MATEMÁTICA")
        
        det_total = det_P * self.det_Mn
        
        # Variables para la ecuación
        c12 = C_recibida[0, 1]
        c21 = C_recibida[1, 0]
        c22 = C_recibida[1, 1]
        
        print(f"{Colores.AMARILLO}🔧 Iniciando protocolo de reparación en Fila {fila_mala+1}...{Colores.RESET}")
        print(f"   Usando ecuación del Determinante:")
        print(f"   (x * {c22}) - ({c12} * {c21}) = {det_total}")
        
        # Despeje: x = (Det + c12*c21) / c22
        numerador = det_total + (c12 * c21)
        recuperado = numerador / c22 if fila_mala == 0 else 0 # Simplificado para demo fila 1
        
        # Calculo real para Fila 1 Col 1
        x_real = (det_total + (C_recibida[0,1] * C_recibida[1,0])) / C_recibida[1,1]
        
        print(f"\n   🧮 Calculando valor perdido...")
        time.sleep(1) # Pequeña pausa dramática
        
        print(f"\n   💎 VALOR RECUPERADO: {Colores.VERDE}{Colores.NEGRITA}{int(round(x_real))}{Colores.RESET}")
        
        C_final = C_recibida.copy()
        C_final[0,0] = int(round(x_real))
        
        imprimir_matriz_bonita("Matriz Reparada", C_final, Colores.VERDE)

if __name__ == "__main__":
    app = DetectiveVisual()
    app.inicio()
    
    # Paso 1: Generar
    input(f"\n{Colores.NEGRITA}[Presiona ENTER para generar el mensaje]{Colores.RESET}")
    C, det_P = app.generar_envio()
    
    # Paso 2: Sabotear
    input(f"\n{Colores.NEGRITA}[Presiona ENTER para interceptar el envío]{Colores.RESET}")
    C_bad = app.sabotaje(C)
    
    # Paso 3: Diagnosticar
    input(f"\n{Colores.NEGRITA}[Presiona ENTER para iniciar diagnóstico]{Colores.RESET}")
    fila_mala = app.diagnostico(C_bad, det_P)
    
    # Paso 4: Reparar
    input(f"\n{Colores.NEGRITA}[Presiona ENTER para intentar reparar]{Colores.RESET}")
    app.reparacion(C_bad, fila_mala, det_P)
    
    imprimir_titulo("¡CASO CERRADO!")