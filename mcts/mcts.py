import chess
import chess.svg
import chess.engine
import random
import math
from node import Node
from collections import deque
from operator import itemgetter

class MonteCarloTreeSearch:
    def __init__(self, root_node, c):
        self.root = root_node
        self.c = c
    

    def selection(self):
        current = self.root
        root_to_move = False
        while not current.is_leaf():
            max_ucb = float("-inf")
            selected_child = None
            max_children = []
            unvisited_children = []

            # alternate
            root_to_move = not root_to_move

            for child in current.children:
                # if str(child.move) not in ['f5f7', 'g7g8', 'f7f5', 'g8g7']:
                if str(child.move) not in ['g4h5', 'e4f5']:
                    pass
                if child.visits == 0:
                    unvisited_children.append(child)
                else:
                    a = child.wins/child.visits 
                    a = 1 - a

                    # alternate
                    if not root_to_move:
                        # a = 1 - a
                        pass

                    assert root_to_move == (not child.player)

                    if child.player:
                        # a = 1 - a
                        pass

                    b = self.c * math.sqrt(2*math.log(current.visits) / child.visits)
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

        # look ahead one step
        for legal_move in list(current_node.board.legal_moves):
            current_board.push(legal_move)
            is_checkmate = current_board.is_checkmate()
            current_board.pop()
            if is_checkmate:
                # skip expand
                child_board = chess.Board(current_board.fen())
                child_node = Node(child_board, current_node, chess.BLACK if current_node.player else chess.WHITE, 0, 0, child_board.san(legal_move))
                child_board.push(legal_move)
                current_node.add_child(child_node)
                # just return the child_node leads to checkmate
                return child_node

        for legal_move in list(current_node.board.legal_moves):
            # if str(legal_move) not in ['f5f7', 'g7g8', 'f7f5', 'g8g7']:
            if str(legal_move) not in ['g4h5', 'e4f5']:                
                pass
            child_board = chess.Board(current_board.fen())
            child_node = Node(child_board, current_node, chess.BLACK if current_node.player else chess.WHITE, 0, 0, child_board.san(legal_move))
            child_board.push(legal_move)
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

    def printTree(self, limit):
        print("Tree: ")
        self.pindex_ucb = []
        return self.printTreeHelper(self.root, 0, 0, 0, limit)
    
    def sort_children_by(self, node, ucb=True):
        """ 
        given a node, sort its children by ucb or win_rate
        return a sorted list of form (index, child) if not ucb
        else return a dict of form {move: index}
        """
        res = []
        for child in node.children:
            if child.visits > 0:
                a = child.wins/child.visits
                b = self.c * math.sqrt(2*math.log(node.visits)/child.visits)
                if ucb:
                    # sort by ucb
                    res.append((1 - a + b, child))
                else:
                    # sort by win_rate
                    res.append((1 - a, child))
            else:
                # inf
                res.append((-1, child))

        first_item = itemgetter(0)
        res2 = sorted(res, key = first_item, reverse=True)                

        if not ucb:
            res3 = []
            for index, (_, child) in enumerate(res2):
                res3.append([index, child])
        else:
            res3 = {}
            for index, (_, child) in enumerate(res2):
                res3[child.move] = index

        return res3


    def printTreeHelper(self, node, level, index_win_rate, index_ucb, limit):
        # global pindex_ucb

        if level >= limit:
            return
        if node.visits == 0:
            pass

        str = ""
        for i in range(level):
            str += "|   "
        win_rate = 0
        if node.visits:
            win_rate = 1-node.wins/node.visits
        str += "|-- " + f"{win_rate:.4f} [[{index_win_rate}:{index_ucb}] [{len(self.pindex_ucb)} {'/'.join(self.pindex_ucb)}]] " + node.nodeRepresentation(self.c)
        print(str)

        children_ucb = self.sort_children_by(node, True)
        children_win_rate = self.sort_children_by(node, False)

        # for (index1, child_tmp) in reversed(children_win_rate):
        for (index1, child_tmp) in reversed(children_win_rate[:3]):
            index2 = children_ucb[child_tmp.move]
            self.pindex_ucb.append(f"{index2}")
            self.printTreeHelper(child_tmp, level + 1, index1, index2, limit)
            self.pindex_ucb.pop()

    def mostPromisingMoves(self):
        current_node = self.root
        i = 1
        while not current_node.is_leaf():
            max_children = []
            max_ucb = float("-inf")
            for child in current_node.children:
                if child.visits != 0:
                    exploitation = child.wins / child.visits
                    exploration = self.c * math.sqrt(2*math.log(current_node.visits) / child.visits)
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
        