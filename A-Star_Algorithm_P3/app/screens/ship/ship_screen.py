from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from components import balance_ship as BalanceShip
from components.data_types.container import Container
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import NumericProperty

class ShipScreen(Screen):
    def on_pre_enter(self, *args):
        input_screen = self.manager.get_screen('input_screen')
        filepath = input_screen.ids.filechooser.selection[0]
        file = BalanceShip.ReadFile(filepath)
        manifest = BalanceShip.ParseFile(file)
        startGrid = BalanceShip.CreateGrid(manifest)
        
        rows, cols = startGrid.shape
        
        grid = self.ids.grid
        grid.clear_widgets()
        
        for r in reversed(range(rows)):
            for c in range(cols):
                container:Container = startGrid[r, c]
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

        self.ids.grid.bind(size=self.resize_cells, children=self.resize_cells)

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

class ContainerBox(Widget):
    bg_color = ListProperty([1, 1, 1, 1])
    weight = NumericProperty()
    weight_color = ListProperty([0, 0, 0, 0])