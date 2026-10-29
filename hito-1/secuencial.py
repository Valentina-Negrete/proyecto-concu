import sys
import time
from array import array


def suma_secuencial(datos):
    acumulador = 0.0

    for valor in datos:
        acumulador += float(valor)

    return acumulador


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2**24

    if n < 1:
        print("N debe ser >= 1", file=sys.stderr)
        return 1

    # Vector de números de precisión simple, como en el original.
    datos = array("f", [1.0]) * n

    inicio = time.perf_counter()
    suma = suma_secuencial(datos)
    fin = time.perf_counter()

    tiempo_ms = (fin - inicio) * 1000

    print(f"N={n} suma={suma} tiempo_ms={tiempo_ms:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())