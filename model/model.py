import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self.idMapN={}
        self._percorsoSfigato = []
        self._totSfiga = 0

    def getAllYears(self):
        return DAO.getAllYears()

    def buidGraph(self,min,max):
        nodi=DAO.getAllConstructors()
        for n in nodi:
            n.risultati ={}
            for i in range (min,max):
                n.risultati["i"]=DAO.getResults(n.constructorId,i)

            self.idMapN[n.constructorId]=n
        self._grafo.add_nodes_from(nodi)
        self.addEdges(min,max,self.idMapN)
    def addEdges(self,min,max,idMap):
        archi=DAO.getAllEdges(min,max,idMap)
        for a in archi:
            self._grafo.add_edge(a.c1,a.c2,weight=a.peso)


    def infoGrafo(self):
        return len(self._grafo.nodes),len(self._grafo.edges)
    def stampaDetagli(self):
        conn=list(nx.connected_components(self._grafo))
        connessa=conn[0] #connessa=list(max(conn,key=len))
        res=[]
        for c in connessa:
            res.append((c.constructorRef,self._getMaxEdge(c)))

        res.sort(key=lambda x:x[1],reverse=True)

        return res
    def _getMaxEdge(self,c):
        val=0
        for i in self._grafo.neighbors(c):
            if self._grafo[c][i]["weight"]>val:
                val=self._grafo[c][i]["weight"]
        return val

    def  worstPath(self,k,m,min,anno_max):
        self._percorsoSfigato=[]
        self._totSfiga=0

        conn = list(nx.connected_components(self._grafo))
        connessa = list(max(conn, key=len))
        validi=[]
        for c in connessa:
            if self.hasM(c, m, min, anno_max):
                validi.append(c)

        if len(validi)<k:
            return [],0
        parziale=[]
        self.ricorsione(parziale,k,validi,0,min,anno_max)


        return self._percorsoSfigato,self._totSfiga

    def ricorsione(self,parziale,k,conn,index,min,max):

        if len(parziale)==k:
            sfiga=self.calcolaSfiga(parziale,min,max)
            if sfiga>self._totSfiga:
                self._totSfiga=sfiga
                self._percorsoSfigato=copy.deepcopy(parziale)
            return
        for i in range(index, len(conn)):
            parziale.append(conn[i])
            self.ricorsione(parziale ,k, conn, i + 1, min, max)
            parziale.pop()



    def hasM(self,costr,m,min,max):
        n=DAO.getCampionatiPerC(costr,min,max)
        if n>=m:
            return True
        return False
    def calcolaSfiga(self,parziale,min,max):
        sfiga=0
        for p in parziale:
            n=0
            d=0
            for i in range(min, max):
                n+=len(DAO.getResults(p.constructorId,i))
                d += len(DAO.getD(p.constructorId, i))
            if d>0:
                s=1-(n/d)
                sFloat=round(s,3)
                sfiga+=sFloat
        return sfiga

