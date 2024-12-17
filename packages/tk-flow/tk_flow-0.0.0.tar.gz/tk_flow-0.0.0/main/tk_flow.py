import tkinter as tk
from tkinter import Scrollbar
import math
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from tkinter import filedialog
import os
from tkinter.font import Font


class Flowchart:
    def __init__(self, root, title="Flowchart Creator", grid_width=100, grid_height=100, grid_pad=0.15, colors=None, outlines=None, fonts=None, connectors=None, spacing=50, node_width=150, node_height=90, label_width=25, label_height=10):
        self.root = root
        self.root.title(title)

        # Grid properties
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.pad = grid_pad

        #  Node Properties
        self.node_width = node_width
        self.node_height = node_height

        # Label Properties
        self.label_width = label_width
        self.label_height = label_height

        # Additional space between nodes
        self.spacing = spacing

        # Default fill colors
        default_colors = {
            "oval": "lightblue",
            "rectangle": "lightgrey",
            "rectangle2": "lightbrown",
            "diamond": "lightgreen",
            "hexagon": "lightyellow",
            "terminal_start": "green",
            "terminal_end": "red"
        }
        self.colors = colors or default_colors

        # Default outline properties
        default_outlines = {
            "oval": {"color": "black", "thickness": 2},
            "rectangle": {"color": "black", "thickness": 2},
            "rectangle2": {"color": "black", "thickness": 2},
            "diamond": {"color": "black", "thickness": 2},
            "hexagon": {"color": "black", "thickness": 2},
            "terminal_start": {"color": "black", "thickness": 2},
            "terminal_end": {"color": "black", "thickness": 2}
        }
        self.outlines = outlines or default_outlines

        # Default font properties
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
        self.fonts = fonts or default_fonts
        

        # Default connector properties
        default_connectors = {
            "color": "black",
            "thickness": 2
        }
        self.connectors = connectors or default_connectors

        # Create a Canvas and Scrollbar
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars for the canvas
        self.scrollbar_y = Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.canvas.config(xscrollcommand=self.scrollbar_x.set)

        # Configure grid expansion
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        # Add export buttons
        self.export_buttons = tk.Frame(root)
        self.export_buttons.pack(fill=tk.X)

        # self.export_png_button = tk.Button(self.export_buttons, text="Export to PNG", command=self.export_to_png)
        # self.export_png_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.export_pdf_button = tk.Button(self.export_buttons, text="Export view to PDF", command=self.export_to_pdf)
        self.export_pdf_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.export_full_pdf_button = tk.Button(self.export_buttons, text="Export full to PDF", command=self.export_full_canvas_to_pdf)
        self.export_full_pdf_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # self.export_full_png_button = tk.Button(self.export_buttons, text="Export full to PNG", command=self.export_full_canvas_to_png)
        # self.export_full_png_button.pack(side=tk.LEFT, padx=5, pady=5)

    def grid_to_canvas(self, col, row):
        """Convert grid (col, row) to canvas (x, y) center coordinates with added spacing between nodes."""
        x = col * (self.grid_width + self.spacing) + self.grid_width / 2
        y = row * (self.grid_height + self.spacing) + self.grid_height / 2
        return x, y

    def node(self, col, row, text = " ", shape="point"):
        #Add a node to the canvas at the specified grid position.
        x, y = self.grid_to_canvas(col, row)
        
        tags = ("node", shape)  # Include the shape as a tag
        
        if shape == "point":
            # Create a tiny invisible circle or just a bounding box
            shape = "label"
            node = self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="", outline="", tags = tags)
        elif shape == "label":
            node = self.canvas.create_rectangle(x - self.label_width, y - self.label_height, x + self.label_width, y + self.label_height, fill="", outline="", tags = tags)
        elif shape == "title":
            node = self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="", outline="", tags = tags)
        else:
            node_factor = 2
            diamond_node_factor = 1.5

            fill_color = self.colors.get(shape, "white")  # Get the color for the shape or default to white
            outline_color = self.outlines[shape]["color"]  # Get the outline color for the shape
            outline_thickness = self.outlines[shape]["thickness"]  # Get the outline thickness

            if shape == "oval":
                node = self.canvas.create_oval(x - self.node_width / node_factor, y - self.node_height / node_factor, x + self.node_width / node_factor, y + self.node_height / node_factor, fill=fill_color, outline=outline_color, width=outline_thickness, tags = tags)
            elif shape == "terminal_start":
                node = self.canvas.create_oval(x - self.node_width / node_factor, y - self.node_height / node_factor, x + self.node_width / node_factor, y + self.node_height / node_factor, fill=fill_color, outline=outline_color, width=outline_thickness, tags = tags)
            elif shape == "terminal_end":
                node = self.canvas.create_oval(x - self.node_width / node_factor, y - self.node_height / node_factor, x + self.node_width / node_factor, y + self.node_height / node_factor, fill=fill_color, outline=outline_color, width=outline_thickness, tags = tags)
            elif shape == "diamond":
                node = self.canvas.create_polygon(x, y - self.node_height / diamond_node_factor, x + self.node_width / diamond_node_factor, y, x, y + self.node_height / diamond_node_factor, x - self.node_width / diamond_node_factor, y, fill=fill_color, outline=outline_color, width=outline_thickness, tags = tags)
            elif shape == "hexagon":
                size = self.node_width / node_factor
                points = self.hexagon_points(x, y, size)
                node = self.canvas.create_polygon(points, fill=fill_color, outline=outline_color, width=outline_thickness, tags = tags)
            else:  # Default rectangle
                node = self.canvas.create_rectangle(x - self.node_width / node_factor, y - self.node_height / node_factor, x + self.node_width / node_factor, y + self.node_height / node_factor, fill=fill_color, outline=outline_color, width=outline_thickness, tags = tags)

        # Add text with custom font properties and centered inside the node
        font = self.fonts[shape]["font"]
        font_size = self.fonts[shape]["size"]
        text_color = self.fonts[shape]["color"]
        text_weight = self.fonts[shape]["weight"]
        text_underline = self.fonts[shape]["underline"]

        # Create text with centered alignment
        font = Font(family=font, size=font_size, weight = text_weight, underline=text_underline)
        
        self.canvas.create_text(x, y, text=text, font=font, fill=text_color, anchor="center", tags="node", justify="center")

        # Update scroll region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
        # Update scroll region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        return node

    def hexagon_points(self, x, y, size):
        """Calculate the vertices of a hexagon centered at (x, y) with a given size."""
        points = []
        for i in range(6):
            angle = math.radians(60 * i)
            px = x + (size * 1) * math.cos(angle)
            py = y + (size/1.5) * math.sin(angle)
            points.extend((px, py))
        return points

    def connect(self, node1, direction1, node2, direction2, style="line"):
        """
        Connect two nodes with specified entry/exit directions.

        Args:
            node1: The starting node.
            direction1: The direction from which the connection leaves the starting node ("n", "s", "e", "w").
            node2: The ending node.
            direction2: The direction from which the connection enters the ending node ("n", "s", "e", "w").
            style: The style of the connection, either "line" or "arrow".
        """
        # Get bounding boxes of the nodes
        bbox1 = self.canvas.bbox(node1)
        bbox2 = self.canvas.bbox(node2)

        # Define direction offsets for each node
        offsets = {
            "n": lambda bbox: ((bbox[0] + bbox[2]) / 2, bbox[1]),  # Top center
            "s": lambda bbox: ((bbox[0] + bbox[2]) / 2, bbox[3]),  # Bottom center
            "e": lambda bbox: (bbox[2], (bbox[1] + bbox[3]) / 2),  # Right center
            "w": lambda bbox: (bbox[0], (bbox[1] + bbox[3]) / 2),  # Left center
            "c": lambda bbox: ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2),  # Center
        }

        # Calculate start and end points based on directions
        start = offsets[direction1](bbox1)
        end = offsets[direction2](bbox2)

        # Get the connector properties (color and thickness)
        connector_color = self.connectors["color"]
        connector_thickness = self.connectors["thickness"]

        # Arrow size based on line thickness (you can adjust this ratio)
        arrow_size = connector_thickness * 6  # Adjust multiplier for arrow size

        # Draw the connection
        if style == "arrow":
            self.canvas.create_line(
                *start, *end, 
                arrow=tk.LAST, 
                fill=connector_color, 
                width=connector_thickness,
                arrowshape=(arrow_size, arrow_size, arrow_size/4)  # Adjust arrow shape based on thickness
            )
        else:
            self.canvas.create_line(*start, *end, fill=connector_color, width=connector_thickness)


        # Update scroll region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def export_to_png(self, dpi=1080):
        """Export canvas to PNG with the specified DPI."""
        # Ask for a file to save the PNG
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if not file_path:
            return

        # Save the canvas to a PostScript file
        ps_file = file_path.replace(".png", ".ps")
        self.canvas.postscript(file=ps_file, colormode="color")

        # Open the PostScript file and convert it to PNG
        img = Image.open(ps_file)

        # Scale the image based on DPI
        width_in_pixels = int(img.width * dpi / 72)  # 72 DPI is default for postscript
        height_in_pixels = int(img.height * dpi / 72)
        img = img.resize((width_in_pixels, height_in_pixels), Image.LANCZOS)

        # Save the scaled image as PNG
        img.save(file_path, dpi=(dpi, dpi))
        print(f"Exported flowchart to PNG at {dpi} DPI: {file_path}")

    def export_to_pdf(self, dpi=1080):
        """Export canvas to PDF with the specified DPI."""
        # Ask for a file to save the PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        # Save the canvas to a PostScript file
        ps_file = file_path.replace(".pdf", ".ps")
        self.canvas.postscript(file=ps_file, colormode="color")

        # Open the PostScript file and scale it
        img = Image.open(ps_file)
        width_in_pixels = int(img.width * dpi / 72)  # 72 DPI is default for postscript
        height_in_pixels = int(img.height * dpi / 72)

        # Create a PDF with the scaled dimensions
        pdf = canvas.Canvas(file_path, pagesize=(width_in_pixels / dpi * 72, height_in_pixels / dpi * 72))
        pdf.drawImage(ps_file, 0, 0, width=width_in_pixels / dpi * 72, height=height_in_pixels / dpi * 72)
        pdf.save()
        print(f"Exported flowchart to PDF at {dpi} DPI: {file_path}")

    def export_full_canvas_to_png(self, dpi=300):
        #Export the full canvas (all nodes, even outside the visible area) to PNG.
        # Ask for a file to save the PNG
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if not file_path:
            return

        # Calculate the bounding box of all content on the canvas
        items = self.canvas.find_all()
        x_coords = [self.canvas.bbox(item)[0:3:2] for item in items]
        y_coords = [self.canvas.bbox(item)[1:4:2] for item in items]
        x_min, x_max = min(map(lambda x: x[0], x_coords)), max(map(lambda x: x[1], x_coords))
        y_min, y_max = min(map(lambda y: y[0], y_coords)), max(map(lambda y: y[1], y_coords))

        # Expand the canvas temporarily to fit all items
        width = x_max - x_min
        height = y_max - y_min
        self.canvas.config(width=width, height=height)
        self.canvas.update()

        # Save the canvas to PostScript
        ps_file = file_path.replace(".png", ".ps")
        self.canvas.postscript(file=ps_file, colormode="color", x=x_min, y=y_min, width=width, height=height)

        # Convert PostScript to PNG
        img = Image.open(ps_file)
        width_in_pixels = int(width * dpi / 72)  # Convert points to pixels
        height_in_pixels = int(height * dpi / 72)
        img = img.resize((width_in_pixels, height_in_pixels), Image.LANCZOS)
        img.save(file_path, dpi=(dpi, dpi))

        # Clean up
        print(f"Exported full canvas to PNG at {dpi} DPI: {file_path}")

        # Restore the canvas to its original size
        self.canvas.config(width=self.default_width, height=self.default_height)
        self.canvas.update()

    def export_full_canvas_to_pdf(self, dpi=300):
        # Export the full canvas (all nodes, even outside the visible area) to PDF.
        # Ask for a file to save the PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        # Calculate the bounding box of all content on the canvas
        items = self.canvas.find_all()
        x_coords = [self.canvas.bbox(item)[0:3:2] for item in items]
        y_coords = [self.canvas.bbox(item)[1:4:2] for item in items]
        x_min, x_max = min(map(lambda x: x[0], x_coords)), max(map(lambda x: x[1], x_coords))
        y_min, y_max = min(map(lambda y: y[0], y_coords)), max(map(lambda y: y[1], y_coords))

        # Expand the canvas temporarily to fit all items
        width = x_max - x_min
        height = y_max - y_min
        self.canvas.config(width=width, height=height)
        self.canvas.update()

        # Save the canvas to PostScript
        ps_file = file_path.replace(".pdf", ".ps")
        self.canvas.postscript(file=ps_file, colormode="color", x=x_min, y=y_min, width=width, height=height)

        # Convert PostScript to PDF
        img = Image.open(ps_file)
        width_in_pixels = int(width * dpi / 72)  # Convert points to pixels
        height_in_pixels = int(height * dpi / 72)

        pdf = canvas.Canvas(file_path, pagesize=(width_in_pixels / dpi * 72, height_in_pixels / dpi * 72))
        pdf.drawImage(ps_file, 0, 0, width=width_in_pixels / dpi * 72, height=height_in_pixels / dpi * 72)
        pdf.save()

        print(f"Exported full canvas to PDF at {dpi} DPI: {file_path}")

        # Restore the canvas to its original size
        self.canvas.config(width=self.default_width, height=self.default_height)
        self.canvas.update()


if __name__ == "__main__":
    root = tk.Tk()

    # Create flowchart with custom properties
    app = Flowchart(root, grid_width=1000, grid_height=1000, node_width=100, node_height=60, spacing=50)
    
    # Create nodes
    start = app.node(1, 1, "Start", "oval")
    decision = app.node(2, 2, "Decision", "diamond")
    end = app.node(4, 3, "End", "rectangle")

    # Connect nodes with specified entry/exit directions
    app.connect(start, "s", decision, "n", "arrow")  # From south of start to north of decision
    app.connect(decision, "e", end, "w", "line")    # From east of decision to west of end


    root.mainloop()
