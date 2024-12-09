import tkinter as tk
from tkinter import filedialog
import math

class LineClippingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Line Clipping Algorithms")

        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.segments = []
        self.window = (0, 0, 0, 0)
        self.zoom_scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<B1-Motion>", self.pan)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label="Load File", command=self.load_file)

        self.start_x = 0
        self.start_y = 0

    def cohen_sutherland_clip(self, x1, y1, x2, y2, xmin, ymin, xmax, ymax):
        INSIDE = 0  # 0000
        LEFT = 1    # 0001
        RIGHT = 2   # 0010
        BOTTOM = 4  # 0100
        TOP = 8     # 1000

        def compute_out_code(x, y):
            code = INSIDE
            if x < xmin:
                code |= LEFT
            elif x > xmax:
                code |= RIGHT
            if y < ymin:
                code |= BOTTOM
            elif y > ymax:
                code |= TOP
            return code

        outcode1 = compute_out_code(x1, y1)
        outcode2 = compute_out_code(x2, y2)
        accept = False

        while True:
            if not (outcode1 | outcode2):
                accept = True
                break
            elif outcode1 & outcode2:
                break
            else:
                x, y = 0, 0
                outcode_out = outcode1 if outcode1 else outcode2

                if outcode_out & TOP:
                    x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                    y = ymax
                elif outcode_out & BOTTOM:
                    x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                    y = ymin
                elif outcode_out & RIGHT:
                    y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                    x = xmax
                elif outcode_out & LEFT:
                    y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                    x = xmin

                if outcode_out == outcode1:
                    x1, y1 = x, y
                    outcode1 = compute_out_code(x1, y1)
                else:
                    x2, y2 = x, y
                    outcode2 = compute_out_code(x2, y2)

        if accept:
            return (x1, y1, x2, y2)
        else:
            return None

    def liang_barsky_clip(self, x1, y1, x2, y2, polygon):
        dx = x2 - x1
        dy = y2 - y1
        t0, t1 = 0.0, 1.0

        for i in range(len(polygon)):
            x3, y3 = polygon[i]
            x4, y4 = polygon[(i + 1) % len(polygon)]

            edge_dx = x4 - x3
            edge_dy = y4 - y3

            normal_x = -edge_dy
            normal_y = edge_dx

            numerator = normal_x * (x1 - x3) + normal_y * (y1 - y3)
            denominator = normal_x * dx + normal_y * dy

            if denominator == 0:
                if numerator < 0:
                    return None
            else:
                t = -numerator / denominator
                if denominator < 0:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)

        if t0 > t1:
            return None

        x1_clipped = x1 + t0 * dx
        y1_clipped = y1 + t0 * dy
        x2_clipped = x1 + t1 * dx
        y2_clipped = y1 + t1 * dy

        return (x1_clipped, y1_clipped, x2_clipped, y2_clipped)

    def draw_scene(self, clipped_segments, algorithm):
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        xmin, ymin, xmax, ymax = self.window

        scale_x = self.zoom_scale * width / (xmax - xmin)
        scale_y = self.zoom_scale * height / (ymax - ymin)

        def transform(x, y):
            return (scale_x * (x - xmin) + self.offset_x, height - scale_y * (y - ymin) + self.offset_y)

        self.canvas.create_rectangle(*transform(xmin, ymin), *transform(xmax, ymax), outline="blue", width=2)

        for (x1, y1, x2, y2) in self.segments:
            self.canvas.create_line(*transform(x1, y1), *transform(x2, y2), fill="red", width=2)

        for (x1, y1, x2, y2) in clipped_segments:
            if algorithm == "Sutherland-Cohen":
                color = "green"
            else:
                color = "purple"
            self.canvas.create_line(*transform(x1, y1), *transform(x2, y2), fill=color, width=2)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return

        with open(file_path, "r") as file:
            lines = file.readlines()

        n = int(lines[0].strip())
        self.segments = [tuple(map(int, lines[i + 1].split())) for i in range(n)]
        self.window = tuple(map(int, lines[n + 1].split()))

        clipped_sutherland = []
        for x1, y1, x2, y2 in self.segments:
            clipped = self.cohen_sutherland_clip(x1, y1, x2, y2, *self.window)
            if clipped:
                clipped_sutherland.append(clipped)

        clipped_liang = []
        convex_polygon = [(self.window[0], self.window[1]), (self.window[2], self.window[1]), (self.window[2], self.window[3]), (self.window[0], self.window[3])]
        for x1, y1, x2, y2 in self.segments:
            clipped = self.liang_barsky_clip(x1, y1, x2, y2, convex_polygon)
            if clipped:
                clipped_liang.append(clipped)

        self.draw_scene(clipped_sutherland, "Sutherland-Cohen")
        self.draw_scene(clipped_liang, "Liang-Barsky")

    def zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.zoom_scale *= factor
        self.draw_scene([], "Sutherland-Cohen")

    def start_pan(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def pan(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.offset_x += dx
        self.offset_y += dy
        self.start_x = event.x
        self.start_y = event.y
        self.draw_scene([], "Sutherland-Cohen")

if __name__ == "__main__":
    root = tk.Tk()
    app = LineClippingApp(root)
    root.mainloop()
