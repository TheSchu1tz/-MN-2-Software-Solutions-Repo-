from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from pathlib import Path
from app.components import balance_ship as BalanceShip
from app.components.data_types.container import Container
from app.components.data_types.coordinate import Coordinate
from app.utils.logger import Logger
from app import search

import time #delete later

class ShipScreen(Screen):
    instrStack = []
    filepath = ""
    solution = None
    prevInstruction = None
    instructionCount = 0
    solutionWritten = False
    pausedForLog = False
    logger:Logger = None

    def SetLogger(self, logger):
        self.logger = logger

    def on_enter(self, *args):
        Window.bind(on_key_down=self.on_key_down)

    def on_leave(self, *args):
        Window.unbind(on_key_down=self.on_key_down)

    def on_pre_enter(self, *args):
        if self.pausedForLog:
            # We are returning from the log screen → do NOT reset anything
            self.pausedForLog = False
            log_screen = self.manager.get_screen("log_screen")
            log_message = log_screen.ids.log_input.text 
            self.logger.LogMessage(log_message)
            return
    
        self.instructionCount = 0
        self.solutionWritten = False
        self.prevInstruction = None
        input_screen = self.manager.get_screen('input_screen')
        self.filepath = input_screen.ids.filechooser.selection[0]
        file = BalanceShip.ReadFile(self.filepath)
        manifest = BalanceShip.ParseFile(file)
        startGrid = BalanceShip.CreateGrid(manifest)
        #TODO: log containers on ship
        numContainers = BalanceShip.NumContainers(startGrid)
        filename = Path(self.filepath).name
        self.logger.LogManifestStart(filename, numContainers)
        DrawGrid(startGrid, self)

        self.ids.instruction_label.text = (f"{filename} has {numContainers} containers\n"
            f"Computing a solution..."
        )
        start = time.time()
        solution, expanded_nodes = search.run_search(startGrid)
        end = time.time()
        print(f"Took {end - start} secs to find solution of depth {solution.depth}")
        print(f"Expanded {expanded_nodes} nodes")

        self.solution = solution
        self.logger.LogSolutionFound(solution.depth, solution.f_func)
        curr:search.Node = solution
        if (solution.depth == 0):
            solutionName = WriteSolutionFile(self.solution.state, self.filepath)
            self.ids.instruction_label.text = (f"Ship is already balanced. Outbound manifest written to desktop as:"
                                               + f"\n[b][color=ffff00]{solutionName}[/color][/b]"
                                               + f"\nDon't forget to email it to the captain."
                                               + f"\nPress [color=ffff00][b]Enter[/b][/color] when done.")
            self.solutionWritten = True
            self.logger.LogCycleEnd(solutionName)
        else:
            self.ids.instruction_label.text = (
                f"Solution found. It will take [b][color=ffff00]{solution.depth}[/color][/b] moves and [b][color=ffff00]{solution.f_func}[/color][/b] minutes [i](not including crane parking).[/i]"
            + "\n          - Press [color=ffff00][b]Enter[/b][/color] to step through instructions."
            + "\n          - Press [color=ffff00][b]Esc[/b][/color] to log a message.\n")
            instrStack = []
            self.instrStack = instrStack
            while curr.parent != None:
                instructionText = WriteInstruction(curr.parent, curr)
                instrStack.append(instructionText)
                curr = curr.parent if curr.parent != None else curr
            instrStack.append(WriteBeginInstruction(instrStack[-1], startGrid))
            end = WriteEndInstruction(instrStack[0], solution.state)
            instrStack.insert(0, end)

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        # 27 = Esc key 
        if key == 27:   # ESC
            self.pausedForLog = True
            self.manager.current = "log_screen"
            return True
        
        # 13 = Enter, 271 = Numpad Enter
        if key in (13, 271):
            self.step_instruction()
        return True
    
    def step_instruction(self):
        self.instructionCount += 1
        if self.solutionWritten:
            self.manager.current = "input_screen"
            return

        if not self.instrStack:
            DrawGrid(self.solution.state, self)
            solutionName = WriteSolutionFile(self.solution.state, self.filepath)
            self.ids.instruction_label.text = (f"All steps complete. Outbound manifest written to desktop as:"
                                               + f"\n[b][color=ffff00]{solutionName}[/color][/b]"
                                               + f"\nDon't forget to email it to the captain."
                                               + f"\nPress [color=ffff00][b]Enter[/b][/color] when done.")
            self.solutionWritten = True
            self.logger.LogCycleEnd(solutionName)
            return

        if self.prevInstruction is not None:
            if self.prevInstruction[2].row != BalanceShip.GRID_ROWS:
                self.logger.LogMove(self.prevInstruction[2], self.prevInstruction[3])
        curr = self.instrStack.pop()   # (text, node, current, target)
        text, node, current, target = curr 
        self.prevInstruction = curr

        self.ids.instruction_label.text += f"\n{self.instructionCount}. " + text
        if isinstance(node, search.Node):
            DrawGrid(node.state, self, current, target)
        else:
            DrawGrid(node, self, current, target)

    def resize_cells(self, *args):
        grid = self.ids.grid

        if not grid.children:
            return
        
        rows = grid.rows + 1
        cols = grid.cols

        # available square size
        cell = min(grid.width / cols, grid.height / rows)

        # apply to each child
        for child in grid.children:
            child.size = (cell, cell)

# writes an instruction to go from park to first node
def WriteBeginInstruction(firstInstruction, startGrid):
    firstCoord = firstInstruction[2]
    rows = startGrid.shape[0]

    instruction = f"Move crane from [color=00ff00]PARK[/color] to [color=ff0000]{firstCoord}[/color]"

    return instruction, startGrid, Coordinate(rows, 0), firstCoord 

# writes an instruction to go from parent node to child node
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

# writes an instruction to go from last node to park
def WriteEndInstruction(lastInstruction, solutionGrid):
    lastCoord = lastInstruction[3]
    rows = solutionGrid.shape[0]

    instruction = f"Move crane from [color=00ff00]{lastCoord}[/color] to [color=ff0000]PARK[/color]"

    return instruction, solutionGrid, lastCoord, Coordinate(rows, 0)

# draws the grid, and highlights the cur and target coordinates if they are provided
def DrawGrid(printGrid, shipScreen:ShipScreen, curCoord=None, targetCoord=None):
    rows, cols = printGrid.shape

    grid = shipScreen.ids.grid
    grid.clear_widgets()

    for r in reversed(range(rows + 1)):  
        for c in range(cols):

            # top row (the new one)
            if r == rows:
                if c == 0 and curCoord is not None and curCoord.row == rows: 
                    color = [0, 1, 0, 1]  # green
                    weight_color = [0, 0, 0, 0]
                elif c == 0 and targetCoord is not None and targetCoord.row == rows:
                    color = [1, 0, 0, 1]  # red
                    weight_color = [0, 0, 0, 0]
                elif c == 0:
                    color = [1, 1, 1, 1]  # white
                    weight_color = [0, 0, 0, 0]
                else:       # rest transparent
                    color = [0, 0, 0, 0]
                    weight_color = [0, 0, 0, 0]

                grid.add_widget(
                    ContainerBox(
                        bg_color=color,
                        weight=0,
                        weight_color=weight_color
                    )
                )
                continue

            # Normal grid rows
            container:Container = printGrid[r, c]

            # handling cur (normal vs park)
            if curCoord is not None and r == curCoord.row and c == curCoord.col and container.item != BalanceShip.UNUSED:
                color = [0, 1, 0, 1]  # green
                weight_color = [0, 0, 0, 1]
            elif curCoord is not None and r == curCoord.row and c == curCoord.col:
                color = [0, 1, 0, 1]  # green
                weight_color = [0, 0, 0, 0]
            # handling target (normal vs park)
            elif targetCoord is not None and r == targetCoord.row and c == targetCoord.col and container.item != BalanceShip.UNUSED:
                color = [1, 0, 0, 1]  # red
                weight_color = [0, 0, 0, 1]
            elif targetCoord is not None and r == targetCoord.row and c == targetCoord.col:
                color = [1, 0, 0, 1]  # red
                weight_color = [0, 0, 0, 0]
            # handling normal grid spaces
            elif container.item == BalanceShip.UNUSED:
                color = [1, 1, 1, 1]  # white
                weight_color = [0, 0, 0, 0]
            elif container.item == BalanceShip.NAN:
                color = [0.1, 0.1, 0.1, 1]
                weight_color = [0, 0, 0, 0]
            else:
                color = [0.7, 0.85, 0.9, 1]
                weight_color = [0, 0, 0, 1]

            grid.add_widget(
                ContainerBox(
                    bg_color=color,
                    weight=container.weight,
                    weight_color=weight_color
                )
            )

    # tell Kivy how many rows really exist
    grid.rows = rows + 1
    grid.cols = cols

    shipScreen.ids.grid.bind(
        size=shipScreen.resize_cells,
        children=shipScreen.resize_cells
    )

def WriteSolutionFile(solution, filepath):
    p = Path(filepath)

    out_dir = Path("p3_solutions")
    out_dir.mkdir(parents=True, exist_ok=True)

    flatSolution = solution.flat
    with open(out_dir / (p.stem + "OUTBOUND.txt"), "w") as new_file:
        for i, container in enumerate(flatSolution):
            line = f"{container.coord}, {{{container.weight:05}}}, {container.item}"
            if i != len(flatSolution) - 1:  # not last
                line += "\n"
            new_file.write(line)
    new_file.close()
    return (p.stem + "OUTBOUND.txt")

class ContainerBox(Widget):
    bg_color = ListProperty([1, 1, 1, 1])
    weight = NumericProperty()
    weight_color = ListProperty([0, 0, 0, 0])

class InstructionLabel(Label):
    markup = True
    text = StringProperty("Computing a solution...")