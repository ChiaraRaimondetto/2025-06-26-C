import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.minAnno=None
        self.maxAnno=None

    def handleBuildGraph(self, e):
        if self.minAnno is None or self.maxAnno is None:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(ft.Text("Selezionare il range di anni"))
            self._view.update_page()
            return
        try:
            intMin=int(self.minAnno)
            intMax=int(self.maxAnno)
            if intMin < intMax:
                self._model.buidGraph(intMin,intMax)
                n,a=self._model.infoGrafo()
                if n is not None and a is not None:
                    self._view._txtGraphDetails.controls.clear()
                    self._view._txtGraphDetails.controls.append(ft.Text(f"Grafo correttamente pesato con {n} nodi e {a} archi!"))
                else:
                    self._view._txtGraphDetails.controls.clear()
                    self._view._txtGraphDetails.controls.append(ft.Text("Non siamo riusciti a creare il grafo"))
                    self._view.update_page()
                    return
            else:
                self._view._txtGraphDetails.controls.clear()
                self._view._txtGraphDetails.controls.append(ft.Text("Selezionare il range di anni in modo decrestente"))
                self._view.update_page()
                return

        except ValueError:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(ft.Text("Non siamo riusciti a creare il grafo"))
            self._view.update_page()
            return
        self._view.update_page()


    def handlePrintDetails(self, e):
        res=self._model.stampaDetagli()
        if res is None:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(ft.Text("Non siamo riusciti ad avere informazioni sul grafo"))
            self._view.update_page()
            return
        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(ft.Text(f"La componente connessa maggiore è lunga {len(res)}nodi\n"
                                                       f"Di seguo i nodi in ordine decrescente in base al peso "))
        for r in res:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{r[0]} --> {r[1]}"))
        self._view.update_page()



    def handleCercaTeamSfortunati(self, e):
        m=self._view._txtInNumDiEdizioni.value
        k=self._view._txtInSoglia.value
        if m is None or k is None:
            self._view._txtInSoglia.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Inserire dei valori"))
            self._view.update_page()
            return
        try:
            intm = int(m)
            intk = int(k)
            intMin = int(self.minAnno)
            intMax = int(self.maxAnno)
            set,sfiga=self._model.worstPath(intk,intm,intMin,intMax)
            if set is not None and sfiga is not None:
                self._view._txt_result.controls.clear()
                self._view._txt_result.controls.append(ft.Text(f"Il set trovato ha lunghezza {len(set)} e ha una sfiga pari a {sfiga} "))
                for s in set:
                    self._view._txt_result.controls.append(ft.Text(f"{s.constructorRef} "))
            else:
                self._view._txt_result.controls.clear()
                self._view._txt_result.controls.append(ft.Text("Non siamo riusciti a creare il set, selezionare dei valor più piccoli"))
                self._view.update_page()
                return
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Inserire dei numeri interi"))
            self._view.update_page()
            return
        self._view.update_page()



    def fillDDYear(self):
        anni=self._model.getAllYears()
        for a in anni:
            self._view._ddYear1.options.append(ft.dropdown.Option(str(a)))
            self._view._ddYear2.options.append(ft.dropdown.Option(str(a)))
    def readYear1(self,e):
        self.minAnno=e.control.value
    def readYear2(self,e):
        self.maxAnno=e.control.value


