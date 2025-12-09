import numpy as np
import sys

np.set_printoptions(suppress=True, precision=5, linewidth=100)

class ComparativaEstabilidad:
    def __init__(self):
        pass
        
    def ejecutar_comparativa(self):
        print("\n" + "="*70)
        print(" 🧪 COMPARATIVA: ¿QUIÉN TIENE LA CULPA DE LAS FRACCIONES?")
        print("="*70)

        print("\n" + "-"*70)
        print("🟢 CASO 1: U Unimodular | M0 con Determinante 2")
        print("   Hipótesis: Las fracciones aparecerán, pero SERÁN ESTABLES.")
        print("-"*70)
 
        U_bien = np.array([[1, 1], [1, 0]], dtype=int)

        M0_sucia = np.array([[2, 0], [0, 1]], dtype=int)
        
        print(f"   Matriz U (Det={int(np.linalg.det(U_bien))}):\n{U_bien}")
        print(f"   Matriz M0 (Det={int(np.linalg.det(M0_sucia))}):\n{M0_sucia}")
        print("\n   --- EVOLUCIÓN AL AUMENTAR LA POTENCIA 'n' ---")
        
        potencias = [1, 5, 10, 20]
        
        for n in potencias:

            Mn = np.dot(np.linalg.matrix_power(U_bien, n), M0_sucia)
            det_Mn = np.linalg.det(Mn)
            Mn_inv = np.linalg.inv(Mn)

            valor_muestra = Mn_inv[0, 0] 
            
            print(f"   [n={n:02d}] Det(Mn) = {det_Mn:4.0f}  ->  Fracción típica: {abs(valor_muestra):.5f}")

        print("\n   ✅ CONCLUSIÓN CASO 1: El determinante oscila (2, -2) pero NO CRECE.")
        print("      Las fracciones son siempre manejables (tipo 0.5).")

        print("\n" + "-"*70)
        print("🔴 CASO 2: U NO Unimodular (Det 2) | M0 Limpia")
        print("   Hipótesis: El determinante explotará y las fracciones serán microscópicas.")
        print("-"*70)
        

        U_mal = np.array([[2, 0], [0, 1]], dtype=int)

        M0_limpia = np.eye(2, dtype=int)
        
        print(f"   Matriz U (Det={int(np.linalg.det(U_mal))}):\n{U_mal}")
        print("\n   --- EVOLUCIÓN AL AUMENTAR LA POTENCIA 'n' ---")
        
        for n in potencias:
            Mn = np.dot(np.linalg.matrix_power(U_mal, n), M0_limpia)
            det_Mn = np.linalg.det(Mn)
            Mn_inv = np.linalg.inv(Mn)
            
            valor_muestra = Mn_inv[0, 0]

            print(f"   [n={n:02d}] Det(Mn) = {det_Mn:12.0f} -> Fracción típica: {valor_muestra:.10f}")

        print("\n   ❌ CONCLUSIÓN CASO 2: El determinante crece exponencialmente (2^n).")
        print("      Con n=20, ¡estamos dividiendo por un millón! (0.0000009537)")
        print("      Esto destruye la aritmética.")

if __name__ == "__main__":
    Demo = ComparativaEstabilidad()
    Demo.ejecutar_comparativa()