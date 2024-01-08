import chess
import chess.svg
import chess.engine
import random
import math
from node import Node
from collections import deque

class MonteCarloTreeSearch:
    def __init__(self, root_node, c):
        self.root = root_node
        self.c = c
    
    def selection(self):
        max_ucb = float("-inf")
        max_children = []
        q = deque()
        q.append(self.root)
        while q:
            currentNode = q.popleft()
            if not currentNode.is_leaf():
                for child in currentNode.children:
                    q.append(child)
            else:
                print(currentNode)
                exploitation = currentNode.wins / currentNode.visits
                exploration = self.c * math.sqrt(math.log(currentNode.parent.visits) / currentNode.visits)
                print("Exploitation: " + str(exploitation) + ", Exploration: " + str(exploration) + ", UCB: " + str(exploitation + exploration))
                if exploration + exploitation > max_ucb:
                    max_ucb = exploration + exploitation
                    max_children = [currentNode]
                elif exploration + exploitation == max_ucb:
                    max_children.append(currentNode)
        choice = random.choice(max_children)
        print("Node: " + str(choice) + ", UCB: " + str(max_ucb))
        return choice
    
    def expansion(self, current_node):
        current_board = current_node.board
        for legal_move in list(current_node.board.legal_moves):
            child_board = chess.Board(current_board.fen())
            child_board.push(legal_move)
            child_node = Node(child_board, current_node, chess.BLACK if current_node.player else chess.WHITE, 0, 10)
            current_node.add_child(child_node)
            # simulate 10 times (so that visits will not be 0)
