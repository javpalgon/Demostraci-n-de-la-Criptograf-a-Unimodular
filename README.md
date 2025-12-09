# Criptografía Unimodular y Corrección de Errores

> **Implementación práctica, análisis de seguridad y simulaciones de recuperación de errores basadas en el paper: *"From golden to unimodular cryptography" (Koshkin & Styers, 2017).*_**

![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Numpy](https://img.shields.io/badge/Library-NumPy-green.svg) ![Status](https://img.shields.io/badge/Status-Academic%20Project-orange.svg)

## Descripción

Este repositorio contiene una suite de herramientas desarrolladas en Python para demostrar la evolución de la **Criptografía Golden** (basada en Fibonacci) hacia la **Criptografía Unimodular Generalizada**.

El proyecto explora cómo el uso de matrices unimodulares arbitrarias aumenta el espacio de claves y la seguridad frente a ataques de texto plano, conservando al mismo tiempo la capacidad de **autocorrección de errores** mediante propiedades matemáticas intrínsecas como la **Razón Unimodular ($\varphi$)** y el **Ratio de Columna**.

## Características Principales

* **Generador de Claves Unimodulares:** Algoritmos para crear matrices $U$ y semillas $M_0$ con determinante $\pm 1$.
* **Cifrado/Descifrado Robusto:** Implementación del sistema $M_n = U^n M_0$ con aritmética matricial.
* **Simulador de Ataques:** Scripts interactivos que permiten al usuario corromper datos cifrados para probar la resistencia del sistema.
* **Corrección de Errores:**
    * Detección mediante **Determinante (Checksum)**.
    * Localización mediante convergencia a la **Razón Unimodular ($\varphi$)**.
    * Resolución de ambigüedades en errores de fila mediante el **Ratio de Columna**.
* **Visualización en Consola:** Interfaces de línea de comandos (CLI) con colores y formato visual para demostraciones en tiempo real.

## Estructura del Repositorio

### 1. Núcleo Criptográfico
* `cifrado-descifrado.py`: Implementación completa del sistema. Permite configurar matrices $U$ y $M_0$ manualmente, realizar *padding* de texto, cifrar y descifrar mensajes.

### 2. Demos Interactivas (Modo Detective)
* `deteccion_errores.py`: **(Recomendado)** Simulador visual paso a paso. Muestra el proceso de emisión, interceptación (hacker), diagnóstico y reparación automática de errores simples.
* `ratio-columna.py`: Demostración avanzada para **Errores de Fila Completa**. Muestra cómo el sistema resuelve la ambigüedad matemática usando el metadato del *Ratio de Columna*.
* `errores_dispersos.py`: Simulación de la estrategia "Divide y Vencerás" para corregir múltiples errores en distintas filas.

### 3. Análisis Matemático y Forense
* `demostracion_fallo_unimodular.py`: Demostración de por qué la matriz generadora $U$ **debe** ser unimodular para evitar la explosión exponencial del determinante y la pérdida de precisión.

## Fundamento Teórico

El sistema se basa en la recurrencia lineal generada por una matriz unimodular $U$ ($\det U = \pm 1$).
A diferencia de Fibonacci (donde los cocientes convergen a $\tau \approx 1.618$), aquí convergen a la **Razón Unimodular generalizada**:

$$\varphi = \frac{\text{tr}(U) + \sqrt{\text{tr}(U)^2 - 4\det(U)}}{2}$$

El protocolo de seguridad implementado incluye el envío de un paquete con:
1.  Matriz Cifrada $C$.
2.  Determinante del mensaje original (Checksum).
3.  Ratio de Columna (para desempate en errores críticos).

## 🛠️ Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/criptografia-unimodular.git](https://github.com/tu-usuario/criptografia-unimodular.git)
    cd criptografia-unimodular
    ```

2.  **Instalar dependencias:**
    Este proyecto requiere `numpy` para el álgebra lineal.
    ```bash
    pip install numpy
    ```

3.  **Ejecutar una demostración:**
    ```bash
    python detective_visual_pro.py
    ```

## Referencia

* **Paper Original:** Sergiy Koshkin, Taylor Styers. *"From golden to unimodular cryptography"*. Chaos, Solitons and Fractals 105 (2017) 208–214.

## Autores

* **Javier Pallarés González** 
* **Darío Zafra Ruiz**
* **Guillermo Linares Borrego**
* **José María Silva Guzmán**

---
*Proyecto realizado para la asignatura de Criptografía - 2025*
