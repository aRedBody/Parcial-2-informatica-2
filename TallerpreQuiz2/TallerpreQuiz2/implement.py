from clases import *
import scipy.io as sio
import pandas as pd
import os

def main():
    sis = Sistema()
    while True:
        menu = int(input("\n\t>>>>> MENU PPAL <<<<<\n1- Ingresar\n2- Graficar\n3-Estadisticos de examen\n4- Salir\n-->"))
        if menu == 1:
            p = Persona()
            p.asignarName(input("Ingrese nombre: "))
            p.asignarCC(int(input("Ingrese cedula: ")))
            p.asignarEdad(int(input("Ingrese edad: ")))
            p.asignarGenero(input("Ingrese genero: "))
            tipArch = int(input("Indique segun archivo a abrir:\r\n 1-Archivo .mat \r\n2- Archivo .csv: "))
            if tipArch == 1:
                dicc = sio.loadmat(input("Ruta del archivo .mat: "))
                llaveArreglo = int(input("Ingrese el numero que desea: \t\n{}".format(''.join(map(lambda x: f"-> {x[0]} : {x[1]} \n", enumerate(dicc))))))
                matriz = dicc[list(dicc.keys())[llaveArreglo]]
                if matriz.ndim == 3: # canales, puntos, ensayos = matriz3D.shape
                    canales,puntos,ensayos = matriz.shape
                    matriz = np.reshape(matriz,(canales,puntos*ensayos), order = "F")
                    senalEEG = Biosenal(matriz)            
                    p.asignarEEG(senalEEG)
                else:
                    senalEEG = Biosenal(matriz)            
                    p.asignarEEG(senalEEG)                    
            else:
                matriz = pd.read_csv(input("Ruta del archivo .csv: "),sep=";")
                # examen = Biosenal(matriz)            
                examen = ExamenTabular(matriz)
                p.asignarEsta(examen)
            sis.ingresarPac(p)
            
        elif menu == 2:
            cedPac = int(input("Ingrese la cédula del paciente del que desea hacer la grafica: "))
            pac = sis.verPac(cedPac)
            # ex= input("Q tipo de examen deseas graficar 1:EEG, 2:ECG,3:Tabular"):
            # if ex == "1":
            #     bioS_graficar = pac.verEEG()
            # elif ex == "2":
            #     bioS_graficar = pac.verECG()
            # elif ex == "3":
            #     bioS_graficar = pac.verEsta()
            bioS_graficar = pac.verEEG()
            print(f"Tenga en cuenta las siguiente información : \n {bioS_graficar}")
            while True:
                submenu = int(input("Que desea graficar:\n\t1. Todos los canales\n\t2. Un solo canal\n\t3. El promedio\n\t4. Salir de graficación\n\t --> "))
                x_min= int(input("Ingrese punto inicial del segmento que desea graficar: "))
                x_max= int(input("Ingrese punto final del segmento que desea graficar: "))                
                gra = Graficadora()
                if submenu == 1:
                    gra.graficarSenal(bioS_graficar.devolver_Segmento(x_min,x_max))
                elif submenu == 2:
                    canal = int(input("Ingrese el canal que desea graficar: "))
                    gra.graficarSenal(bioS_graficar.devolver_Canal(canal, x_min,x_max))
                elif submenu == 3:
                    eje = int(input("Ingrese a lo largo de que eje desea hacer el promedio, 0 o 1 para graficar: "))
                    gra.graficaPromedio(bioS_graficar.promedio(eje, x_min,x_max))
                elif submenu == 4:
                    break

        elif menu == 3:
            cedPac = int(input("Ingrese la cédula del paciente del que desea hacer los calculos: "))
            pac = sis.verPac(cedPac)
            examenT = pac.verEsta()
            if examenT != None:
                print(examenT.verCol())
                columnas = input("Columna que desea graficar")
                examenT.grafico([columnas])
            
        elif menu == 4:
            break

if __name__ == "__main__":
    main()
            
        
        
    