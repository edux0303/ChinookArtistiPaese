import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Chinook - Artisti per paese"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._ddCountry = None
        self._txtK = None
        self._btnCreaGrafo = None
        self._btnStampaInfo = None
        self._ddArtista = None
        self._txtN = None
        self._btnGruppo = None
        self._txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Chinook - Artisti per paese", color="blue", size=24)
        self._page.controls.append(self._title)

        # ROW 1: paese + K + crea grafo + stampa info
        self._ddCountry = ft.Dropdown(label="Paese")
        self._txtK = ft.TextField(label="Min brani venduti K", value="3")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                               on_click=self._controller.handleCreaGrafo)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa Info",
                                                on_click=self._controller.handleStampaInfo)
        row1 = ft.Row([ft.Container(self._ddCountry, width=220),
                       ft.Container(self._txtK, width=180),
                       ft.Container(self._btnCreaGrafo, width=150),
                       ft.Container(self._btnStampaInfo, width=150)],
                      alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)
        self._page.controls.append(row1)

        # ROW 2: punto 2
        self._ddArtista = ft.Dropdown(label="Artista di partenza")
        self._txtN = ft.TextField(label="Numero artisti N (2-5)")
        self._btnGruppo = ft.ElevatedButton(text="Trova rassegna",
                                            on_click=self._controller.handleGruppo)
        row2 = ft.Row([ft.Container(self._ddArtista, width=300),
                       ft.Container(self._txtN, width=180),
                       ft.Container(self._btnGruppo, width=180)],
                      alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)

        # riempio il menu dei paesi all'avvio
        self._controller.fillDDCountry()

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()