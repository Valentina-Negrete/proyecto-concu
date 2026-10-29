# Hito 1 — Concurrencia en CPU


**Objetivo:** demostrar dominio de hilos y sincronización.

## Enunciado

1. Problema con paralelismo de **datos** claro. Este esqueleto usa **suma de un vector grande** de `float` (el mismo *shape* que las Clases 2 y 4, y que el Hito 2). Pueden cambiar a multiplicación de vectores, conteo de palabras o una operación matricial simple: actualizá este README si lo hacen.
2. Versión **secuencial** (`secuencial.cpp`, ya completa) y versión **multi-hilo** (`paralelo.cpp`, esqueleto con `TODO`).
3. Al menos **una** primitiva de sincronización de la Clase 3 (`std::mutex`, variable de condición, o monitor). OpenMP es válido si lo justificás en el informe.
4. Medir aceleración \( S(T) = T_{\mathrm{seq}} / T(T) \) vs. número de hilos y comparar con la Ley de Amdahl, con una fracción secuencial \( s \) **declarada** (estimada o barrida). Las columnas ilustrativas de las slides **no** son tus mediciones.

## Entregable

- Código que **compila y corre**
- Informe de 1–2 páginas: curva medida vs. teórica y **por qué** difieren
- Tabla de tiempos (mediana de ≥ 3 corridas), `hardware_concurrency()`, flags de compilación

## Compilación

```bash
make
./secuencial 16777216
./paralelo 16777216 4
./benchmark 16777216
```

Compilador C++17. En Linux, `make` agrega `-pthread`. Windows (Developer Command Prompt):

```text
cl /std:c++17 /O2 /EHsc secuencial.cpp
cl /std:c++17 /O2 /EHsc paralelo.cpp
cl /std:c++17 /O2 /EHsc benchmark.cpp
```

## Criterio de “listo”

- [ ] `secuencial` y `paralelo` dan la misma suma (tolerancia float; con vector de unos, el total esperado es \( N \))
- [ ] `paralelo` usa una primitiva de sincronización **real** (no un comentario). El `break` placeholder tiene que desaparecer.
- [ ] `benchmark` imprime \( T(T) \) y \( S(T) \) para varios \( T \)
- [ ] informe con Amdahl y análisis (memoria, *join*, sobre-suscripción, \( s \), tamaño de `BLOQUE`, …)

## Esqueleto

| Archivo | Qué hay |
|---|---|
| `secuencial.cpp` | referencia completa |
| `paralelo.cpp` | `std::thread` + cola dinámica a medias: los `TODO` son el despacho con mutex |
| `benchmark.cpp` | mide seq vs. par variando hilos; **copiá** tu worker cuando lo termines |
| `Makefile` | `secuencial`, `paralelo`, `benchmark` |

Hasta que completes los `TODO`, `./paralelo` imprime `suma=0`: compila a propósito, no está resuelto. Dejar el placeholder = no cumple el enunciado.



## Implementación en Python y resultados experimentales

### Entorno de ejecución

Las pruebas se realizaron en una computadora con las siguientes características:

- **Sistema operativo:** Linux, arquitectura x86_64.
- **Procesador:** Intel Celeron N4020 a 1,10 GHz.
- **Núcleos físicos:** 2.
- **Procesadores lógicos:** 2.
- **Python:** 3.12.3.
- **Tamaño del vector:** \(N = 2^{24} = 16.777.216\) elementos.
- **Repeticiones:** 5 por configuración.
- **Estadístico informado:** mediana de los tiempos de ejecución.

La implementación utiliza un arreglo de números de precisión simple (`array("f")`), como representación de los datos de entrada. La acumulación de la suma se realiza en variables de punto flotante de Python.

### Resultados medidos

La siguiente tabla presenta las medianas obtenidas por `benchmark.py`. El speedup se calcula como la razón entre el tiempo de la versión secuencial y el tiempo de la versión paralela.

| Versión | Hilos | Mediana (ms) | Speedup | Suma |
|---|---:|---:|---:|---:|
| Secuencial | — | 1229,860 | 1,000 | 16777216,0 |
| Paralela | 1 | 1810,049 | 0,679 | 16777216,0 |
| Paralela | 2 | 3045,667 | 0,404 | 16777216,0 |
| Paralela | 4 | 1930,399 | 0,637 | 16777216,0 |

Las sumas obtenidas coinciden en todas las configuraciones. Sin embargo, ninguna de las versiones paralelas supera el rendimiento de la versión secuencial. El mejor resultado entre las configuraciones paralelas medidas corresponde a un hilo, aunque también es más lento que el programa secuencial.

### Comparación con la ley de Amdahl

La ley de Amdahl modela el speedup teórico de un programa a partir de su fracción secuencial:

\[
S(T)=\frac{1}{s+\frac{1-s}{T}}
\]

Donde \(T\) representa la cantidad de hilos y \(s\) la fracción secuencial del programa.

Para realizar una comparación ilustrativa, se declara \(s=0,25\). Este valor es un supuesto del modelo y no una estimación obtenida experimentalmente.

| Hilos \(T\) | Speedup medido | Speedup teórico (\(s=0,25\)) |
|---:|---:|---:|
| 1 | 0,679 | 1,000 |
| 2 | 0,404 | 1,600 |
| 4 | 0,637 | 2,286 |

En el modelo ideal, aumentar la cantidad de hilos mejora el speedup hasta el límite impuesto por la fracción secuencial. En las mediciones reales ocurre algo diferente: todos los speedups son inferiores a uno.

### Análisis de las diferencias

La diferencia entre los resultados medidos y los teóricos se explica, en parte, por las características de la implementación y del entorno:

- **GIL de CPython:** en la implementación habitual de Python, el Global Interpreter Lock limita la ejecución simultánea de código Python puro entre hilos. Esto reduce las ventajas del paralelismo para una tarea intensiva en cálculos.
- **Sincronización:** los hilos utilizan un candado (`threading.Lock`) para reservar bloques de elementos del vector. La coordinación añade trabajo.
- **Creación y finalización de hilos:** iniciar los hilos y esperar su finalización mediante `join()` también tiene un costo.
- **Reparto de bloques:** la asignación de bloques requiere operaciones adicionales que no existen de la misma manera en la versión secuencial.
- **Recursos disponibles:** la computadora dispone de dos núcleos físicos, por lo que utilizar cuatro hilos no equivale a disponer de cuatro núcleos.

El modelo básico de Amdahl no representa directamente estos costos ni las limitaciones del GIL. Por eso, la curva teórica no coincide con las mediciones de esta implementación.

### Conclusiones

Las implementaciones secuencial y paralela producen el mismo resultado para el vector evaluado. No obstante, la implementación paralela en Python no consigue una aceleración en estas pruebas: la versión secuencial tarda aproximadamente 1,23 segundos, mientras que las versiones paralelas medidas tardan más.

El experimento muestra que utilizar varios hilos no garantiza una mejora de rendimiento. La sobrecarga de coordinación y las particularidades de la ejecución de código Python influyen en el resultado. La ley de Amdahl sirve como referencia teórica, pero sus predicciones deben interpretarse teniendo en cuenta las características reales de la implementación y del hardware.

Las mediciones corresponden a esta computadora y a este entorno de ejecución; no deben generalizarse automáticamente a otras implementaciones o plataformas.
