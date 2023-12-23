class Node:
    def __init__(self, board, parent, player):
        self.board = board
        self.children = []
        self.parent = parent
        self.wins = 0
        self.visits = 0
        self.player = player

    