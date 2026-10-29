from database.DB_connect import DBConnect
from model.artista import Artista


"""
1. All’avvio, riempire un menu a tendina con i paesi dei clienti 
(campo Country della tabella Customer), in ordine alfabetico.
2. L’utente sceglie un paese P e inserisce in un campo di testo un 
intero K ≥ 1. Premendo “Crea Grafo”, l’applicazione costruisce un grafo semplice,
 non orientato e pesato: a) i nodi sono gli artisti (tabella Artist)
  di cui i clienti del paese P hanno acquistato almeno K brani in totale
(somma di Quantity di InvoiceLine, passando per Track e Album).
 Per ogni artista si memorizzino:
    * il numero di brani venduti nel paese P;
    * il ricavo nel paese P (somma di UnitPrice × Quantity);
    * l’insieme dei clienti del paese P che hanno acquistato almeno un suo brano;
    * il suo genere principale, cioè il genere con più brani dell’artista in
tutto il catalogo (tabella Track). A parità vince il GenreId minore; b) due
 artisti sono collegati da un arco se almeno un cliente del paese P ha acquistato brani
  di entrambi; c) il peso dell’arco è il numero di clienti distinti in comune.
3. Stampare il numero di nodi e di archi. Riempire poi un menu a tendina con gli artisti del grafo,
 in ordine alfabetico.
4. Premendo “Stampa Info”, stampare: a) l’artista con più brani venduti e il numero; b)
 l’artista con il ricavo maggiore e il ricavo, con due decimali; c) l’artista con grado maggiore e il grado; d) i
  5 archi di peso maggiore, in ordine decrescente di peso. A parità si ordina alfabeticamente per il nome del primo artista e poi del secondo; e) il numero di componenti connesse e la dimensione della più grande; f) il numero di generi principali diversi tra i nodi, e il genere principale più frequente con il numero di artisti.
PUNTO 2
Si vuole organizzare una rassegna musicale per il paese P. L’utente sceglie un artista di partenza dal menu e inserisce un intero N, con 2 ≤ N ≤ 5. Con un algoritmo ricorsivo, trovare un gruppo di artisti che rispetta tutti questi vincoli:
1. contiene esattamente N artisti;
2. contiene l’artista di partenza;
3. è connesso: ogni artista aggiunto deve essere adiacente ad almeno uno degli artisti già presenti nel gruppo;
4. gli artisti hanno tutti generi principali diversi.
Tra tutti i gruppi ammissibili, scegliere quello che raggiunge più clienti distinti, cioè quello con l’unione degli insiemi di clienti più grande. A parità di clienti, si sceglie quello con il numero totale di brani venduti maggiore.
Stampare gli artisti del gruppo in ordine alfabetico, ciascuno con genere principale e brani venduti, poi il numero di clienti distinti raggiunti e il totale dei brani venduti. Se il gruppo non esiste, stampare un messaggio opportuno.



"""

class DAO():

    @staticmethod
    def getCountry():
        """Paesi dei clienti, in ordine alfabetico."""
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT c.Country AS paese
                FROM Customer c
                ORDER BY c.Country
                """
        cursor.execute(query)
        for row in cursor:
            results.append(row["paese"])
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(paese, minimo):
        """Artisti con almeno 'minimo' brani venduti nel paese, con brani venduti e ricavo."""
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT a.ArtistId AS id, a.Name AS nome,
                       SUM(il.Quantity) AS numero, SUM(il.UnitPrice * il.Quantity) AS ricavo
                FROM Artist a, Album ab, Track t, InvoiceLine il, Invoice i, Customer c
                WHERE a.ArtistId = ab.ArtistId AND ab.AlbumId = t.AlbumId
                  AND t.TrackId = il.TrackId AND il.InvoiceId = i.InvoiceId
                  AND i.CustomerId = c.CustomerId AND c.Country = %s
                GROUP BY a.ArtistId, a.Name
                HAVING SUM(il.Quantity) >= %s
                """
        cursor.execute(query, (paese, minimo))
        for row in cursor:
            results.append(Artista(row["id"], row["nome"], int(row["numero"]), float(row["ricavo"])))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppia(paese):
        """Coppie (artista, cliente) del paese: il cliente ha comprato almeno un brano dell'artista."""
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT a.ArtistId AS ida, i.CustomerId AS idC
                FROM Artist a, Album ab, Track t, InvoiceLine il, Invoice i, Customer c
                WHERE a.ArtistId = ab.ArtistId AND ab.AlbumId = t.AlbumId
                  AND t.TrackId = il.TrackId AND il.InvoiceId = i.InvoiceId
                  AND i.CustomerId = c.CustomerId AND c.Country = %s
                """
        cursor.execute(query, (paese,))
        for row in cursor:
            results.append((row["ida"], row["idC"]))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getGeneriArtisti():
        """(artista, genere, numero brani) su tutto il catalogo.
        Per ogni artista la prima riga è il genere principale."""
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ab.ArtistId AS idA, t.GenreId AS idG, COUNT(*) AS numero
                FROM Album ab, Track t
                WHERE ab.AlbumId = t.AlbumId
                GROUP BY ab.ArtistId, t.GenreId
                ORDER BY ab.ArtistId, numero DESC, t.GenreId
                """
        cursor.execute(query)
        for row in cursor:
            results.append((row["idA"], row["idG"], row["numero"]))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getGeneri():
        """Dizionario {GenreId: nome}."""
        conn = DBConnect.get_connection()
        results = {}
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = "SELECT GenreId AS id, Name AS nome FROM Genre"
        cursor.execute(query)
        for row in cursor:
            results[row["id"]] = row["nome"]
        cursor.close()
        conn.close()
        return results