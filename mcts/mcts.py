import chess
import random
import math
from node import Node
from operator import itemgetter


class MonteCarloTreeSearch:
    def __init__(self, root_node, c):
        self.root = root_node
        self.c = c
        self.mate_in_1 = {}
        self.be_mated_in_1 = {}
        self.mate_in_2 = {}
    

    def selection(self):
        current = self.root
        while not current.is_leaf():
            max_ucb = float("-inf")
            selected_child = None
            max_children = []
            unvisited_children = []

            for child in current.children:
                if child.visits == 0:
                    unvisited_children.append(child)
                else:
                    # Use lose rate. Is this a bug? BUG
                    child_ucb = child.get_ucb2(self.c)
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
         
    
    def one_step_lookahead(self, current_node: Node, cache: bool) -> Node:
        """
        lookahead one step and check if there is a checkmate/win.
        If true, retun the node representing the move that checmates.
        if not, return None
        """

        if cache:
            res = self.mate_in_1.get(current_node.get_moves(), None)
            if res:
                return res

        current_board = current_node.board
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
                # cache
                if cache:
                    self.mate_in_1[current_node.get_moves()] = child_node
                # return the child_node leads to checkmate, eliminates wasted expansion
                return child_node
        return None


    # def three_step_lookahead(self, current_node: Node):
    #     """
    #     lookahead 3 steps.
    #     If there is a next step move, no matther what the opponent will do, 
    #     there is a checkmate move, then return that next step move.
    #     if no, return None
    #     """
    #     assert self.mate_in_1[current_node.get_moves] is None

    #     moves = current_node.get_moves()
    #     current_board = current_node.board
    #     for legal_move in list(current_node.board.legal_moves):
    #         moves = moves + (current_board.san(legal_move),)
    #         current_board.push(legal_move)
    #         checkmate_for_every_move = True
    #         for opponent_legal_move in list(current_board.legal_moves):
    #             moves = moves + (current_board.san(opponent_legal_move),)
    #             current_board.push(opponent_legal_move)
    #             if moves not in self.mate_in_1:
    #                 checkmate_for_every_move = False
    #                 # return None # no need to pop, I guess, so directly return
    #                 break
    #         current_board.pop()
    #         if checkmate_for_every_move:
    #             # skip expand
    #             child_board = chess.Board(current_board.fen())
    #             child_node = Node(child_board, current_node, chess.BLACK if current_node.player else chess.WHITE, 0, 0, child_board.san(legal_move))
    #             child_board.push(legal_move)
    #             current_node.add_child(child_node)
    #             # just return the child_node leads to checkmate
    #             return child_node
    #         else:
    #             break

    #     return None


    def expansion(self, current_node):
        
        # 1-step lookahead
        node = self.one_step_lookahead(current_node, True)
        if node:
            return node
        
        # # 3-step lookahead
        # node = self.three_step_lookahead(current_node)
        # if node:
        #     return node

        current_board = current_node.board
        for legal_move in list(current_node.board.legal_moves):
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


    def printTree(self, limit, topk):
        print("Tree: ")
        self.pindex_ucb = []
        return self.printTreeHelper(self.root, 0, 0, 0, limit, topk)


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


    def printTreeHelper(self, node, level, index_win_rate, index_ucb, limit, topk):
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
        # "\033[31mHello\033[0m"
        if level % 2 == 0:
            color_code = 31
        else:
            color_code = 32
        color = f"\033[{color_code}m{win_rate:.4f}\033[0m"
        str += f"|-- " + f"{color} [[{index_win_rate}:{index_ucb}] [{len(self.pindex_ucb)} {'/'.join(self.pindex_ucb)}]] " + node.node_repr(self.c)
        print(str)

        children_ucb = self.sort_children_by(node, True) # get a list
        children_win_rate = self.sort_children_by(node, False) # get a dict

        if level > 0 and topk > 0:
            children_win_rate = children_win_rate[:topk]
        for (index1, child_tmp) in reversed(children_win_rate):
            index2 = children_ucb[child_tmp.move]
            self.pindex_ucb.append(f"{index2}")
            self.printTreeHelper(child_tmp, level + 1, index1, index2, limit, topk)
            self.pindex_ucb.pop()


    # def mostPromisingMoves(self):
    #     current_node = self.root
    #     i = 1
    #     while not current_node.is_leaf():
    #         max_children = []
    #         max_ucb = float("-inf")
    #         for child in current_node.children:
    #             if child.visits != 0:
    #                 exploitation = child.wins / child.visits
    #                 exploration = self.c * math.sqrt(2*math.log(current_node.visits) / child.visits)
    #                 # print("Exploitation: " + str(exploitation) + ", Exploration: " + str(exploration) + ", UCB: " + str(exploitation + exploration))
    #                 info = (
    #                     exploitation, 
    #                     (child.wins, child.visits), 
    #                     exploration,
    #                     (current_node.visits, child.visits)
    #                 )
    #                 if exploration + exploitation > max_ucb:
    #                     max_ucb = exploration + exploitation
    #                     max_children = [(child, info)]
    #                 elif exploration + exploitation == max_ucb:
    #                     max_children.append((child, info))
    #         choice, info = random.choice(max_children)
    #         print("Step " + str(i) + ": " + str(choice.move) + ", UCB: " + str(max_ucb), info)
    #         i += 1
    #         current_node = choice
        