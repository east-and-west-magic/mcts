import chess
import chess.svg
import chess.engine
import random
import math
from node import Node
from queue import PriorityQueue, Queue

class MonteCarloTreeSearch:
    def __init__(self, root_node, c):
        self.root = root_node
        self.c = c
    
    def selection(self):
        queue = Queue()
        pq = PriorityQueue()
        queue.put(self.root)
        while not queue.empty():
            currentNode = queue.get()
            if not currentNode.is_leaf():
                for child in currentNode.children:
                    queue.put(child)
            else:
                print(currentNode)
                exploitation = currentNode.wins
                exploration = self.c * math.sqrt(math.log(currentNode.parent.visits) / currentNode.visits)
                print("Exploitation: " + str(exploitation) + ", Exploration: " + str(exploration) + ", UCB: " + str(exploitation + exploration))
                pq.put((-(exploitation + exploration), currentNode))

        (priority, data) = pq.get()
        print()
        print("Node: " + str(data) + ", Priority: " + str(-priority))
        return data
    
    def expansion(self, current_node):
        current_board = current_node.board
        for legal_move in list(current_node.board.legal_moves):
            child_board = chess.Board(current_board.fen())
            child_board.push(legal_move)
            child_node = Node(child_board, current_node, chess.BLACK if current_node.player else chess.WHITE, 0, 10)
            current_node.add_child(child_node)
            # simulate 10 times (so that visits will not be 0)
