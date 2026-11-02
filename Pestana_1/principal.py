"""Script principal: pide los datos al usuario y llama a la función de ModLab2.py."""

from ModLab2 import resolver_sistema


def pedir_numero(mensaje):
    while True:
        try:
            return float(input(mensaje).strip().replace(",", "."))
        except ValueError:
            print("  Valor no válido, intenta de nuevo.")


def pedir_tamano():
    while True:
        try:
            n = int(input("Tamaño del sistema (2, 3 o 4): "))
            if 2 <= n <= 4:
                return n
        except ValueError:
            pass
        print("  Ingresa un entero entre 2 y 4.")


def main():
    print("=== Solucionador de sistemas de ecuaciones lineales ===\n")
    n = pedir_tamano()

    A = []
    b = []
    print("\nIngresa los coeficientes de cada ecuación:")
    for i in range(n):
        fila = [pedir_numero(f"  Ecuación {i + 1}, coeficiente de x{j + 1}: ") for j in range(n)]
        A.append(fila)
        b.append(pedir_numero(f"  Ecuación {i + 1}, término independiente: "))

    try:
        solucion = resolver_sistema(A, b)
    except ValueError as error:
        print(f"\nError: {error}")
        return

    print("\nSolución:")
    for i, valor in enumerate(solucion, start=1):
        print(f"  x{i} = {valor:.6f}")


if __name__ == "__main__":
    main()
