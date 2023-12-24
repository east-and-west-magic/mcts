import chess

class Node:
    def __init__(self, board, parent, player):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def __str__(self):
        return f"Board: {self.board.fen()}, Visits: {self.visits}, Wins: {self.wins}, Player: {'White' if self.player else 'Black'}"

    def update_wins(self):
        self.wins += 1

    def update_visits(self):
        self.visits += 1
    
    def add_child(self, child):
        self.children.append(child)

    def is_leaf(self):
        return not self.children

    