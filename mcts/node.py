class Node:
    def __init__(self, board, parent, player, wins, visits, move):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = []
        self.wins = wins
        self.visits = visits
        self.move = move


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
    
    
    def path(self):
        """
        get all the parent nodes based on the current node.
        The output will be root->...->current_node.
        """
        nodes = []
        tmp = self
        while tmp.parent:
            nodes.append(tmp)
            tmp = tmp.parent
        nodes.reverse()
        return nodes
    

    def is_end(self):
        return self.board.is_game_over()
    

    def nodeRepresentation(self, c):
        n = self # BAD. I will change it later. TODO: change n.* to self.*
        moves = '/'.join([n.move for n in n.path()])
        lmoves = len(n.path())
        if n.parent is None:
            return \
                f"win: {n.visits-n.wins}, " \
                f"visits: {n.visits}, " \
                f"[], " \
                f"[{lmoves} {moves}]"
                # f"{self.board.fen()}"
        
        if n.visits > 0:
                import math
                a = 1 - n.wins / n.visits
                b = c * math.sqrt(2*math.log(n.parent.visits) / n.visits)
                return \
                f"ucb: {a + b:.4f} (({n.visits-n.wins}/{n.visits}) {a:.4f}+{b:.4f}), " \
                f"[{n.move}], " \
                f"[{lmoves} {moves}]"
                # f"{n.board.fen()}"
        else:
            return \
                f"ucb: {float('inf')}, " \
                f"[{n.move}], " \
                f"[{lmoves} {moves}]"
                # f"{n.board.fen()}"

        # if self.visits == 0:
        #     return f"({self.visits-self.wins}/{self.visits}, {[str(m) for m in reversed(moves)]}, {self.board.fen()}) "
        # else:
        #     return f"({1-self.wins/self.visits:.4f}, {self.wins/self.visits:.4f}, {self.visits-self.wins}/{self.visits}, {[str(m) for m in reversed(moves)]}, {self.board.fen()}) "
    