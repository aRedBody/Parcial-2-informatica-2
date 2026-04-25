import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio
import os

plt.ion()
os.makedirs("graficas", exist_ok=True)


class AnalizadorSIATA:
    def __init__(self):
        self.__ruta = ""
        self.__df = pd.DataFrame()
        self.__tiene_fecha = False

    def cargar(self, ruta):
        self.__ruta = ruta
        self.__df = pd.read_csv(ruta)
        # Detectar columna de fecha (datetime64 ya parseado, o string convertible)
        for col in self.__df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.__df[col]):
                self.__df.set_index(col, inplace=True)
                self.__tiene_fecha = True
                print(f"  Columna de fecha '{col}' establecida como indice.")
                break
            if self.__df[col].dtype == object:
                conv = pd.to_datetime(self.__df[col], errors='coerce')
                if conv.notna().sum() > len(conv) * 0.5:
                    self.__df[col] = conv
                    self.__df.set_index(col, inplace=True)
                    self.__tiene_fecha = True
                    print(f"  Columna de fecha '{col}' establecida como indice.")
                    break
        print(f"  Archivo: {os.path.basename(ruta)} | Filas: {len(self.__df)} | Columnas: {list(self.__df.columns)}")

    def __str__(self):
        return f"AnalizadorSIATA | {os.path.basename(self.__ruta)} | {len(self.__df)} filas"

    def mostrarInfo(self):
        print("\n--- INFO ---")
        self.__df.info()
        print("\n--- DESCRIBE ---")
        print(self.__df.describe())

    def verColumnas(self):
        return list(self.__df.select_dtypes(include='number').columns)

    def graficarColumna(self, col):
        datos = self.__df[col].dropna()

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(f"SIATA - {col}")

        axes[0].plot(self.__df.index, self.__df[col], lw=0.8, color='steelblue')
        axes[0].set_title("Serie temporal")
        axes[0].set_xlabel("Fecha")
        axes[0].set_ylabel(col)
        axes[0].tick_params(axis='x', rotation=30)

        axes[1].boxplot(datos, patch_artist=True)
        axes[1].set_title("Boxplot")
        axes[1].set_xlabel(col)
        axes[1].set_ylabel("Valor")

        axes[2].hist(datos, bins=30, color='seagreen', edgecolor='white')
        axes[2].set_title("Histograma")
        axes[2].set_xlabel(col)
        axes[2].set_ylabel("Frecuencia")

        plt.tight_layout()
        archivo = f"graficas/SIATA_graficos_{col}.png"
        plt.savefig(archivo, dpi=150, bbox_inches='tight')
        print(f"  Grafico guardado: {archivo}")
        plt.show()

    def operaciones(self, col1, col2, op):
        # 1. apply: normalizar col1
        mn, mx = self.__df[col1].min(), self.__df[col1].max()
        norm = self.__df[col1].apply(lambda x: (x - mn) / (mx - mn) if pd.notna(x) else float('nan'))
        print(f"\n1. apply - Normalizacion de '{col1}' (primeras 5 filas):")
        print(norm.head().to_string())

        # 2. map: categorizar col1 segun mediana
        mediana = self.__df[col1].median()
        cat = self.__df[col1].map(lambda x: 'ALTO' if pd.notna(x) and x >= mediana else ('BAJO' if pd.notna(x) else None))
        print(f"\n2. map - Categorizacion de '{col1}' (mediana={mediana:.2f}):")
        print(cat.value_counts().to_string())

        # 3. sumar o restar dos columnas
        if op == 's':
            res = self.__df[col1] + self.__df[col2]
            print(f"\n3. Suma '{col1}' + '{col2}' (primeras 5 filas):")
        else:
            res = self.__df[col1] - self.__df[col2]
            print(f"\n3. Resta '{col1}' - '{col2}' (primeras 5 filas):")
        print(res.head().to_string())

    def graficarRemuestreo(self, col):
        if not self.__tiene_fecha:
            print("  Error: el archivo no tiene columna de fecha como indice.")
            return
        d = self.__df[col].resample('D').mean().dropna()
        try:
            m = self.__df[col].resample('ME').mean().dropna()
        except:
            m = self.__df[col].resample('M').mean().dropna()
        try:
            q = self.__df[col].resample('QE').mean().dropna()
        except:
            q = self.__df[col].resample('Q').mean().dropna()

        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        fig.suptitle(f"SIATA - Remuestreo - {col}")

        axes[0].plot(d.index, d.values, marker='o', ms=3, color='royalblue')
        axes[0].set_title("Diario")
        axes[0].set_xlabel("Fecha")
        axes[0].set_ylabel(col)
        axes[0].tick_params(axis='x', rotation=30)

        axes[1].plot(m.index, m.values, marker='o', ms=4, color='darkorange')
        axes[1].set_title("Mensual")
        axes[1].set_xlabel("Fecha")
        axes[1].set_ylabel(col)
        axes[1].tick_params(axis='x', rotation=30)

        axes[2].plot(q.index, q.values, marker='s', ms=6, color='forestgreen')
        axes[2].set_title("Trimestral")
        axes[2].set_xlabel("Fecha")
        axes[2].set_ylabel(col)
        axes[2].tick_params(axis='x', rotation=30)

        plt.tight_layout()
        archivo = f"graficas/SIATA_remuestreo_{col}.png"
        plt.savefig(archivo, dpi=150, bbox_inches='tight')
        print(f"  Grafico guardado: {archivo}")
        plt.show()


class AnalizadorEEG:
    FS = 1000

    def __init__(self):
        self.__ruta = ""
        self.__data3d = np.zeros((1, 1, 1))
        self.__data2d = np.zeros((1, 1))

    def cargar(self, ruta):
        self.__ruta = ruta
        mat = sio.loadmat(ruta)
        llaves = sio.whosmat(ruta)
        print("\nVariables en el archivo (whosmat):")
        for i, (nombre, forma, tipo) in enumerate(llaves):
            print(f"  {i} -> {nombre}: {forma} ({tipo})")
        idx = int(input("Seleccione el numero de la variable a cargar: "))
        llave = llaves[idx][0]
        self.__data3d = mat[llave]
        if self.__data3d.ndim == 3:
            canales, puntos, ensayos = self.__data3d.shape
            self.__data2d = np.reshape(self.__data3d, (canales, puntos * ensayos), order='F')
        else:
            self.__data2d = self.__data3d
        print(f"  Forma 3D: {self.__data3d.shape} | Forma 2D: {self.__data2d.shape}")

    def __str__(self):
        return f"AnalizadorEEG | {os.path.basename(self.__ruta)} | 3D: {self.__data3d.shape}"

    def mostrarLlaves(self):
        print("\nVariables en el archivo (whosmat):")
        for nombre, forma, tipo in sio.whosmat(self.__ruta):
            print(f"  {nombre}: {forma} ({tipo})")

    def verCanales(self):
        return self.__data3d.shape[0]

    def verMuestras(self):
        return self.__data2d.shape[1]

    def sumarCanales(self, canales, pmin, pmax):
        t = np.arange(pmin, pmax) / self.FS
        suma = np.sum([self.__data2d[ch, pmin:pmax] for ch in canales], axis=0)
        nombres = [c + 1 for c in canales]

        fig, axes = plt.subplots(2, 1, figsize=(14, 8))
        fig.suptitle(f"EEG - Suma canales {nombres}")

        for ch in canales:
            axes[0].plot(t, self.__data2d[ch, pmin:pmax], label=f"Canal {ch + 1}")
        axes[0].set_title(f"Canales seleccionados: {nombres}")
        axes[0].set_xlabel("Tiempo (s)")
        axes[0].set_ylabel("Amplitud (uV)")
        axes[0].legend()
        axes[0].grid(alpha=0.3)

        axes[1].plot(t, suma, color='crimson', label=f"Suma canales {nombres}")
        axes[1].set_title(f"Resultado: suma de canales {nombres}")
        axes[1].set_xlabel("Tiempo (s)")
        axes[1].set_ylabel("Amplitud (uV)")
        axes[1].legend()
        axes[1].grid(alpha=0.3)

        plt.tight_layout()
        c_str = "_".join(str(c) for c in nombres)
        archivo = f"graficas/EEG_suma_{c_str}.png"
        plt.savefig(archivo, dpi=150, bbox_inches='tight')
        print(f"  Grafico guardado: {archivo}")
        plt.show()

    def estadisticas3D(self, eje):
        prom = np.mean(self.__data3d, axis=eje).flatten()
        std  = np.std(self.__data3d,  axis=eje).flatten()

        if len(prom) > 300:
            paso = len(prom) // 300
            prom = prom[::paso]
            std  = std[::paso]

        idx = np.arange(len(prom))

        fig, axes = plt.subplots(2, 1, figsize=(14, 8))
        fig.suptitle(f"EEG - Estadisticas 3D - eje {eje}")

        axes[0].stem(idx, prom, linefmt='C0-', markerfmt='C0o', basefmt='k-')
        axes[0].set_title(f"Promedio a lo largo del eje {eje}")
        axes[0].set_xlabel("Indice")
        axes[0].set_ylabel("Amplitud media (uV)")
        axes[0].grid(alpha=0.3)

        axes[1].stem(idx, std, linefmt='C1-', markerfmt='C1o', basefmt='k-')
        axes[1].set_title(f"Desviacion estandar a lo largo del eje {eje}")
        axes[1].set_xlabel("Indice")
        axes[1].set_ylabel("Desv. estandar (uV)")
        axes[1].grid(alpha=0.3)

        plt.tight_layout()
        archivo = f"graficas/EEG_estadisticas_eje{eje}.png"
        plt.savefig(archivo, dpi=150, bbox_inches='tight')
        print(f"  Grafico guardado: {archivo}")
        plt.show()


class AlmacenObjetos:
    def __init__(self):
        self.__objetos = {}

    def agregar(self, nombre, obj):
        self.__objetos[nombre] = obj
        print(f"  Objeto '{nombre}' guardado ({type(obj).__name__}).")

    def buscar(self, nombre):
        return self.__objetos.get(nombre, False)

    def listar(self):
        if not self.__objetos:
            print("  No hay objetos guardados.")
            return
        print("\nObjetos en el almacen:")
        for nom, obj in self.__objetos.items():
            print(f"  * '{nom}': {type(obj).__name__}")
