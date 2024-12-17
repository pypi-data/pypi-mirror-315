from tk_flow import Flowchart
import tkinter as tk


# Set up window
root = tk.Tk()
example_flowchart = Flowchart()


# Node Creation
start = example_flowchart.node(col = 2, row = 0, text = 'Start', shape = 'terminal_start')
input_1 = example_flowchart.node(col = 2, row = 1, text = 'Input', shape = 'hexagon')
decision = example_flowchart.node(col = 2, row = 2, text = 'Process 1\nor\nProcess 2?', shape = 'diamond')
process_1 = example_flowchart.node(col = 1, row = 3, text = 'Process 1', shape = 'rectangle')
process_2 = example_flowchart.node(col = 3, row = 3, text = 'Process 2', shape = 'rectangle2' )
end = example_flowchart.node(col = 2,row = 4, text = 'End', shape = 'terminal_end')

# Connector Label Creation
decision_1 = example_flowchart.node(col = 1.5, row = 2, text = '1', shape = 'label')
decision_2 = example_flowchart.node(col = 2.5, row = 2, text = '2', shape = 'label')

# Connection Point Creation
decision_1_point = example_flowchart.node(col = 1, row = 2)
decision_2_point = example_flowchart.node(col = 3, row = 2)


# Connecting Nodes
example_flowchart.connect(node1 = start, direction1 = 's' , node2 = input_1 , direction2 = 'n' , style = 'arrow' )
example_flowchart.connect(node1 = input_1, direction1 = 's' , node2 = decision , direction2 = 'n' , style = 'arrow')
example_flowchart.connect(node1 = decision, direction1 = 'w', node2 = decision_1, direction2 = 'e')
example_flowchart.connect(node1 = decision, direction1 = 'e', node2 = decision_2, direction2 = 'w')
example_flowchart.connect(node1 = decision_1, direction1 = 'w', node2 = decision_1_point, direction2 = 'c')
example_flowchart.connect(node1 = decision_2, direction1 = 'e', node2 = decision_2_point, direction2 = 'c')
example_flowchart.connect(node1 = decision_1_point, direction1 = 'c', node2 = process_1, direction2 = 'n', style = 'arrow')
example_flowchart.connect(node1 = decision_2_point, direction1 = 'c', node2 = process_2, direction2 = 'n', style = 'arrow')
example_flowchart.connect(node1 = process_1, direction1 = 's', node2 = end, direction2 = 's', style = 'arrow')
example_flowchart.connect(node1 = process_2, direction1 = 's', node2 = end, direction2 = 's', style = 'arrow')


root.mainloop()