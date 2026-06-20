import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleBuildGraph(self, e):
        self._view._txtGraphDetails.controls.clear()
        inizio = self._view._ddYear1.value
        fine = self._view._ddYear2.value

        if inizio is None or fine is None or inizio == "" or fine == "":
            self._view._txtGraphDetails.controls.append(ft.Text("Inserire gli anni", color="red"))
            self._view.update_page()
            return
        if inizio > fine:
            self._view._txtGraphDetails.controls.append(ft.Text("Inserire anni crescenti", color="red"))
            self._view.update_page()
            return
        self._model.creaGrafo(inizio, fine)
        self._view._txtGraphDetails.controls.append(ft.Text("Grafo correttamente creato.", color="green"))
        n, m = self._model.dimensioniGrafo()
        self._view._txtGraphDetails.controls.append(ft.Text(f"Il grafo contiene {n} nodi e {m} archi"))
        self._view.update_page()

    def handlePrintDetails(self, e):
        self._view._txtGraphDetails.controls.clear()
        nodi = self._model.cercaComponente()
        for n in nodi:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{n[0]} -- {n[1]}"))
        self._view._btnCalcolaSoluzione.disabled = False
        self._view.update_page()

    def handleCercaDreamChampionship(self, e):
        self._view._txt_result.controls.clear()
        k = self._view._txtInSoglia.value
        m = self._view._txtInNumDiEdizioni.value

        if k == "" or k is None or m == "" or m is None:
            self._view._txt_result.controls.append(ft.Text("Inserire i valori", color="red"))
            self._view.update_page()
            return
        try:
            k = int(k)
            m = int(m)
        except:
            self._view._txt_result.controls.append(ft.Text("Inserire valori interi", color="red"))
            self._view.update_page()
            return

        if k <0  or m<0:
            self._view._txt_result.controls.append(ft.Text("Inserire valori positivi", color="red"))
            self._view.update_page()

        campionato, imprevisti = self._model.campionato(k, m)
        self._view._txt_result.controls.append(ft.Text(f"Sottocampionato con indice {imprevisti}", color="green"))
        for c in campionato:
            self._view._txt_result.controls.append(ft.Text(f"{c}"))
        self._view.update_page()

    def fillDdYears(self):
        anni = self._model.getAnni()
        for a in anni:
            self._view._ddYear1.options.append(ft.dropdown.Option(a))
            self._view._ddYear2.options.append(ft.dropdown.Option(a))





