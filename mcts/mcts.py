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
            # print("Node: " + str(choice) + ", UCB: no visits")
            return choice
        else:
            choice = random.choice(max_children)
            # print("Node: " + str(choice) + ", UCB: " + str(max_ucb))
            return choice
    
    def expansion(self, current_node):
        current_board = current_node.board
        for legal_move in list(current_node.board.legal_moves):
            child_board = chess.Board(current_board.fen())
            child_board.push(legal_move)
            child_node = Node(child_board, current_node, chess.BLACK if current_node.player else chess.WHITE, 0, 0, legal_move)
            current_node.add_child(child_node)
            # print(child_node)
        if current_node.children: # how to deal with
            return random.choice(current_node.children) # just simulate one time
    
    def simulation(self, current_node):
        current_board = chess.Board(current_node.board.fen())
        while not current_board.is_game_over():
            move = random.choice(list(current_board.legal_moves))
            current_board.push(move)
        # print(current_board.result())
        # print(current_node)
        return current_board.result()

    def backpropagation(self, current_node, outcome):
        while current_node:
            if (current_node.player and outcome == "1-0") or (not current_node.player and outcome == "0-1"):
                current_node.update_wins(1)
            elif outcome == "1/2-1/2":
                current_node.update_wins(0.5)
            current_node.update_visits()
            # print("- " + str(current_node))
            current_node = current_node.parent

    def printTree(self):
        print("Tree: ")
        return self.printTreeHelper(self.root, 0)
    
    def printTreeHelper(self, node, level):
        str = ""
        for i in range(level):
            str += "|   "
        str += "|-- " + node.nodeRepresentation()
        print(str)
        for child in node.children:
            self.printTreeHelper(child, level + 1)
    
    def mostPromisingMoves(self):
        current_node = self.root
        # print("Step 1: " + str(current_node))
        i = 1
        while not current_node.is_leaf():
            max_children = []
            max_ucb = float("-inf")
            for child in current_node.children:
                if child.visits != 0:
                    exploitation = child.wins / child.visits
                    # print("exploitation: " + str(exploitation))
                    exploration = self.c * math.sqrt(math.log(current_node.visits) / child.visits)
                    # print("exploration: " + str(exploration))
                    # print("Exploitation: " + str(exploitation) + ", Exploration: " + str(exploration) + ", UCB: " + str(exploitation + exploration))
                    if exploration + exploitation > max_ucb:
                        max_ucb = exploration + exploitation
                        max_children = [child]
                    elif exploration + exploitation == max_ucb:
                        max_children.append(child)
            choice = random.choice(max_children)
            print("Step " + str(i) + ": " + str(choice.move))
            i += 1
            current_node = choice
        