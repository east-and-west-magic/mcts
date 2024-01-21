import chess
import chess.svg
import chess.engine
from node import Node
from mcts import MonteCarloTreeSearch
from tqdm import tqdm


def main():
    import random
    random.seed(123)

    n_simu = 100
    n_mcts = 100
    n_show = 1

    # Tree 6 - Strange Test Case, From Week-5/time6
    if True:

        # fen = "4k3/8/4K3/Q7/8/8/8/8 w - - 0 1"
        # fen = "2k5/8/2K5/Q7/8/8/8/8 w - - 0 1"
        # fen = "1k6/8/3K4/Q7/8/8/8/8 w - - 0 1"
        # fen = "8/k7/3K4/8/1Q6/8/8/8 w - - 0 1"
    
        # fen = "8/8/8/1R6/2K5/8/k7/8 w - - 0 1" # rook ending DTM: 4
        # fen = "8/8/8/8/2K5/k7/8/1R6 w - - 0 1" # rook ending DTM: 6 # BUG: Rb2
        fen = "8/8/8/8/2k5/K7/1r6/8 w - - 0 1" # rook ending DTD: 1
        # fen = "8/8/8/8/2K5/k7/1R6/8 b - - 0 1" # rook ending DTM: 1 or draw
        # fen = "8/3K4/8/8/8/k7/8/1Q6 w - - 0 1" # queen ending DTM: 4

        # fen = "8/1Q1K4/8/8/k7/8/8/8 w - - 0 1" # queen ending DTM: 6
        # fen = "3Q4/4K3/8/2k5/8/8/8/8 w - - 0 1" # queen ending DTM: 10

        # fen = "3k4/8/3PK3/8/8/8/8/8 w - - 1 3" # easy pawn ending
        # fen = "3k4/8/3K4/3P4/8/8/8/8 w - - 0 1"
        # fen = "8/6p1/5p2/5P2/4k1KP/8/8/8 w - - 0 1"

        # fen = "1r6/p1p2Rk1/4B1p1/8/8/1Pb5/q1P2PP1/3K3R b - - 2 27" # super hard, 3 fold repetition

        # fen = "4K3/8/8/8/8/8/3k4/q6R w - - 0 1" # hard, rook ending
        # fen = "4k3/8/8/8/8/8/8/Q3K2r w - - 0 1"
        # fen = "4k2r/8/8/8/8/8/8/Q3K3 b - - 0 1"
        # fen = "4k2r/8/8/8/8/8/8/3QK3 w - - 0 1"

        # fen = "1r4k1/p1p2R2/4B1p1/8/8/1Pb5/q1P2PP1/3K3R w - - 3 28"
        # fen = "1r6/p1p3k1/4B1p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 1 27"
        root_node = Node(chess.Board(fen), None, chess.WHITE, 0, 0, None)
        monte_carlo = MonteCarloTreeSearch(root_node, 1)

        for i in tqdm(range(n_mcts)):
            if (i == 79) or (i == 30):
                pass

            print("Test " + str(i + 1) + ":")
            current = monte_carlo.selection()

            moves = []
            tmp = current
            while tmp.move is not None:
                moves.append(str(tmp.move))
                tmp = tmp.parent


            if moves == ['g4h5', 'e4f5']:
                pass

            node_log = None
            if current.is_end():
                current_board = chess.Board(current.board.fen())
                assert current_board.is_game_over()
                child = current
            else:
                child = monte_carlo.expansion(current)
                node_log = child
                if child is None:
                    child = current

            node_log = child
            for _ in range(n_simu):
                outcome = monte_carlo.simulation(child)
                monte_carlo.backpropagation(child, outcome)

            ###################### 
            nodes = node_log.path()
            for level, n in enumerate(nodes):
                if n.visits > 0:
                        import math
                        a = 1 - n.wins / n.visits
                        b = monte_carlo.c * math.sqrt(2 * math.log(n.parent.visits) / n.visits)
                        print(
                        f"[steve] level: {level+1},",
                        f"move: {n.move},",
                        f"ucb: {a + b:.4f} ({a:.4f}+{b:.4f}),",
                        f"winrate: {1-n.wins/n.visits},",
                        f"win: {n.visits-n.wins},",
                        f"visits: {n.visits},", 
                        f"pvisits: {n.parent.visits},", 
                        f"path: {[str(n.move) for n in nodes]}"
                    )
                else:
                    print(
                        f"[steve] level: {level+1},",
                        f"move: {n.move},",
                        # f"winrate: {1-n.wins/n.visits},",
                        f"win: {n.visits-n.wins},",
                        f"visits: {n.visits},",
                        f"path: {[str(n.move) for n in nodes]}"
                    )

            if (i + 1) % n_show == 0:
                monte_carlo.printTree()
            else:
                # monte_carlo.printTree()
                pass

        # print most promising path and see if it converges to chess engine's moves
        # tail -f a.txt
        # grep f5f7 a.txt| wc

if __name__ == "__main__":
    main()
