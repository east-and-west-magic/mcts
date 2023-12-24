import chess
import chess.svg
import chess.engine
import random
import math
from node import Node

class MonteCarloTreeSearch:
    def __init__(self, root_node, c):
        self.root = root_node
        self.c = c
    
    def selection(self):
        current = self.root
        while not current.is_leaf():
            max_ucb = float("-inf")
            selected_child = None
            unvisited_children = []
            for child in current.children:
                if child.visits == 0:
                    unvisited_children.append(child)
                else:
                    child_ucb = child.wins + self.c * math.sqrt(math.log(current.visits) / child.visits)
                    if child_ucb > max_ucb:
                        selected_child = child
                        max_ucb = child_ucb
                if unvisited_children:
                    selected_child = random.choice(unvisited_children)
            current = selected_child
        return current
    
    def expansion(self, current_node):
        current_board = current_node.board
        for legal_move in list(current_node.board.legal_moves):
            child_board = chess.Board(current_board.fen())
            child_board.push(legal_move)
            child_node = Node(child_board, current_node, chess.BLACK if current_node.player else chess.WHITE)
            current_node.add_child(child_node)