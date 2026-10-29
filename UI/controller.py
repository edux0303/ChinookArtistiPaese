import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view._txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDDCountry(self):
        for paese in self._model.getCountry():
            self._view._ddCountry.options.append(ft.dropdown.Option(key=paese, text=paese))

    # ==================== PUNTO 1 ====================

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        # 1. paese
        if self._view._ddCountry.value is None:
            self._errore("Selezionare un paese!")
            return
        country = self._view._ddCountry.value

        # 2. K
        try:
            numero = int(self._view._txtK.value)
        except (ValueError, TypeError):
            self._errore("K deve essere un numero intero!")
            return
        if numero < 1:
            self._errore("K deve essere almeno 1!")
            return

        # 3. creo il grafo
        self._model.buildGraph(country, numero)
        if self._model.getNumNodi() == 0:
            self._errore(f"Nessun artista con almeno {numero} brani venduti in {country}!")
            return

        # 4. stampo nodi e archi
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        # 5. riempio il dropdown degli artisti (punto 2)
        self._view._ddArtista.options.clear()
        self._view._ddArtista.value = None
        for a in self._model.getNodiOrdinati():
            self._view._ddArtista.options.append(ft.dropdown.Option(key=str(a.id), text=str(a)))

        self._view.update_page()

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # a) più brani venduti
        artista, numero = self._model.getBraniPiuVenduti()
        self._view._txt_result.controls.append(
            ft.Text(f"Artista con più brani venduti: {artista} ({numero} brani)"))

        # b) ricavo maggiore
        artista, ricavo = self._model.getRicavoMaggiore()
        self._view._txt_result.controls.append(
            ft.Text(f"Artista con ricavo maggiore: {artista} ({ricavo:.2f})"))

        # c) grado maggiore
        artista, grado = self._model.getGradoMaggiore()
        self._view._txt_result.controls.append(
            ft.Text(f"Artista con grado maggiore: {artista} (grado: {grado})"))

        # d) top 5 archi
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(ft.Text("Top 5 archi di peso maggiore:"))
        for i, (n1, n2, peso) in enumerate(self._model.getTop5(), start=1):
            self._view._txt_result.controls.append(
                ft.Text(f"{i}. {n1} -- {n2} (clienti in comune: {peso})"))

        # e) componenti connesse
        numComp, dimMax = self._model.getComponenti()
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di componenti connesse: {numComp}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Dimensione della componente più grande: {dimMax}"))

        # f) generi principali
        numGeneri, idG, numArt = self._model.getGeneriInfo()
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Generi principali diversi: {numGeneri}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Genere più frequente: {self._model.getNomeGenere(idG)} ({numArt} artisti)"))

        self._view.update_page()

    # ==================== PUNTO 2 ====================

    def handleGruppo(self, e):
        self._view._txt_result.controls.clear()

        # 1. il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # 2. artista di partenza
        if self._view._ddArtista.value is None:
            self._errore("Selezionare un artista di partenza!")
            return
        partenza = self._model.getArtista(int(self._view._ddArtista.value))
        if partenza is None:
            self._errore("Artista non presente nel grafo, ricreare il grafo!")
            return

        # 3. N
        try:
            n = int(self._view._txtN.value)
        except (ValueError, TypeError):
            self._errore("N deve essere un numero intero!")
            return
        if n < 2 or n > 5:
            self._errore("N deve essere compreso tra 2 e 5!")
            return

        # 4. ricorsione
        gruppo, clienti, brani = self._model.getGruppo(partenza, n)

        # 5. stampa
        if len(gruppo) == 0:
            self._errore(f"Nessun gruppo di {n} artisti connesso e con generi diversi "
                         f"partendo da {partenza}")
            return

        self._view._txt_result.controls.append(
            ft.Text(f"Rassegna di {n} artisti (partenza: {partenza}):"))
        for a in sorted(gruppo, key=lambda x: str(x)):
            self._view._txt_result.controls.append(
                ft.Text(f"- {a} - genere: {self._model.getNomeGenere(a.genere)}, "
                        f"brani venduti: {a.numeroBrani}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Clienti distinti raggiunti: {clienti}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Totale brani venduti: {brani}"))

        self._view.update_page()