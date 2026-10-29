
import sys
import threading
from array import array

BLOQUE = 1 << 16  # 65.536 elementos por bloque


def suma_paralela(datos, cantidad_hilos):
    if cantidad_hilos < 1:
        raise ValueError("La cantidad de hilos debe ser >= 1")

    n = len(datos)
    proximo = 0
    parciales = [0.0] * cantidad_hilos
    candado = threading.Lock()

    def worker(indice_hilo):
        nonlocal proximo
        acumulador = 0.0

        while True:
            # Reservar un bloque de forma exclusiva.
            with candado:
                if proximo >= n:
                    break

                inicio = proximo
                fin = min(proximo + BLOQUE, n)
                proximo = fin

            # La suma se realiza fuera del candado.
            for i in range(inicio, fin):
                acumulador += float(datos[i])

        # Cada hilo guarda su propio resultado parcial.
        parciales[indice_hilo] = acumulador

    hilos = []

    for i in range(cantidad_hilos):
        hilo = threading.Thread(target=worker, args=(i,))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return sum(parciales)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2**24
    cantidad_hilos = int(sys.argv[2]) if len(sys.argv) > 2 else 4

    if n < 1 or cantidad_hilos < 1:
        print("N y la cantidad de hilos deben ser >= 1", file=sys.stderr)
        return 1

    datos = array("f", [1.0]) * n
    suma = suma_paralela(datos, cantidad_hilos)

    print(f"N={n} T={cantidad_hilos} suma={suma}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
