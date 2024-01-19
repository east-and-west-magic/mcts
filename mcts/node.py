import chess

class Node:
    def __init__(self, board, parent, player, wins, visits, move):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = []
        self.wins = wins
        self.visits = visits
        self.move = move
        self.end = board.is_game_over()

    def __str__(self):
        return f"Board: {self.board.fen()}, Visits: {self.visits}, Wins: {self.wins}, Player: {'White' if self.player else 'Black'}"

    def update_wins(self, value):
        self.wins += value

    def update_visits(self):
        self.visits += 1
    
    def add_child(self, child):
        self.children.append(child)

    def is_leaf(self):
        return not self.children
    
    def is_end(self):
        return self.end
    
    def nodeRepresentation(self):
        moves = []
        tmp = self
        while tmp.move is not None:
            moves.append(tmp.move)
            tmp = tmp.parent
        for level, move in enumerate(reversed(moves)):
            # print(f"[steve] level: {level+1} move: {move} path: {[str(m) for m in reversed(moves)]}")
            pass

        return f"({self.wins/self.visits:.4f}, {1-self.wins/self.visits:.4f}, {self.wins}/{self.visits}, {[str(m) for m in reversed(moves)]}, {self.board.fen()}) "
    