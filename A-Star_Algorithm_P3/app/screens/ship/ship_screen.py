from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from app.components import balance_ship as BalanceShip
from app.components.data_types.container import Container
from app import search
from kivy.uix.label import Label

class ShipScreen(Screen):
    def on_pre_enter(self, *args):
        input_screen = self.manager.get_screen('input_screen')
        filepath = input_screen.ids.filechooser.selection[0]
        file = BalanceShip.ReadFile(filepath)
        manifest = BalanceShip.ParseFile(file)
        startGrid = BalanceShip.CreateGrid(manifest)
        DrawGrid(startGrid, self)
        solution = search.run_search(startGrid)

    def resize_cells(self, *args):
        grid = self.ids.grid

        if not grid.children:
            return
        
        rows = grid.rows
        cols = grid.cols

        # available square size
        cell = min(grid.width / cols, grid.height / rows)

        # apply to each child
        for child in grid.children:
            child.size = (cell, cell)

def DrawGrid(printGrid, shipScreen:ShipScreen):
    rows, cols = printGrid.shape

    grid = shipScreen.ids.grid
    grid.clear_widgets()
    
    for r in reversed(range(rows)):
        for c in range(cols):
            container:Container = printGrid[r, c]
            if (container.item == BalanceShip.UNUSED):
                color = [1, 1, 1, 1]
                weight_color = [0, 0, 0, 0]
            elif (container.item == BalanceShip.NAN):
                color = [0.1, 0.1, 0.1, 1]
                weight_color = [0, 0, 0, 0]
            else:
                color = [0.7, 0.85, 0.9, 1]
                weight_color = [1, 1, 1, 1]
            grid.add_widget(
                ContainerBox(
                    bg_color=color, 
                    weight=container.weight, 
                    weight_color=weight_color
                )
            )
    
    grid.rows = rows
    grid.cols = cols

    shipScreen.ids.grid.bind(size=shipScreen.resize_cells, children=shipScreen.resize_cells)
    
class ContainerBox(Widget):
    bg_color = ListProperty([1, 1, 1, 1])
    weight = NumericProperty()
    weight_color = ListProperty([0, 0, 0, 0])

class InstructionLabel(Label):
    text = "Computing a solution..."