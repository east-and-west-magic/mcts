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
        unvisited_children = []
        q = deque()
        q.append(self.root)
        while q:
            currentNode = q.popleft()
            if not currentNode.is_leaf():
                for child in currentNode.children:
                    q.append(child)
            elif currentNode.visits == 0:
                # print(currentNode)
                unvisited_children.append(currentNode)
            else:
                # print(currentNode)
                exploitation = currentNode.wins / currentNode.visits
                exploration = self.c * math.sqrt(math.log(currentNode.parent.visits) / currentNode.visits)
                # print("Exploitation: " + str(exploitation) + ", Exploration: " + str(exploration) + ", UCB: " + str(exploitation + exploration))
                if exploration + exploitation > max_ucb:
                    max_ucb = exploration + exploitation
                    max_children = [currentNode]
                elif exploration + exploitation == max_ucb:
                    max_children.append(currentNode)
        if unvisited_children:
            choice = random.choice(unvisited_children)
            print("Node: " + str(choice) + ", no visits")
            return choice
        else:
            choice = random.choice(max_children)
            print("Node: " + str(choice) + ", UCB: " + str(max_ucb))
            return choice
    
    def expansion(self, current_node):
        current_board = current_node.board
        for legal_move in list(current_node.board.legal_moves):
            child_board = chess.Board(current_board.fen())
            child_board.push(legal_move)
            child_node = Node(child_board, current_node, chess.BLACK if current_node.player else chess.WHITE, 0, 0)
            current_node.add_child(child_node)
            # print(child_node)
        if current_node.children: # how to deal with
            return random.choice(current_node.children) # just simulate one time
    
    def simulation(self, current_node):
        current_board = current_node.board
        while not current_board.is_game_over():
            move = random.choice(list(current_board.legal_moves))
            current_board.push(move)
        # print(current_board.result())
        return current_board.result()

    def backpropagation(self, current_node, outcome):
        while current_node:
            if (current_node.player and outcome == "1-0") or (not current_node.player and outcome == "0-1"):
                current_node.update_wins(1)
            elif outcome == "1/2-1/2":
                current_node.update_wins(0.5)
            current_node.update_visits()
            print(current_node)
            current_node = current_node.parent