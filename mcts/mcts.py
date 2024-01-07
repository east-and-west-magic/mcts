import chess
import chess.svg
import chess.engine
import random
import math
from node import Node
from queue import PriorityQueue

class MonteCarloTreeSearch:
    def __init__(self, root_node, c):
        self.root = root_node
        self.c = c
    
    def selection(self):
        queue = []
        pq = PriorityQueue()
        queue.append(self.root)
        while queue:
            currentNode = queue.pop(0)
            if not currentNode.is_leaf():
                for child in currentNode.children:
                    queue.append(child)
            else:
                print(currentNode)
                exploitation = currentNode.wins
                exploration = self.c * math.sqrt(math.log(currentNode.parent.visits) / currentNode.visits)
                print("Exploitation: " + str(exploitation) + ", Exploration: " + str(exploration) + ", UCB: " + str(exploitation + exploration))
                pq.put((-(exploitation + exploration), currentNode))

        (priority, data) = pq.get()
        print(data)
        print(-priority)
        return data
        # current = self.root
        # while not current.is_leaf():
        #     max_ucb = float("-inf")
        #     selected_child = None
        #     max_children = []
        #     unvisited_children = []
        #     for child in current.children:
        #         if child.visits == 0:
        #             unvisited_children.append(child)
        #         else:
        #             child_ucb = child.wins + self.c * math.sqrt(math.log(current.visits) / child.visits)
        #             if child_ucb > max_ucb:
        #                 max_children = []
        #                 max_children.append(child)
        #                 max_ucb = child_ucb
        #             elif child_ucb == max_ucb:
        #                 max_children.append(child)
        #         if unvisited_children:
        #             selected_child = random.choice(unvisited_children)
        #         else:
        #             selected_child = random.choice(max_children)
        #     current = selected_child
        #     print(current)
        # return current
    
    def expansion(self, current_node):
        current_board = current_node.board
        for legal_move in list(current_node.board.legal_moves):
            child_board = chess.Board(current_board.fen())
            child_board.push(legal_move)
            child_node = Node(child_board, current_node, chess.BLACK if current_node.player else chess.WHITE, 0, 10)
            current_node.add_child(child_node)
            # simulate 10 times (so that visits will not be 0)
