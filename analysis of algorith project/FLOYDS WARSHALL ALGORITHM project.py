import random
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for better compatibility
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

MIN_DIM = 5
MAX_DIM = 15
DEFAULT_DIM = 8

# --- Maze Generation ---
def generate_maze(size=8, wall_probability=0.15):
    grid = np.zeros((size, size), dtype=int)  # Create a grid with all paths (0)
    for i in range(size):
        for j in range(size):
            # Ensure start and end are always open (0)
            if (i == 0 and j == 0) or (i == size - 1 and j == size - 1):
                grid[i][j] = 0
            elif random.random() < wall_probability:
                grid[i][j] = 1  # Place wall (1)
            else:
                grid[i][j] = 0  # Path (0)
    return grid

# --- Floyd-Warshall Algorithm ---
def floyd_warshall(grid, start, end):
    size = len(grid)
    dist = np.full((size, size), np.inf)  # Distance matrix initialized to infinity
    dist[start] = 0  # Distance from start to itself is 0
    prev = np.full((size, size, 2), -1, dtype=int)  # Initialize prev as a numpy array of tuples
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for _ in range(size * size):
        updated = False
        for i in range(size):
            for j in range(size):
                if grid[i][j] == 0:
                    for di, dj in moves:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < size and 0 <= nj < size and grid[ni][nj] == 0:
                            if dist[ni][nj] > dist[i][j] + 1:
                                dist[ni][nj] = dist[i][j] + 1
                                prev[ni][nj] = [i, j]
                                updated = True
        if not updated:
            break
    path = []
    current = end
    while tuple(current) != (-1, -1) and tuple(current) != start:
        path.append(tuple(current))
        current = tuple(prev[tuple(current)])
    if tuple(current) == start:
        path.append(start)
        path.reverse()
        return path
    return []

# --- Visualization ---
def visualize_maze(grid, shortest_path=None):
    size = len(grid)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xticks(np.arange(0, size, 1))
    ax.set_yticks(np.arange(0, size, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Plot the grid (maze)
    for i in range(size):
        for j in range(size):
            color = 'white' if grid[i][j] == 0 else 'black'
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color))

    # If there is a shortest path, highlight it first
    if shortest_path:
        for point in shortest_path:
            ax.add_patch(plt.Rectangle((point[1], point[0]), 1, 1, color='red', alpha=0.5))

    # Mark start and end points as filled circles and label them
    start = (0, 0)
    end = (size - 1, size - 1)
    ax.add_patch(plt.Circle((start[1] + 0.5, start[0] + 0.5), 0.3, color='green', zorder=10))  # Start as green circle
    ax.add_patch(plt.Circle((end[1] + 0.5, end[0] + 0.5), 0.3, color='blue', zorder=10))      # End as blue circle
    ax.text(start[1] + 0.5, start[0] + 0.5, 'S', color='white', fontsize=16, ha='center', va='center', zorder=11, fontweight='bold')
    ax.text(end[1] + 0.5, end[0] + 0.5, 'E', color='white', fontsize=16, ha='center', va='center', zorder=11, fontweight='bold')

    plt.draw()
    plt.pause(0.01)  # Non-blocking visualization

class MazeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Runner AI")
        self.configure(bg="#f7f7f7")
        self.geometry("700x500")
        self.resizable(False, False)
        self.size = tk.IntVar(value=DEFAULT_DIM)
        self.status = tk.StringVar(value="Adjust settings and generate a maze.")
        self.is_generating = False
        self._build_ui()

    def _build_ui(self):
        # Control panel
        panel = tk.Frame(self, bg="#fff", bd=1, relief="solid")
        panel.place(x=20, y=20, width=220, height=460)

        tk.Label(panel, text="Maze Runner AI", font=("Arial", 16, "bold"), bg="#fff", fg="#2d6a4f").pack(pady=(20, 5))
        tk.Label(panel, text="Generate square maze images using AI.\nAdjust the grid size and click generate.", font=("Arial", 9), bg="#fff", fg="#555").pack(pady=(0, 15))

        tk.Label(panel, text="Grid Size:", font=("Arial", 10, "bold"), bg="#fff").pack()
        size_slider = ttk.Scale(panel, from_=MIN_DIM, to=MAX_DIM, orient="horizontal", variable=self.size, command=lambda e: self._update_size_label())
        size_slider.pack(fill="x", padx=20)
        self.size_label = tk.Label(panel, text=f"{DEFAULT_DIM}x{DEFAULT_DIM}", font=("Arial", 10, "bold"), bg="#fff", fg="#2d6a4f")
        self.size_label.pack(pady=(0, 10))

        self.generate_btn = tk.Button(panel, text="Generate New Maze", font=("Arial", 11, "bold"), bg="#2d6a4f", fg="#fff", relief="flat", command=self.generate_maze_action)
        self.generate_btn.pack(pady=10, fill="x", padx=20)

        self.status_label = tk.Label(panel, textvariable=self.status, font=("Arial", 9), bg="#fff", fg="#888", wraplength=180, justify="left")
        self.status_label.pack(pady=(20, 0), padx=10, anchor="w")

        # Maze display area
        self.display_frame = tk.Frame(self, bg="#f7f7f7", bd=0)
        self.display_frame.place(x=260, y=20, width=420, height=460)
        self.canvas = None

    def _update_size_label(self):
        val = int(self.size.get())
        self.size_label.config(text=f"{val}x{val}")

    def generate_maze_action(self):
        if self.is_generating:
            return
        self.is_generating = True
        self.status.set("Generating maze...")
        self.update_idletasks()
        self.display_maze(None, None)
        self.after(100, self._generate_maze)

    def _generate_maze(self):
        size = int(self.size.get())
        maze = generate_maze(size)
        start = (0, 0)
        end = (size - 1, size - 1)
        path = floyd_warshall(maze, start, end)
        if path:
            self.status.set(f"Successfully generated {size}x{size} maze.")
            self.display_maze(maze, path)
        else:
            self.status.set("No solution found. Try again or reduce wall probability.")
            self.display_maze(maze, None)
        self.is_generating = False

    def display_maze(self, maze, path):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        if maze is not None:
            size = maze.shape[0]
            for i in range(size):
                for j in range(size):
                    color = 'white' if maze[i, j] == 0 else 'black'
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color))
            if path:
                for point in path:
                    ax.add_patch(plt.Rectangle((point[1], point[0]), 1, 1, color='red', alpha=0.5))
            # Draw start and end as circles with labels
            ax.add_patch(plt.Circle((0.5, 0.5), 0.3, color='green', zorder=10))
            ax.text(0.5, 0.5, 'S', color='white', fontsize=16, ha='center', va='center', zorder=11, fontweight='bold')
            ax.add_patch(plt.Circle((size - 0.5, size - 0.5), 0.3, color='blue', zorder=10))
            ax.text(size - 0.5, size - 0.5, 'E', color='white', fontsize=16, ha='center', va='center', zorder=11, fontweight='bold')
            ax.set_xlim(0, size)
            ax.set_ylim(0, size)
        else:
            ax.text(0.5, 0.5, "Maze will appear here", fontsize=14, color="#aaa", ha="center", va="center")
        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(fig, master=self.display_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

if __name__ == "__main__":
    app = MazeApp()
    app.mainloop()
