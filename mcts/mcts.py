from typing import Any
import chess
import random
import math
from node import Node
from operator import itemgetter
import pathlib

import cppyy
# cppyy.include("mcts/chess.hpp")
cppyy.include(pathlib.Path(__file__).parent / "chess.hpp")
from cppyy.gbl import chess as cppchess


debug = False


class MonteCarloTreeSearch:
    def __init__(self, root_node: Node, c: float):
        self.root: Node = root_node
        self.c: float = c
        self.mate_in_1: dict = {}
        # self.be_mated_in_1: dict = {}
        # self.mate_in_2: dict = {}
    

    def selection(self) -> Node:
        current: Node = self.root
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
                move = child_board.san_and_push(legal_move)
                child_node = Node(
                    child_board, 
                    current_node, 
                    chess.BLACK if current_node.player else chess.WHITE, 
                    0, 
                    0, 
                    move,
                )
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


    def expansion(self, current_node: Node) -> Node | None:
        
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
            move = child_board.san_and_push(legal_move)
            child_node = Node(
                child_board, 
                current_node, 
                chess.BLACK if current_node.player else chess.WHITE, 
                0, 
                0, 
                move,
            )
            current_node.add_child(child_node)
        if current_node.children: # how to deal with
            return random.choice(current_node.children) # just simulate one time
        else:
            return None


    # all_results = set(
    #     cppchess.GameResultReason.CHECKMATE,
    #     cppchess.GameResultReason.STALEMATE,
    #     cppchess.GameResultReason.INSUFFICIENT_MATERIAL,
    #     cppchess.GameResultReason.FIFTY_MOVE_RULE,
    #     cppchess.GameResultReason.THREEFOLD_REPETITION,
    #     cppchess.GameResultReason.NONE,
    # )

    def simulation_cpp(self, current_node: Node) -> str:
        fen = current_node.board.fen()
        board = cppchess.Board(fen)
        # moves = cppchess.Movelist()
        while board.isGameOver().second == cppchess.GameResult.NONE:
            # for _ in range(50):
            moves = cppchess.Movelist()
            cppchess.movegen.legalmoves(moves, board)
            t = [str(cppchess.uci.moveToSan(board, move)) for move in moves]
            sorted_moves = sorted(zip(t, moves))
            # if len(moves) == 0:
            #     break
            move = random.choice(sorted_moves)
            # print(chess.uci.moveToSan(board, move))
            board.makeMove(move[1])
        # result = board.isGameOver().first
        # assert result in all_results
        result_fen = board.getFen()
        result_board = chess.Board(result_fen)
        return result_board.result()


    def simulation_python(self, current_node: Node) -> str:
        current_board = chess.Board(current_node.board.fen())        
        while not current_board.is_game_over():
            moves = list(current_board.legal_moves)
            t = [str(current_board.san(move)) for move in moves]

            ##############
            if debug:
                fen = current_board.fen()
                # fen = current_node.board.fen()
                cppboard = cppchess.Board(fen)
                if cppboard.isGameOver().second != cppchess.GameResult.NONE:
                    # raise Exception("different game over situation!!!")
                    pass
                cppmoves = cppchess.Movelist()
                cppchess.movegen.legalmoves(cppmoves, cppboard)
                cppt = [str(cppchess.uci.moveToSan(cppboard, move)) for move in cppmoves]
                if sorted(cppt) != sorted(t):
                    raise Exception('diffent legal moves!!!')
            ##############

            sorted_moves = sorted(zip(t, moves))
            move = random.choice(sorted_moves)
            current_board.push(move[1])

        ############################
        if debug:
            fen = current_board.fen()
            # fen = current_node.board.fen()
            cppboard = cppchess.Board(fen)
            if cppboard.isGameOver().second == cppchess.GameResult.NONE:
                # raise Exception("different game over situation!!!")
                pass
        ############################
        return current_board.result()

 
    def backpropagation(self, current_node:Node, outcome: float) -> None:
        while current_node:
            if (current_node.player and outcome == "1-0") or (not current_node.player and outcome == "0-1"):
                current_node.update_wins(1)
            elif outcome == "1/2-1/2":
                current_node.update_wins(0.5)
            current_node.update_visits()
            current_node = current_node.parent


    def printTree(self, limit: int, topk: int) -> None:
        def printTreeHelper(node: Node, 
                            level: int, 
                            index_win_rate: float, 
                            index_ucb: int, 
                            limit: int, 
                            topk: int,
        ) -> None:
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

            if level % 2 == 0:
                color_code = "31" # red opponent
            else:
                # color_code = "34" # blue, myself
                color_code = "32" # green, myself
            if node.visits == 0:
                color_code = "39"

            win_rate_with_color = f"\033[{color_code}m{win_rate:.4f}\033[0m"
            # if you cannot get color to work on your system, use this:
            # win_rate_with_color = f"{win_rate:.4f}"

            str += f"|--"
            str += f" {win_rate_with_color}"
            str += f" [{index_win_rate}:{index_ucb}]"
            str += f" [({len(pindex_ucb)}) {'/'.join(pindex_ucb)}]"
            str += f" {node.node_repr(self.c)}"
            print(str)

            children_ucb = self.sort_children_by(node, True) # get a list
            children_win_rate = self.sort_children_by(node, False) # get a dict

            if level > 0 and topk > 0:
                children_win_rate = children_win_rate[:topk]
            for (index1, child_tmp) in reversed(children_win_rate):
                index2 = children_ucb[child_tmp.move]
                pindex_ucb.append(f"{index2}")
                printTreeHelper(child_tmp, level + 1, index1, index2, limit, topk)
                pindex_ucb.pop()


        print("Tree: ")
        pindex_ucb: list[int] = []
        printTreeHelper(self.root, 0, 0, 0, limit, topk)


    def sort_children_by(self, node: Node, ucb: bool=True) -> Any:
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
