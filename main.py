from HillClimbingNQueens import HillClimbingNQueens
from SimulatedAnnealingNQueens import SimulatedAnnealingNQueens
from DFSNQueens import DFSNQueens
from GeneticNQueens import GeneticNQueens
from Com_Funcs import test_algorithm, visualize_board
import csv

def Averages(csv_file,start_row,end_row):
            with open(csv_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                

visualize_board(10)
test_algorithm(GeneticNQueens, 10, 10)

