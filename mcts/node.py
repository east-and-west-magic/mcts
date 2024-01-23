from __future__ import annotations
from typing import List
import math
import chess


class Node:
    def __init__(self, 
                 board: chess.Board, 
                 parent: Node, 
                 player: bool, 
                 wins: float, 
                 visits: int, 
                 move: str):
        self.board = board
        self.parent = parent
        self.player = player
        self.wins = wins
        self.visits = visits
        self.move = move

        self.children = []


    def __str__(self) -> str:
        return \
            f"Board: {self.board.fen()}," \
            f"Visits: {self.visits}," \
            f"Wins: {self.wins}," \
            f"Player: {'White' if self.player else 'Black'}"


    def update_wins(self, value: float) -> None:
        self.wins += value


    def update_visits(self, value: int = 1) -> None:
        self.visits += value


    def add_child(self, child: Node) -> None:
        self.children.append(child)


    def is_leaf(self) -> bool:
        return not self.children
    
    
    def is_end(self) -> bool:
        return self.board.is_game_over()


    def get_nodes(self) -> List[Node]:
        """
        get all the parent nodes based on the current node.
        The output will be root->...->current_node.
        """
        nodes = []
        current = self
        while current.parent:
            nodes.append(current)
            current = current.parent
        nodes.reverse()
        return nodes
    

    def get_moves(self) -> List[str]:
        return [n.move for n in self.get_nodes()]
    

    def get_win_rate(self) -> float:
        return self.wins / self.visits


    def get_lose_rate(self) -> float:
        return 1 - self.get_win_rate()


    def get_curious_rate(self) -> float:
        return math.sqrt(2*math.log(self.parent.visits) / self.visits)


    def get_ucb(self, c: float) -> float:
        return self.get_win_rate() + c * self.get_curious_rate()


    def get_ucb2(self, c: float) -> float:
        return self.get_lose_rate() + c * self.get_curious_rate()


    def node_repr(self, c) -> str:
        moves = self.get_moves()
        if self.parent is None:
            return \
                f"win: {self.visits-self.wins}, " \
                f"visits: {self.visits}, " \
                f"[], " \
                f"[{len(moves)} {'/'.join(moves)}]"
                # f"{self.board.fen()}"
        
        if self.visits > 0:
                a = self.get_lose_rate()
                b = self.get_curious_rate()
                return \
                f"ucb: {self.get_ucb2(c):.4f} (({self.visits-self.wins}/{self.visits}) {a:.4f}+{b:.4f}), " \
                f"[{self.move}], " \
                f"[{len(moves)} {'/'.join(moves)}]"
                # f"{n.board.fen()}"

        return \
            f"ucb: {float('inf')}, " \
            f"[{self.move}], " \
            f"[{len(moves)} {'/'.join(moves)}]"
            # f"{n.board.fen()}"


    # def nodeRepresentation(self) -> str:
    #     if self.visits == 0:
    #         return f"({self.board.fen()}) "
    #     else:
    #         return f"({self.wins}/{self.visits}, {self.board.fen()}) "
    