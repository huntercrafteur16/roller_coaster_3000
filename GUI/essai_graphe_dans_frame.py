import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
 
app = tk.Tk()
app.wm_title("Frame Matplotlib")
 
fig = Figure(figsize=(6, 4), dpi=96)
ax = fig.add_subplot(111)
ax.plot(range(3), [5, 6, 2])
 
graph = FigureCanvasTkAgg(fig, master=app)
canvas = graph.get_tk_widget()
canvas.grid(row=0, column=0)
 
app.mainloop()