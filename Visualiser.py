import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import random
import math
from Board_Algos import DFSNQueens, HillClimbingNQueens, GeneticNQueens, SimulatedAnnealingNQueens

def visualize_random_board(n):  # Only for visualizing the board,
    # Generate a random board: one queen per row, random column
    board = [random.randint(0, n - 1) for _ in range(n)]

    fig, ax = plt.subplots()
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_aspect('equal')
    ax.set_title(f'{n}-Queens Random Placement')

    # Draw the chessboard
    for row in range(n):
        for col in range(n):
            color = 'white' if (row + col) % 2 == 0 else 'gray'
            rect = plt.Rectangle((col, n - row - 1), 1, 1, facecolor=color)
            ax.add_patch(rect)

    # Draw the queens
    for row, col in enumerate(board):
        ax.text(col + 0.5, n - row - 0.5, '♛', fontsize=20, ha='center', va='center', color='red')

    plt.grid(True)
    plt.show()
    
visualize_random_board(15) #preferably dont exceed 15, as the queen representation becomes junky.

