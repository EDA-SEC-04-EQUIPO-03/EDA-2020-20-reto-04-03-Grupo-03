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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import mapentry as me
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def Analizador():
 try:
        analyzer = {
                    'trips': None,
                    'connections': None,
                    'bikeid': None,
                    'components': None,
                    'years': None
                    
                    }

        analyzer['trips'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStations)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStations)
        analyzer['years'] = m.newMap(numelements=14000,
                                     maptype='CHAINING',
                                     comparefunction=compareDates)
        
        return analyzer
 except Exception as exp:
        error.reraise(exp, 'model:Analizador')

# Funciones para agregar informacion al grafo

def AddViaje(analyzer,trip):
    #Cada estación se agrega como un vértice al grafo, si es que aún no existe.
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(analyzer, origin)
    addStation(analyzer, destination)
    addConnection(analyzer, origin, destination, duration)

def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(analyzer ["connections"], stationid):
            gr.insertVertex(analyzer ["connections"], stationid)
    return analyzer

def addConnection(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    promedio=None
    edge = gr.getEdge(analyzer ["connections"], origin, destination)
    if edge is None:
        gr.addEdge(analyzer["connections"], origin, destination, duration)
    elif edge is not None and promedio is None:
        numero_viajes=1
        promedio=int(edge["weight"])
        promedio =(promedio*numero_viajes + duration)/(numero_viajes + 1)
        numero_viajes += 1
        edge["weight"]=promedio
    else:
        promedio=int(edge["weight"])
        promedio =(promedio*numero_viajes + duration)/(numero_viajes + 1)
        numero_viajes += 1
        edge["weight"]=promedio
    return analyzer

def Analizar_Top_Entry(analyzer,vertice):
    lista=[]
    estructura=totalEdges(analyzer["connections"])
    iterator=it.newIterator(estructura)
    while it.hasNext(iterator):
        arco=it.next(iterator) #dict_keys(['vertexA', 'vertexB', 'weight'])
        lista.append(arco[vertice])
    top={"Top1":1,"Top2":1,"Top3":1} #valores
    Top={"Top1":None,"Top2":None,"Top3":None} #nombres
    for arco_entrada in lista:
        valor=lista.count(arco_entrada)
        #print("Vertice a/b: "+str(arco_entrada)+" ="+str(valor)) //funciona 
        if valor>top["Top1"] and (arco_entrada != Top["Top1"]) and valor>top["Top2"] and valor>top["Top3"]:
            top["Top1"]=valor
            Top["Top1"]=arco_entrada
        elif valor>top["Top2"] and (arco_entrada != Top["Top2"]) and valor>top["Top3"] and valor<top["Top1"]: #and Top["Top2"]!=Top["Top1"]
            top["Top2"]=valor
            Top["Top2"]=arco_entrada
        elif valor>top["Top3"] and (arco_entrada != Top["Top3"]) and valor<top["Top1"] and valor<top["Top2"]: #and Top["Top2"]!=Top["Top1"]
            top["Top3"]=valor
            Top["Top3"]=arco_entrada
    return top,Top

def Never_top(analyzer):
    lista=[]
    estructura=totalVertices(analyzer["connections"]) #single lista de los vertices
    iterator=it.newIterator(estructura)
    while it.hasNext(iterator):
        edge=it.next(iterator) #str - lista de vertices- //estaciones id
        lista.append(edge)
    top={"Top1":9999,"Top2":9999,"Top3":9999}
    Top={"Top1":None,"Top2":None,"Top3":None}
    for arco in lista: #arco = cada vertice
        num_edges=arcosXvertex(analyzer["connections"],arco)
        #print("Vertice "+str(arco)+" = "+str(num_edges)) //funciona
        if num_edges<top["Top1"] and num_edges<top["Top2"] and num_edges<top["Top3"] and arco!=Top["Top1"]:
            top["Top1"]=num_edges
            Top["Top1"]=arco
        elif num_edges<top["Top2"] and num_edges<top["Top3"] and num_edges>top["Top1"] and arco!=Top["Top2"]:
            top["Top2"]=num_edges
            Top["Top2"]=arco
        elif num_edges<top["Top3"] and num_edges>top["Top2"] and num_edges>top["Top1"] and arco!=Top["Top3"]:
            top["Top3"]=num_edges
            Top["Top3"]=arco
    return top, Top

#def O():
    # Obtener vertices iniciales
    #   Buscar veces que ese vertice esta en arco con f.librery
    #     Establecer top3
    #     Ret Dict

def AddViajePorhora(analyzer, fecha,trip):  #trip:linea de archivo, fecha:año de cada archivo
    structure=analyzer["years"]
    hayviaje= m.contains(structure, fecha)
    if hayviaje:
        entrada=m.get(structure, fecha) #//dict: llave/valor = año/{"info":"","trips":singlelinked}
        struc=me.getValue(entrada)  #//dict -> return: {"info":"año","trips":singlelinked} 
    else:
        struc=newViajeFecha(fecha) #crear
        m.put(structure, fecha, struc) #args: Map, key value //2020:{"info":"","trips":singlelinked}
    lt.addLast(struc["trips"], trip) #{"info":"","trips":singlelinked}   añadir en trips linea archivo


def newViajeFecha(año):
    entry = {'info': "", "trips": None}
    entry['info'] = año
    entry['trips'] = lt.newList('ARRAY_LIST', compareDates)
    return entry

def getTripsFecha(analyzer, opción):
    mapa=analyzer["years"]
    estacionentrada=123
    entradabig=0
    estacionsalida=321
    salidabig=0
    if opción==1:
        i=0
        while i<=10:
            listadesingles=m.get(mapa,i) #año/{"info":"","trips":singlelinked}
            single=me.getValue(listadesingles)  #//dict -> return: {"info":"","trips":singlelinked} 
            iterator=it.newIterator(single["trips"])
            while it.hasNext(iterator):
                lineaarchivo = it.next(iterator)
                #chequear estacion mas salidas-vertexA-
                mayorsalida=salenviajes(analyzer["connections"],lineaarchivo["start station id"]) #int
                #chequear estación mas llegadas -vertexB-
                mayorentrada=entranviajes(analyzer["connections"],lineaarchivo["end station id"]) #int
                if mayorentrada>entradabig:
                    entradabig=mayorentrada
                    estacionentrada=lineaarchivo["end station id"]
                if mayorsalida>salidabig:
                    salidabig=mayorsalida
                    estacionsalida=lineaarchivo["start station id"]
            i+=1
    # retornar estructura{"EstacionE":estacionentrada,"ValorE":entradabig,"EstacionS":estacionsalida,"ValorS":salidabig}
    elif opción==2:
        i=11
        while i<=20:
            print("")
    elif opción==3:
        i=21
        while i<=30:
            print("")
    elif opción==4:
        i=31
        while i<=40:
            print("")
    elif opción==5:
        i=41
        while i<=50:
            print("")
    elif opción==6:
        i=51
        while i<=60:
            print("")
    elif opción==7:
        i=61
        while i<100:
            print("")
    else:
        print("Esa opción no vale")
    return {"EstacionE":estacionentrada,"ValorE":entradabig,"EstacionS":estacionsalida,"ValorS":salidabig}

# ==============================
# Funciones de consulta
# ==============================

# Número de componentes conectados fuertemente
def numSCC(analyzer):
    sc = scc.KosarajuSCC(analyzer["connections"])
    return scc.connectedComponents(sc)
    

# ¿Dos estaciones en el mismo componente?
def sameCC(analyzer, station1, station2):
    sc = scc.KosarajuSCC(analyzer["connections"])
    return scc.stronglyConnected(sc, station1, station2)


def totalVertex(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertex(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def totalEdges(grafo):
    """
    Retorna todos los arcos del grafo
    """
    return gr.edges(grafo)

def totalVertices(grafo):
    """
    Retorna todos los vertices del grafo
    """
    return gr.vertices(grafo)

def arcosXvertex(grafo,word):
    """
    Retorna arcos del vertice
    """
    a=gr.indegree(grafo,word)
    b=gr.outdegree(grafo,word)
    return a+b

def salenviajes(grafo,word):
    """
    numero de arcos que salen del vertex (word)
    """
    return gr.outdegree(grafo,word)

def entranviajes(grafo,word):
    """
    numero de arcos que entran al vertex (word)
    """
    return gr.indegree(grafo,word)

# ==============================
# Funciones Helper
# ==============================



# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(stat, keyvalue):
    """
    Compara dos estaciones
    """
    code = keyvalue['key']
    if (stat == code):
        return 0
    elif (stat > code):
        return 1
    else:
        return -1

def compareBikeid(bike, keyvaluebike):
    """
    Compara dos bikeids
    """
    bikecode = keyvaluebike['key']
    if (bike == bikecode):
        return 0
    elif (bike > bikecode):
        return 1
    else:
        return -1

def compareDates(date1, date2):
    date20=me.getKey(date2)
    #print(date1)
    #print(date2)
    if (date1 == date20):
        return 0
    elif (date1 > date20):
        return 1
    else:
        return -1
    