## tk_flow
tk_flow is a python library structure to have the simplest flowchart capabilities using the existing tkinter library to produce the imagery and containing the ability to export the generated graphics to a pdf format.






## Function Usage
Currently this function can create different flowchart block shapes:
- rectangle
- oval
- diamond
- hexagon

The current shapes are the core flowchart items, each shape can be modified uniformly, with two rectangle options to have variants of the rectangle. 

```python
from tk_flow import Flowchart
import tkinter as tk

# Set up window
root = tk.Tk()
example_flowchart = Flowchart() 


# Node Creation
start = example_flowchart.node(col = 2, row = 0, text = 'Start', shape = 'terminal_start')
end = example_flowchart.node(col = 2,row = 4, text = 'End', shape = 'terminal_end')

example_flowchart.connect(node1 = start, direction1 = 's' , node2 = end, direction2 = 'n' , style = 'arrow' )

```


## Shapes/NodeTypes
- point (blank space to anchor lines in the flow)
- title
- label
- terminal_start (oval type node, designated as start node, by default filled green)
- terminal_end (oval type node, designated as end node, by default filled red)
- rectangle
- rectangle2
- diamond
- hexagon
- oval


## Formatting
Most of the formating Items are stored in a dictionary and can be edited individually.
```python
default_colors = {
            "oval": "lightblue",
            "rectangle": "lightgrey",
            "rectangle2": "lightbrown",
            "diamond": "lightgreen",
            "hexagon": "lightyellow",
            "terminal_start": "green",
            "terminal_end": "red"
        }

default_outlines = {
            "oval": {"color": "black", "thickness": 2},
            "rectangle": {"color": "black", "thickness": 2},
            "rectangle2": {"color": "black", "thickness": 2},
            "diamond": {"color": "black", "thickness": 2},
            "hexagon": {"color": "black", "thickness": 2},
            "terminal_start": {"color": "black", "thickness": 2},
            "terminal_end": {"color": "black", "thickness": 2}
        }

default_fonts = {
            "oval": {"font": "Courier", "size": 24, "color": "black", "weight": "normal", "underline" : False},
            "rectangle": {"font": "Courier", "size": 24, "color": "black", "weight": "normal", "underline" : False},
            "rectangle2": {"font": "Courier", "size": 24, "color": "black", "weight": "bold", "underline" : False},
            "diamond": {"font": "Courier", "size": 24, "color": "black", "weight": "normal", "underline" : False},
            "hexagon": {"font": "Courier", "size": 24, "color": "black", "weight": "normal", "underline" : False},
            "label": {"font": "Courier", "size": 18, "color": "black", "weight": "bold", "underline" : False},
            "terminal_start": {"font": "Courier", "size": 66, "color": "black", "weight": "bold", "underline" : False},
            "terminal_end": {"font": "Courier", "size": 66, "color": "black", "weight": "bold", "underline" : False},
            "title": {"font": "Courier", "size": 72, "color": "black", "weight": "bold", "underline" : False}
        }

default_connectors = {
            "color": "black",
            "thickness": 2
        }


```


## Input Variables
```python
#input variable options
Flowchart(
   root,
   title="Flowchart Creator",
   grid_width=100,
   grid_height=100,
   grid_pad=0.15,
   colors=None,
   outlines=None,
   fonts=None,
   connectors=None,
   spacing=50,
   node_width=150,
   node_height=90,
   label_width=25,
   label_height=10
)
```   
