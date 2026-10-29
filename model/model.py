import networkx as nx
from itertools import combinations
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._nomiGeneri = DAO.getGeneri()      # {GenreId: nome}
        # punto 2
        self._solBest = []
        self._clientiBest = -1
        self._braniBest = -1
        self._visti = set()
        self._N = 0

    # ==================== PUNTO 1 ====================

    def getCountry(self):
        return DAO.getCountry()

    def buildGraph(self, paese, minimo):
        self._grafo.clear()
        self._idMap = {}

        # nodi: artisti con almeno 'minimo' brani venduti nel paese
        nodi = DAO.getNodi(paese, minimo)
        self._idMap = {a.id: a for a in nodi}
        self._grafo.add_nodes_from(nodi)

        # set dei clienti di ogni artista
        for idA, idC in DAO.getCoppia(paese):
            if idA in self._idMap:
                self._idMap[idA].clienti.add(idC)

        # genere principale: la prima riga di ogni artista (query già ordinata)
        for idA, idG, numero in DAO.getGeneriArtisti():
            if idA in self._idMap and self._idMap[idA].genere is None:
                self._idMap[idA].genere = idG

        # archi: clienti in comune, peso = numero di clienti in comune
        for a1, a2 in combinations(nodi, 2):
            comuni = a1.clienti & a2.clienti
            if len(comuni) > 0:
                self._grafo.add_edge(a1, a2, weight=len(comuni))

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda a: str(a))

    def getArtista(self, idA):
        return self._idMap.get(idA)

    def getNomeGenere(self, idG):
        return self._nomiGeneri.get(idG, "sconosciuto")

    # a) artista con più brani venduti
    def getBraniPiuVenduti(self):
        best = max(self._grafo.nodes, key=lambda a: a.numeroBrani)
        return best, best.numeroBrani

    # b) artista con ricavo maggiore
    def getRicavoMaggiore(self):
        best = max(self._grafo.nodes, key=lambda a: a.ricavo)
        return best, best.ricavo

    # c) artista con grado maggiore
    def getGradoMaggiore(self):
        best = max(self._grafo.nodes, key=lambda a: self._grafo.degree(a))
        return best, self._grafo.degree(best)

    # d) 5 archi di peso maggiore
    def getTop5(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            nomi = sorted([str(u), str(v)])
            archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0], x[1]))
        return archi[:5]

    # e) componenti connesse
    def getComponenti(self):
        componenti = list(nx.connected_components(self._grafo))
        piuGrande = max(componenti, key=len)
        return len(componenti), len(piuGrande)

    # f) generi principali diversi e genere più frequente
    def getGeneriInfo(self):
        conta = {}
        for a in self._grafo.nodes:
            conta[a.genere] = conta.get(a.genere, 0) + 1
        best = max(conta, key=lambda g: conta[g])
        return len(conta), best, conta[best]

    # ==================== PUNTO 2 ====================

    def getGruppo(self, partenza, N):
        self._solBest = []
        self._clientiBest = -1
        self._braniBest = -1
        self._visti = set()
        self._N = N
        self._ricorsione([partenza])
        return self._solBest, self._clientiBest, self._braniBest

    def _ricorsione(self, parziale):
        # 0. gruppo già visto in un altro ordine -> mi fermo
        chiave = frozenset(parziale)
        if chiave in self._visti:
            return
        self._visti.add(chiave)

        # 1. caso terminale: il gruppo ha N artisti
        if len(parziale) == self._N:
            tutti = set()
            for a in parziale:
                tutti.update(a.clienti)  # aggiungo tutti i clienti dell'artista a
            clienti = len(tutti)
            brani = sum(a.numeroBrani for a in parziale)
            if (clienti > self._clientiBest or
                    (clienti == self._clientiBest and brani > self._braniBest)):
                self._solBest = list(parziale)
                self._clientiBest = clienti
                self._braniBest = brani
            return

        # 2. candidati: vicini degli artisti già nel gruppo
        candidati = set()
        for p in parziale:
            for v in self._grafo.neighbors(p):
                if self._ammissibile(v, parziale):
                    candidati.add(v)

        # 3. provo ad aggiungere ogni candidato
        for c in sorted(candidati, key=lambda x: -x.numeroBrani):
            parziale.append(c)
            self._ricorsione(parziale)
            parziale.pop()

    def _ammissibile(self, c, parziale):
        if c in parziale:
            return False
        for p in parziale:
            if p.genere == c.genere:
                return False
        return True


