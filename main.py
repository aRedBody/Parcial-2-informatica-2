from clases import *


def main():
    almacen = AlmacenObjetos()

    while True:
        menu = int(input("\n\t>>>>> MENU PRINCIPAL <<<<<\n1- Cargar CSV (SIATA)\n2- Cargar MAT (EEG)\n3- Almacen de objetos\n4- Salir\n-->"))

        if menu == 1:
            obj = AnalizadorSIATA()
            obj.cargar(input("Ruta del archivo CSV: "))
            nombre = input("Nombre para este objeto: ")
            almacen.agregar(nombre, obj)
            cols = obj.verColumnas()
            print(f"Columnas numericas: {cols}")

            while True:
                sub = int(input("\n--- SIATA ---\n1- Info basica\n2- Graficos de columna\n3- Operaciones\n4- Remuestreo\n5- Volver\n-->"))
                if sub == 1:
                    obj.mostrarInfo()
                elif sub == 2:
                    col = input(f"Columna a graficar {cols}: ")
                    obj.graficarColumna(col)
                elif sub == 3:
                    print(f"Columnas: {cols}")
                    c1 = input("Primera columna: ")
                    c2 = input("Segunda columna: ")
                    op = input("Operacion (sumar / restar): ")
                    obj.operaciones(c1, c2, op)
                elif sub == 4:
                    col = input(f"Columna para remuestrear {cols}: ")
                    obj.graficarRemuestreo(col)
                elif sub == 5:
                    break

        elif menu == 2:
            obj = AnalizadorEEG()
            obj.cargar(input("Ruta del archivo MAT: "))
            nombre = input("Nombre para este objeto: ")
            almacen.agregar(nombre, obj)
            n = obj.verCanales()
            m = obj.verMuestras()

            while True:
                sub = int(input("\n--- EEG ---\n1- Mostrar llaves\n2- Sumar 3 canales\n3- Estadisticas 3D\n4- Volver\n-->"))
                if sub == 1:
                    obj.mostrarLlaves()
                elif sub == 2:
                    print(f"Canales disponibles: 1 a {n} | Muestras: 0 a {m - 1}  ({m / AnalizadorEEG.FS:.1f} s)")
                    c1 = int(input(f"Canal 1 (1-{n}): ")) - 1
                    c2 = int(input(f"Canal 2 (1-{n}): ")) - 1
                    c3 = int(input(f"Canal 3 (1-{n}): ")) - 1
                    pmin = int(input("Muestra minima: "))
                    pmax = int(input("Muestra maxima: "))
                    obj.sumarCanales([c1, c2, c3], pmin, pmax)
                elif sub == 3:
                    print("Ejes:\n  0 -> a lo largo de canales\n  1 -> a lo largo de muestras\n  2 -> a lo largo de epocas")
                    eje = int(input("Eje (0, 1 o 2): "))
                    obj.estadisticas3D(eje)
                elif sub == 4:
                    break

        elif menu == 3:
            while True:
                sub = int(input("\n--- ALMACEN ---\n1- Listar\n2- Buscar\n3- Volver\n-->"))
                if sub == 1:
                    almacen.listar()
                elif sub == 2:
                    nombre = input("Nombre a buscar: ")
                    obj = almacen.buscar(nombre)
                    if obj:
                        print(f"  Encontrado: {obj}")
                    else:
                        print("  No encontrado.")
                elif sub == 3:
                    break

        elif menu == 4:
            print("Hasta luego!")
            break


if __name__ == "__main__":
    main()
