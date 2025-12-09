import numpy as np
import sys


np.set_printoptions(suppress=True, precision=4, linewidth=100)

class CriptoUnimodular:
    def __init__(self):
        self.U = None
        self.M0 = None
        self.Mn = None
        self.Mn_inv = None
        self.n = 0
        self.mu = 0
        
    def configurar_sistema(self):
        print("\n" + "="*60)
        print("  CONFIGURACIÓN DEL SISTEMA (M0 GENERALIZADA)")
        print("="*60)

        print("\n[PASO 1] Definir Matriz U (Debe ser Unimodular) -> det(U) = +-1")
        
        print("Guía visual de posiciones:")
        print("┌             ┐")
        print("│  u11   u12  │")
        print("│  u21   u22  │")
        print("└             ┘")
        while True:
            try:
                print("Introduce los valores de U:")
                u11 = int(input("   u11: "))
                u12 = int(input("   u12: "))
                u21 = int(input("   u21: "))
                u22 = int(input("   u22: "))
                
                U_temp = np.array([[u11, u12], [u21, u22]], dtype=int)
                det_U = int(round(np.linalg.det(U_temp)))
                
                print(f"   -> Determinante(U) = {det_U}")
                
                if abs(det_U) != 1:
                    print(f"   ❌ ERROR: U debe ser estrictamente unimodular (+-1).")
                else:
                    self.U = U_temp
                    print("   ✅ Matriz U aceptada.")
                    break
            except ValueError:
                print("   ❌ Error: Introduce números enteros.")

        print("\n" + "-"*60)
        print("[PASO 2] Definir Semilla M0")
        print("Introduce la 2ª Columna. La 1ª se calculará: Col1 = U * Col2")
        
        while True:
            try:

                val_sup = int(input("\nIntroduce valor superior inicial (m12): "))
                val_inf = int(input("Introduce valor inferior inicial (m22): "))

                col2 = np.array([[val_sup], [val_inf]])
                col1 = np.dot(self.U, col2)
                M0_temp = np.hstack((col1, col2))

                self.mu = int(round(np.linalg.det(M0_temp)))
                
                print(f"\n   -> Matriz M0 resultante:\n{M0_temp}")
                print(f"   -> Determinante mu = {self.mu}")
                
                if self.mu == 0:
                    print("   ❌ ERROR CRÍTICO: El determinante es 0. La matriz no tiene inversa.")
                    print("      Prueba con otros valores.")
                    continue
                
                if abs(self.mu) != 1:
                    print(f"   ⚠️ AVISO: M0 no es unimodular (mu={self.mu}).")
                    print("      El sistema funcionará usando aritmética de punto flotante (decimales).")
                else:
                    print("   ✅ M0 es unimodular. Cifrado ideal en enteros.")
                
                self.M0 = M0_temp
                break
                
            except ValueError:
                print("Error de entrada.")

        print("\n" + "-"*60)
        print("[PASO 3] Generar Clave Secreta Mn")
        self.n = int(input("Introduce la potencia secreta n: "))
        
        # Mn = U^n * M0
        U_pow = np.linalg.matrix_power(self.U, self.n)
        self.Mn = np.dot(U_pow, self.M0)

        self.Mn_inv = np.linalg.inv(self.Mn)
        
        det_Mn = np.linalg.det(self.Mn)
        
        print(f"\n🔑 CLAVE FINAL (Mn):\n{self.Mn}")
        print(f"   Determinante(Mn) = {det_Mn:.2f} (Debería ser +/- {abs(self.mu)})")
        print(f"   Inversa Mn^(-1) [Para descifrar]:\n{self.Mn_inv}")


    def cifrar(self, texto):
        print("\n" + "="*60)
        print("  INICIANDO CIFRADO (C = P * Mn)")
        print("="*60)

        numeros = [ord(c) for c in texto]
        while len(numeros) % 4 != 0:
            numeros.append(32)
            
        bloques_P = []
        for i in range(0, len(numeros), 4):
            bloques_P.append(np.array(numeros[i:i+4]).reshape(2, 2))
            
        bloques_C = []
        print(f"Texto '{texto}' convertido en {len(bloques_P)} matrices.\n")
        
        for i, P in enumerate(bloques_P):
            C = np.dot(P, self.Mn)
            bloques_C.append(C)
            
            print(f"--- Bloque {i+1} ---")
            print(f"P (Texto):\n{P}")
            print(f"C (Cifrado):\n{C}\n")
            
        return bloques_C

    def descifrar(self, bloques_C):
        print("\n" + "="*60)
        print("  INICIANDO DESCIFRADO (P = C * Mn^(-1))")
        print("="*60)
        
        texto_final = ""
        
        for i, C in enumerate(bloques_C):

            P_float = np.dot(C, self.Mn_inv)

            P_int = np.round(P_float).astype(int)
            
            print(f"--- Bloque {i+1} ---")
            print(f"C (Cifrado):\n{C}")
            print(f"Resultado Raw (Float):\n{P_float}")
            print(f"Redondeado (Entero P):\n{P_int}\n")
            
            for num in P_int.flatten():
                texto_final += chr(int(num))
                
        return texto_final

if __name__ == "__main__":
    sistema = CriptoUnimodular()

    sistema.configurar_sistema()

    print("\n" + "-"*60)
    msg = input("Introduce mensaje a cifrar: ")

    cifrado = sistema.cifrar(msg)
    descifrado = sistema.descifrar(cifrado)
    
    print("="*60)
    print("  RESULTADO FINAL")
    print("="*60)
    print(f"Original:   {msg}")
    print(f"Descifrado: {descifrado}")