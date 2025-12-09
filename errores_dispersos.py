import numpy as np
import sys

class Colores:
    HEADER = '\033[95m'
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    ROJO = '\033[91m'
    NEGRITA = '\033[1m'
    RESET = '\033[0m'

def imprimir_matriz(titulo, M, color=Colores.RESET):
    print(f"\n{color}{Colores.NEGRITA}{titulo}:{Colores.RESET}")
    print(f"{color}┌{' '*25}┐")
    print(f"│ {M[0,0]:^10}   {M[0,1]:^10} │")
    print(f"│ {M[1,0]:^10}   {M[1,1]:^10} │")
    print(f"└{' '*25}┘{Colores.RESET}")

class DemoErroresDispersos:
    def __init__(self):
        self.U = np.array([[1, 1], [1, 0]], dtype=int)
        self.M0 = np.eye(2, dtype=int)
        self.n = 7 
        
        U_pow = np.linalg.matrix_power(self.U, self.n)
        self.Mn = np.dot(U_pow, self.M0)
        self.det_Mn = int(round(np.linalg.det(self.Mn)))
        
        tr = np.trace(self.U)
        det = int(round(np.linalg.det(self.U)))
        self.phi = (tr + np.sqrt(tr**2 - 4*det)) / 2

    def generar_caso(self):
        print(f"\n{Colores.HEADER}" + "="*60)
        print(" 🚑 SIMULACIÓN: ERRORES DISPERSOS (DISTINTAS FILAS) 🚑")
        print("="*60 + f"{Colores.RESET}")

        P = np.array([[10, 20], [30, 40]])
        det_P = int(round(np.linalg.det(P)))
        
        C = np.dot(P, self.Mn)
        
        print(f"{Colores.AZUL}[EMISOR]{Colores.RESET} Enviando paquete...")
        imprimir_matriz("Matriz Original", C, Colores.VERDE)
        print(f"   Checksum (Det P): {det_P}")
        print(f"   Ratio Unimodular (φ) esperado: {self.phi:.5f}")
        
        return C, det_P

    def ataque_disperso(self, C):
        print(f"\n{Colores.ROJO}" + "-"*60)
        print(" [SABOTAJE] DESTRUCCIÓN DE DIAGONAL")
        print("-"*60 + f"{Colores.RESET}")
        
        C_bad = C.copy()

        C_bad[0,0] = 999
        C_bad[1,1] = 111
        
        imprimir_matriz("Matriz Recibida (Dañada)", C_bad, Colores.ROJO)
        return C_bad

    def reparar_filas(self, C_bad, det_P):
        print(f"\n{Colores.AZUL}" + "="*60)
        print(" 🕵️  FASE DE RECUPERACIÓN INTELIGENTE")
        print("="*60 + f"{Colores.RESET}")
        
        C_fixed = C_bad.copy()
        det_total_esperado = det_P * self.det_Mn

        print(f"\n{Colores.AMARILLO}--- PASO 1: Estimación Aproximada con φ ---{Colores.RESET}")

        c01 = C_bad[0,1]
        est_c00 = c01 * self.phi
        val_c00 = int(round(est_c00))
        print(f"   Fila 1: {c01} * φ ≈ {est_c00:.4f} -> Estimado: {val_c00}")

        c10 = C_bad[1,0]
        est_c11 = c10 / self.phi
        val_c11 = int(round(est_c11))
        print(f"   Fila 2: {c10} / φ ≈ {est_c11:.4f} -> Estimado: {val_c11}")

        C_fixed[0,0] = val_c00
        C_fixed[1,1] = val_c11

        print(f"\n{Colores.AMARILLO}--- PASO 2: Verificación de Checksum y Pulido ---{Colores.RESET}")
        
        det_actual = int(round(np.linalg.det(C_fixed)))
        print(f"   Det Esperado: {det_total_esperado}")
        print(f"   Det Actual:   {det_actual}")
        
        if det_actual == det_total_esperado:
            print(f"   ✅ ¡Perfecto a la primera!")
            imprimir_matriz("Matriz Restaurada", C_fixed, Colores.VERDE)
            return
            
        print(f"   ⚠️ Desviación detectada (Culpable: precisión decimal). Iniciando escaneo de vecinos...")
        encontrado = False
        
        rango = [-1, 0, 1]
        
        for d1 in rango:
            for d2 in rango:
                cand_00 = val_c00 + d1
                cand_11 = val_c11 + d2
                det_test = (cand_00 * cand_11) - (c01 * c10)
                
                if det_test == det_total_esperado:
                    print(f"\n   🔧 {Colores.VERDE}AJUSTE ENCONTRADO:{Colores.RESET}")
                    print(f"      Fila 1 corregida: {val_c00} -> {cand_00} (Desplazamiento {d1})")
                    print(f"      Fila 2 corregida: {val_c11} -> {cand_11} (Desplazamiento {d2})")
                    
                    C_fixed[0,0] = cand_00
                    C_fixed[1,1] = cand_11
                    encontrado = True
                    break
            if encontrado: break
            
        if encontrado:
            imprimir_matriz("Matriz Restaurada con Éxito", C_fixed, Colores.VERDE)
        else:
            print(f"\n{Colores.ROJO}❌ Error grave: No se pudo cuadrar el determinante ni con ajuste fino.{Colores.RESET}")
            print("Intenta aumentar la potencia 'n' en la configuración.")

if __name__ == "__main__":
    app = DemoErroresDispersos()
    C, det = app.generar_caso()
    
    input(f"\n{Colores.NEGRITA}[ENTER para disparar]{Colores.RESET}")
    C_bad = app.ataque_disperso(C)
    
    input(f"\n{Colores.NEGRITA}[ENTER para recuperar]{Colores.RESET}")
    app.reparar_filas(C_bad, det)