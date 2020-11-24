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
                    'components': None
                    
                    }

        analyzer['trips'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStations)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStations)
        
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

def Analizar_Top_Entry(analyzer):
    lista=[]
    estructura=totalEdges(analyzer["connections"])
    iterator=it.newIterator(estructura)
    while it.hasNext(iterator):
        arco=it.next(iterator) #dict_keys(['vertexA', 'vertexB', 'weight'])
        lista.append(arco["vertexA"])
    top={"Top1":0,"Top2":0,"Top3":0}
    maxi=0
    for arco_entrada in lista:
        valor=lista.count(arco_entrada)
        if valor>maxi:
            if valor>top["Top1"] and (valor != top["Top1"]) and valor>top["Top2"] and valor>top["Top3"]:
                top["Top1"]=valor
            elif valor>top["Top2"] and (valor != top["Top2"]) and valor>top["Top3"] and valor<top["Top1"]:
                top["Top2"]=valor
            elif valor>top["Top3"] and (valor != top["Top3"]) and valor<top["Top1"] and valor<top["Top2"]:
                top["Top3"]=valor
    return top

#def O():
    # Obtener vertices iniciales
    #   Buscar veces que ese vertice esta en arco con f.librery
    #     Establecer top3
    #     Ret Dict

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
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def totalEdges(grafo):
    return gr.edges(grafo)

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