import numpy as np
import sys
import time

class Colores:
    HEADER = '\033[95m'
    AZUL = '\033[94m'
    CYAN = '\033[96m'
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

class DetectiveColumna:
    def __init__(self):
        self.U = np.array([[1, 1], [1, 0]], dtype=int)
        self.M0 = np.eye(2, dtype=int)
        self.n = 8 
        U_pow = np.linalg.matrix_power(self.U, self.n)
        self.Mn = np.dot(U_pow, self.M0)
        self.det_Mn = int(round(np.linalg.det(self.Mn)))

        tr = np.trace(self.U)
        det = int(round(np.linalg.det(self.U)))
        self.phi = (tr + np.sqrt(tr**2 - 4*det)) / 2

    def generar_caso(self):
        print(f"\n{Colores.HEADER}" + "="*60)
        print(" 🏛️  SIMULACIÓN: PROTOCOLO COMPLETO DE ENVÍO  🏛️")
        print("="*60 + f"{Colores.RESET}")

        P = np.array([[65, 66],  
                      [67, 68]]) 
        det_P = int(round(np.linalg.det(P)))

        C = np.dot(P, self.Mn)

        ratio_columna = C[1,0] / C[0,0]
        
        print(f"\n{Colores.AZUL}[FASE 1] EL EMISOR PREPARA EL ENVÍO{Colores.RESET}")
        print("   Texto Plano original: 'ABCD'")

        print(f"\n   {Colores.AMARILLO}📦 PAQUETE QUE SE ENVÍA POR LA RED:{Colores.RESET}")
        print(f"   {Colores.AMARILLO}{Colores.RESET}")
        print(f"   {Colores.AMARILLO} 1. DATA (Matriz C):{Colores.RESET}")
        print(f"   {Colores.AMARILLO}    [[{C[0,0]:^6}, {C[0,1]:^6}],{Colores.RESET}")
        print(f"   {Colores.AMARILLO}     [{C[1,0]:^6}, {C[1,1]:^6}]]{Colores.RESET}")
        print(f"   {Colores.AMARILLO}{Colores.RESET}")
        print(f"   {Colores.AMARILLO} 2. METADATO A (Checksum det(P)): {det_P:<23}{Colores.RESET}")
        print(f"   {Colores.AMARILLO} 3. METADATO B (Ratio Col): {ratio_columna:<22.5f}{Colores.RESET}")
        
        return C, det_P, ratio_columna

    def ataque_doble(self, C):
        print(f"\n{Colores.ROJO}" + "-"*60)
        print(" [FASE 2] INTERCEPCIÓN Y SABOTAJE (ATAQUE DE FILA)")
        print("-"*60 + f"{Colores.RESET}")
        
        C_bad = C.copy()
  
        C_bad[0,0] = 12345  
        C_bad[0,1] = 9876   
        print("\nValores de la Fila 1 reales: 3596, 2223")
        imprimir_matriz("El Hacker destruye la Fila 1 completa", C_bad, Colores.ROJO)
        return C_bad

    def resolver_ambiguedad(self, C_bad, det_P, ratio_col_esperado):
        print(f"\n{Colores.AZUL}" + "="*60)
        print(" [FASE 3] RECEPCIÓN Y RECUPERACIÓN")
        print("="*60 + f"{Colores.RESET}")
        
        det_total = det_P * self.det_Mn
        
        print(f"\n🔧 Herramientas disponibles del paquete:")
        print(f"   - Matriz Dañada")
        print(f"   - Checksum recibido: {det_P}")
        print(f"   - Ratio Columna recibido: {Colores.CYAN}{ratio_col_esperado:.5f}{Colores.RESET}")
        
        c21 = C_bad[1, 0]
        c22 = C_bad[1, 1]
        
        print(f"\n🔍 Buscando candidatos para la Fila 1 [x, y]...")
        
        x_estimado = c21 / ratio_col_esperado
        centro = int(x_estimado)
        candidatos = []
        
        for x in range(centro - 5000, centro + 5000):

            num = (x * c22) - det_total
            if c21 != 0 and num % c21 == 0:
                y = num // c21
                candidatos.append((x, y))
        
        print(f"\n{Colores.AMARILLO}⚠️  AMBIGÜEDAD: Hay {len(candidatos)} parejas que cumplen el Determinante.{Colores.RESET}")
        print(f"   (Mostrando muestra representativa)")
        
        print(f"\n{'x':^10} | {'y':^10} | {'Ratio Columna Calc':^20} | {'Veredicto'}")
        print("-" * 65)
        
        mejor_candidato = None
        idx_centro = len(candidatos) // 2
        
        for i, (x, y) in enumerate(candidatos):

            ratio_calc = c21 / x if x != 0 else 0
            diff = abs(ratio_calc - ratio_col_esperado)
            
            estado = ""
            if diff < 0.0001:
                estado = f"{Colores.VERDE}✅ MATCH EXACTO{Colores.RESET}"
                mejor_candidato = (x, y)
            elif diff < 0.1:
                estado = f"{Colores.ROJO}❌ FALSO POSITIVO{Colores.RESET}"
            
            # Mostrar solo algunos
            if abs(i - idx_centro) < 3:
                print(f"{x:^10} | {y:^10} | {ratio_calc:^20.5f} | {estado}")

        if mejor_candidato:
            print(f"\n{Colores.VERDE}🏆 RECUPERACIÓN EXITOSA{Colores.RESET}")
            print(f"   Usando el Ratio Columna ({ratio_col_esperado:.5f}),")
            print(f"   hemos filtrado los candidatos falsos.")
            
            C_final = C_bad.copy()
            C_final[0,0] = mejor_candidato[0]
            C_final[0,1] = mejor_candidato[1]
            imprimir_matriz("Matriz Restaurada", C_final, Colores.VERDE)

if __name__ == "__main__":
    app = DetectiveColumna()
    C, det, ratio = app.generar_caso()
    input(f"\n{Colores.NEGRITA}[ENTER para enviar y sabotear]{Colores.RESET}")
    C_bad = app.ataque_doble(C)
    input(f"\n{Colores.NEGRITA}[ENTER para recuperar]{Colores.RESET}")
    app.resolver_ambiguedad(C_bad, det, ratio)