import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.ion()
class Persona:
    def __init__(self):
        self.__name = ""
        self.__cc = 0
        self.__genero = ""
        self.__edad = 0
        self.__EEG = Biosenal()
        self.__ECG = Biosenal()
        self.__datos = ExamenTabular()
        
    def asignarName(self,t):
        self.__name = t
    def asignarCC(self,t):
        self.__cc = t
    def asignarEdad(self,e):
        self.__edad = e 
    def asignarGenero(self,g):
        self.__genero = g 
    def asignarEEG(self,t):
        self.__EEG = t 
    def asignarECG(self,t):
        self.__ECG = t 
    def asignarEsta(self,t):
        self.__datos = t 
    def verName(self):
        return self.__name
    def verCC(self):
        return self.__cc
    def verGenero(self):
        return self.__genero
    def verEdad(self):
        return self.__edad 
    def verEEG(self):
        return self.__EEG  
    def verECG(self):
        return self.__ECG  
    def verEsta(self):
        return self.__datos
    

class Sistema: 
    def __init__(self):
        self.__pacs = {}
        
    def ingresarPac(self,p):
        self.__pacs[p.verCC()] = p
        
    def verPac(self,ced):
        return self.__pacs.get(ced,False)

class Biosenal:
    #constructor que recibe los datos, si no se entregan por defectos estaran 
    #vacios
    def __init__(self,data = np.zeros((2,2))):
        self._data = data
        self.__dimension =  self._data.ndim
        self.__forma =  self._data.shape
        self.__tamano =  self._data.size
        self.__canales = self.__forma[0]
        self.__puntos = self.__forma[1]
        
    def __str__(self):
        return f"""Las características de la matriz de la señal matriz son: 
                    forma: {self.__forma}
                    dimension: {self.__dimension}
                    tamaño: {self.__tamano}"""
                    
    def asignarDatos(self,data):
        self._data = data 
        self.__dimension =  self._data.ndim
        self.__forma =  self._data.shape
        self.__tamano =  self._data.size
        self.__canales = data.forma[0]
        self.__puntos = data.forma[1]
        
    def verForma(self):
        return self.__forma
    def verDim(self):
        return self.__dimension
    def verTam(self):
        return self.__tamano
    def verCanales(self):
        return self.__canales
    def verPuntos(self):
        return self.__puntos
        
    def devolver_Canal(self,canal,pmin,pmax):
        if pmin >= pmax:
            return None
        return self._data[canal,pmin:pmax]
    
    def devolver_Segmento(self,pmin,pmax):
        if pmin >= pmax:
            return None
        return self._data[:,pmin:pmax]
    
    def promedio(self,eje,pmin,pmax):
        return np.mean(self._data[:,pmin:pmax],axis = eje)        
    
    def desviacion(self,eje,pmin,pmax):
        return  np.std(self._data[:,pmin:pmax],axis = eje)
    
class ExamenTabular(Biosenal):
    def __init__(self,data = np.zeros((2,2))):
        Biosenal.__init__(self,data)
        self.__tablaEx = pd.DataFrame(self._data)
        self.__columnas = self.__tablaEx.columns
        
    def verCol(self):
        return self.__columnas    
        
    def procesoEstadistico(self):
        return self.__tablaEx.describe()
    
    def devolver_Segmento(self,imin,imax,columnas):
        if imin >= imax:
            return None
        return self.__tablaEx.loc[imin:imax,[columnas]]    
    
    def promedio(self):
        eje =  int(input("Ingrese:\n 0- A lo largo de las columnas\n 1- A lo argo de las filas"))
        return self.__tablaEx.mean(axis=eje)      
    def desviacion(self):
        eje =  int(input("Ingrese:\n 0- A lo largo de las columnas\n 1- A lo argo de las filas"))
        return self.__tablaEx.std(axis=eje)      
    def mediana(self):
        eje =  int(input("Ingrese:\n 0- A lo largo de las columnas\n 1- A lo argo de las filas"))
        return self.__tablaEx.median(axis=eje)   
    def grafico(self,columnas):
        self.__tablaEx.boxplot(columnas)
        
class Graficadora:
    def __init__(self):
        self.__fig = plt.figure()
        self.__axes = self.__fig.add_subplot(111)
        # self.__axes2 = self.__fig.add_subplot(212)
        
    def graficarSenal(self,datos):
        self.__axes.clear()
        if datos.ndim == 1:
            self.__axes.plot(datos) 
        else:
            for c in range(datos.shape[0]):
                self.__axes.plot(datos[c,:]+c*600) 
        nx = input("Ingrese nombre del eje x: ")
        ny = input("Ingrese nombre del eje y: ")
        tit = input("Titulo: ")
        self.__axes.set_xlabel(nx)
        self.__axes.set_ylabel(ny)
        self.__axes.set_title(tit)
        plt.show()
        
    def graficaPromedio(self, datos):
        self.__axes.clear()
        self.__axes.stem(datos)
        self.__axes.set_xlabel('Sensores')
        self.__axes.set_ylabel('Promedio Voltaje (uV)')
        self.__axes.set_title('Proemdios EEG')
        plt.show()
        
