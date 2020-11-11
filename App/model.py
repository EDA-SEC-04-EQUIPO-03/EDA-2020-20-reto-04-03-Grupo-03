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
                    'components': None,
                    'routes': None
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
    edge = gr.getEdge(analyzer ["connections"], origin, destination)
    if edge is None:
        gr.addEdge(analyzer["connections"], origin, destination, duration)
    return analyzer



# ==============================
# Funciones de consulta
# ==============================

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    print(" Iniciando")
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    print(" Terminado")
    return scc.connectedComponents(analyzer['components'])


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def servedRoutes(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stops'])
    itlstvert = it.newIterator(lstvert)
    maxvert = None
    maxdeg = 0
    while(it.hasNext(itlstvert)):
        vert = it.next(itlstvert)
        lstroutes = m.get(analyzer['stops'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg


# ==============================
# Funciones Helper
# ==============================

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name


# ==============================
# Funciones de Comparacion
# ==============================

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1