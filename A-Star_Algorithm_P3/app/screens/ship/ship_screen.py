from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from app.components import balance_ship as BalanceShip
from app.components.data_types.container import Container
from app import search


class ShipScreen(Screen):
    instrStack = []
    solution = None

    def on_enter(self, *args):
        Window.bind(on_key_down=self.on_key_down)

    def on_leave(self, *args):
        Window.unbind(on_key_down=self.on_key_down)

    def on_pre_enter(self, *args):
        input_screen = self.manager.get_screen('input_screen')
        filepath = input_screen.ids.filechooser.selection[0]
        file = BalanceShip.ReadFile(filepath)
        manifest = BalanceShip.ParseFile(file)
        startGrid = BalanceShip.CreateGrid(manifest)
        DrawGrid(startGrid, self)

        self.ids.instruction_label.text = "Computing a solution..."
        solution:search.Node = search.run_search(startGrid)
        self.solution = solution
        curr:search.Node = solution
        self.ids.instruction_label.text = "Solution found. Press Enter to step through instructions."
        instrStack = []
        self.instrStack = instrStack
        while curr.parent != None:
            instructionText = WriteInstruction(curr.parent, curr)
            instrStack.append(instructionText)
            curr = curr.parent

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        # 13 = Enter, 271 = Numpad Enter
        if key in (13, 271):
            self.step_instruction()
        return True
    
    def step_instruction(self):
        if not self.instrStack:
            DrawGrid(self.solution.state, self)
            self.ids.instruction_label.text = "All steps complete."
            return

        curr = self.instrStack.pop()   # (text, node, r, c)
        text, node, current, target = curr 

        self.ids.instruction_label.text = text
        DrawGrid(node.state, self, current, target)

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

def WriteInstruction(parent:search.Node, child:search.Node):
    parentGrid = parent.state
    childGrid = child.state
    rows, cols = parentGrid.shape
    for r in range(rows):
        for c in range(cols):
            parentContainer:Container = parentGrid[r, c]
            childContainer:Container = childGrid[r, c]
            if parentContainer.item != childContainer.item and childContainer.item == BalanceShip.UNUSED:
                instruction = f"Move container from [color=00ff00]{parentContainer.coord}[/color] to "
                for r2 in range(rows):
                    for c2 in range(cols):
                        container3:Container = childGrid[r2, c2]
                        if parentContainer.item == container3.item:
                            instruction += f"[color=ff0000]{container3.coord}[/color]"
                            return instruction, parent, parentContainer.coord, container3.coord

    return f""

def DrawGrid(printGrid, shipScreen:ShipScreen, curCoord=None, targetCoord=None):
    rows, cols = printGrid.shape

    grid = shipScreen.ids.grid
    grid.clear_widgets()
    
    for r in reversed(range(rows)):
        for c in range(cols):
            container:Container = printGrid[r, c]
            if curCoord != None and r == curCoord.row and c == curCoord.col:
                color = [0, 1, 0, 1] # green
                weight_color = [0, 0, 0, 1] # black
            elif targetCoord != None and r == targetCoord.row and c == targetCoord.col:
                color = [1, 0, 0, 1] # red
                weight_color = [0, 0, 0, 0] # transparent
            elif (container.item == BalanceShip.UNUSED):
                color = [1, 1, 1, 1] # white
                weight_color = [0, 0, 0, 0] # transparent
            elif (container.item == BalanceShip.NAN):
                color = [0.1, 0.1, 0.1, 1] # dark gray
                weight_color = [0, 0, 0, 0] # transparent
            else:
                color = [0.7, 0.85, 0.9, 1] # light blue
                weight_color = [0, 0, 0, 1] # black
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
    markup = True
    text = StringProperty("Computing a solution...")