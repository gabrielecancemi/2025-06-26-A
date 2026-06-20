import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.idCircuiti = dict()
        self.circuitiValidi = []
        self.usabili = []
        self.imprevistiMax = 0
        self.sottocircuito = []

    def getAnni(self):
        return DAO.getAnni()

    def creaGrafo(self, inizio, fine):
        self._grafo.clear()
        nodi = DAO.getNodi()

        for n in nodi:
            n.risultati = DAO.getPiazzamenti(inizio, fine, n.circuitId)
            print(n)
            self.idCircuiti[n.circuitId] = n
            self._grafo.add_node(n)

        for a, b in itertools.combinations(self.idCircuiti.values(), 2):
            for y in a.risultati.keys():
                if b.risultati.get(y, None) is not None:
                    w = 0
                    for anno in a.risultati.values():
                        for piazzamento in anno:
                            if piazzamento.posizione is not None:
                                w += 1
                    for anno in b.risultati.values():
                        for piazzamento in anno:
                            if piazzamento.posizione is not None:
                                w += 1
                    self._grafo.add_edge(a, b, weight = w)

    def dimensioniGrafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def cercaComponente(self):
        comp = list(nx.connected_components(self._grafo))
        maggiore = comp[0] if len(comp)>0 else []
        res = []
        for n in maggiore:
            self.circuitiValidi.append(n)
            mas = 0
            for v in self._grafo.neighbors(n):
                peso = self._grafo[n][v]["weight"]
                if peso > mas:
                    mas = peso
            res.append((n, mas))

        res.sort(key = lambda x : x[1], reverse=True)

        return res

    def campionato(self, k, m):
        usabili = []
        for n in self.circuitiValidi:
            if len(n.risultati.keys()) >= m:
                usabili.append(n)
        self.usabili = usabili
        self.ricorsione([], k)
        return self.sottocircuito, self.imprevistiMax

    def ricorsione(self, parziale, k):
        print("qui")
        if len(parziale) == k:
            imprevisti = self.calcolaImprevisti(parziale)
            if self.imprevistiMax < imprevisti:
                self.imprevistiMax = imprevisti
                self.sottocircuito = copy.deepcopy(parziale)
        else:
            for cir in self.usabili:
                if cir not in parziale:
                    parziale.append(cir)
                    self.ricorsione(parziale, k)
                    parziale.pop()

    def calcolaImprevisti(self, parziale):
        i = 0
        for c in parziale:
            np = 0
            ntot = 0
            for anno in c.risultati.values():
                for piazzamento in anno:
                    ntot += 1
                    if piazzamento.posizione is not None:
                        np += 1
            i += (1 - (np/ntot))
        return i


