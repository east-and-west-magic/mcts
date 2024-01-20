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
        current = self.root
        while not current.is_leaf():
            max_ucb = float("-inf")
            selected_child = None
            max_children = []
            unvisited_children = []
            for child in current.children:
                # if str(child.move) not in ['f5f7', 'g7g8', 'f7f5', 'g8g7']:
                if str(child.move) not in ['g4h5', 'e4f5']:
                    pass
                if child.visits == 0:
                    unvisited_children.append(child)
                else:
                    a = child.wins/child.visits 
                    if not child.player:
                        a = 1 - a
                    b = self.c * math.sqrt(math.log(current.visits) / child.visits)
                    child_ucb = a + b 
                    if child_ucb > max_ucb:
                        max_children = []
                        max_children.append(child)
                        max_ucb = child_ucb
                    elif child_ucb == max_ucb:
                        max_children.append(child)
                if unvisited_children:
                    selected_child = random.choice(unvisited_children)
                else:
                    selected_child = random.choice(max_children)
            current = selected_child
            # print(current)
        return current
        

    def selection2(self):
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
                unvisited_children.append(currentNode)
            else:
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
            assert False
            # print("Node: " + str(choice) + ", UCB: no visits")
            return choice
        else:
            choice = random.choice(max_children)
            # print("Node: " + str(choice) + ", UCB: " + str(max_ucb))
            return choice
    
    def expansion(self, current_node):
        current_board = current_node.board
        for legal_move in list(current_node.board.legal_moves):
            # if str(legal_move) not in ['f5f7', 'g7g8', 'f7f5', 'g8g7']:
            if str(legal_move) not in ['g4h5', 'e4f5']:                
                pass
            child_board = chess.Board(current_board.fen())
            child_board.push(legal_move)
            child_node = Node(child_board, current_node, chess.BLACK if current_node.player else chess.WHITE, 0, 0, legal_move)
            current_node.add_child(child_node)
        if current_node.children: # how to deal with
            return random.choice(current_node.children) # just simulate one time
        else:
            return None
    
    def simulation(self, current_node):
        current_board = chess.Board(current_node.board.fen())
        while not current_board.is_game_over():
            move = random.choice(list(current_board.legal_moves))
            current_board.push(move)
        return current_board.result()

    def backpropagation(self, current_node, outcome):
        while current_node:
            if (current_node.player and outcome == "1-0") or (not current_node.player and outcome == "0-1"):
                current_node.update_wins(1)
            elif outcome == "1/2-1/2":
                current_node.update_wins(0.5)
            current_node.update_visits()
            current_node = current_node.parent

    def printTree(self):
        print("Tree: ")
        return self.printTreeHelper(self.root, 0)
    
    def printTreeHelper(self, node, level):
        if level >= 2:
            return
        if node.visits == 0:
            pass

        str = ""
        for i in range(level):
            str += "|   "
        str += "|-- " + node.nodeRepresentation()
        print(str)
        for child in node.children:
            self.printTreeHelper(child, level + 1)        

    def mostPromisingMoves(self):
        current_node = self.root
        i = 1
        while not current_node.is_leaf():
            max_children = []
            max_ucb = float("-inf")
            for child in current_node.children:
                if child.visits != 0:
                    exploitation = child.wins / child.visits
                    exploration = self.c * math.sqrt(math.log(current_node.visits) / child.visits)
                    # print("Exploitation: " + str(exploitation) + ", Exploration: " + str(exploration) + ", UCB: " + str(exploitation + exploration))
                    info = (
                        exploitation, 
                        (child.wins, child.visits), 
                        exploration,
                        (current_node.visits, child.visits)
                    )
                    if exploration + exploitation > max_ucb:
                        max_ucb = exploration + exploitation
                        max_children = [(child, info)]
                    elif exploration + exploitation == max_ucb:
                        max_children.append((child, info))
            choice, info = random.choice(max_children)
            print("Step " + str(i) + ": " + str(choice.move) + ", UCB: " + str(max_ucb), info)
            i += 1
            current_node = choice
        