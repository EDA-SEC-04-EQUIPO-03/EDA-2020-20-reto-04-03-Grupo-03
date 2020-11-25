"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
from DISClib.ADT import graph as g
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

servicefile = '201801-1-citibike-tripdata.csv'
initialStation = None
recursionLimit = 20000
# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información ")
    print("3- Requerimiento #1 ")

    print("5- Requerimiento #3 ")

    print("7- Requerimiento #5 ")
    print("0- Salir")
    print("*******************************************")

def CargarInfo():
    print("\nCargando información de transporte de singapur ....")
    # A continuación si se quieren cargar todos los archivos disponible .csv
    #controller.loadTrips(cont)
    # A continuación si se quieren cargar archivo .csv específicos
    controller.loadData(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalVertex(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))

def Req1():
    E1=input("Ingrese la primer estación de interés: ")
    E2=input("Ingrese la segunda estación de interés: ")
    print("Num de componentes conectados: "+str(controller.numSCC(cont)))
    print("Entre "+str(E1)+" y "+str(E2)+" es: "+str(controller.sameCC(cont,E1,E2))+" que pertenezcan al mismo cluster")
    

def Req3():
    print("Escriba a continuación -1- si quiere analizar top de estaciones de llegada")
    print("Escriba a continuación -2- si quiere analizar top de estaciones de salida")
    print("Escriba a continuación -3- si quiere analizar estaciones menos usadas")
    A=input("Inserte una opción válida aca por favor: ")
    if int(A)==1:
        tripletop=controller.hallartop3(cont,"vertexA")
        print("La primer estación de la que llegan más viajes es: "+str(tripletop[1]["Top1"])+" = "+str(tripletop[0]["Top1"]))
        print("La segunda estación de la que llegan más viajes es: "+str(tripletop[1]["Top2"])+" = "+str(tripletop[0]["Top1"]))
        print("La tercer estación de la que llegan más viajes es: "+str(tripletop[1]["Top3"])+" = "+str(tripletop[0]["Top1"]))
    elif int(A)==2:
        tripletop=controller.hallartop3(cont,"vertexB")
        print("La primer estación de la que salen más viajes es: "+str(tripletop[1]["Top1"])+" = "+str(tripletop[0]["Top1"]))
        print("La segunda estación de la que salen más viajes es: "+str(tripletop[1]["Top2"])+" = "+str(tripletop[0]["Top1"]))
        print("La tercer estación de la que salen más viajes es: "+str(tripletop[1]["Top3"])+" = "+str(tripletop[0]["Top1"]))
    elif int(A)==3: 
        tripleNotop=controller.minimunEdges(cont)
        print("La primer estación menos usada: "+str(tripleNotop[1]["Top1"])+" = "+str(tripleNotop[0]["Top1"]))
        print("La segunda estación menos usada: "+str(tripleNotop[1]["Top2"])+" = "+str(tripleNotop[0]["Top1"]))
        print("La tercer estación menos usada "+str(tripleNotop[1]["Top3"])+" = "+str(tripleNotop[0]["Top1"]))
    
    else:
        print("Esa opción no vale, intente de nuevo")

def Req4():
    print("haloja ")

def Req5():
    print("Querido usuario, siga las intrucciones: ")
    print("->   Si usted tiene entre 0-10 años marque -1-")
    print("->   Si usted tiene entre 11-20 años marque -2-")
    print("->   Si usted tiene entre 21-30 años marque -3-")
    print("->   Si usted tiene entre 31-40 años marque -4-")
    print("->   Si usted tiene entre 41-50 años marque -5-")
    print("->   Si usted tiene entre 51-60 años marque -6-")
    print("->   Si usted tiene más de 60 años años marque -7-")
    opcion=input("Ingrese aca su opción según su edad: ")
    Opcion=int(opcion)
    trip=controller.tripsyear(cont,Opcion)
    

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(CargarInfo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(Req1, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    #Lora gei
    #guardar
    
    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(Req3, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(Req4, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(Req5, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    else:
        sys.exit(0)
sys.exit(0)

