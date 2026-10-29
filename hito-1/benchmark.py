
import statistics
import sys
import threading
import time
from array import array
import os

from secuencial import suma_secuencial
from paralelo import suma_paralela

REPETICIONES = 5
CANTIDADES_HILOS = [1, 2, 4, 8, 16]


def medir(funcion, repeticiones=REPETICIONES):
    tiempos = []
    resultado = None

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion()
        fin = time.perf_counter()
        tiempos.append((fin - inicio) * 1000)

    return resultado, statistics.median(tiempos)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2**24

    if n < 1:
        print("N debe ser >= 1", file=sys.stderr)
        return 1

    datos = array("f", [1.0]) * n
    hardware = os.cpu_count()

    suma_seq, tiempo_seq = medir(lambda: suma_secuencial(datos))

    print(f"hardware_concurrency={hardware} N={n}")
    print(f"repeticiones={REPETICIONES}")
    print("hilos,mediana_ms,speedup,suma")

    print(f"seq,{tiempo_seq:.3f},1.000,{suma_seq}")

    for t in CANTIDADES_HILOS:
        if hardware is not None and t > hardware * 2:
            continue

        suma_par, tiempo_par = medir(
            lambda: suma_paralela(datos, t)
        )

        speedup = tiempo_seq / tiempo_par if tiempo_par > 0 else 0.0

        print(
            f"{t},{tiempo_par:.3f},{speedup:.3f},{suma_par}"
        )

        if suma_par != suma_seq:
            print(
                f"ERROR: suma distinta con {t} hilos",
                file=sys.stderr,
            )
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
