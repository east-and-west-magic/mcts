import chess
import chess.svg
import chess.engine
from node import Node
from mcts import MonteCarloTreeSearch
from tqdm import tqdm


def main():
    import random
    random.seed(123)

    # Tree 6 - Strange Test Case, From Week-5/time6
    if True:

        pass

        # fen = "4k3/8/4K3/Q7/8/8/8/8 w - - 0 1"
        # fen = "2k5/8/2K5/Q7/8/8/8/8 w - - 0 1"
        # fen = "1k6/8/3K4/Q7/8/8/8/8 w - - 0 1"
        # fen = "8/k7/3K4/8/1Q6/8/8/8 w - - 0 1"
    
        # fen = "3Q4/4K3/8/2k5/8/8/8/8 w - - 0 1"

        # fen = "3k4/8/3PK3/8/8/8/8/8 w - - 1 3"
        # fen = "3k4/8/3K4/3P4/8/8/8/8 w - - 0 1"
        # fen = "8/6p1/5p2/5P2/4k1KP/8/8/8 w - - 0 1"
        fen = "1r6/p1p3k1/4B1p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 1 27"
        root_node = Node(chess.Board(fen), None, chess.WHITE, 0, 0, None)
        monte_carlo = MonteCarloTreeSearch(root_node, 3)

        # for i in tqdm(range(10)):
        for i in tqdm(range(1_000_000)):
            if i == 23:
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
                outcome = monte_carlo.simulation(current)
                monte_carlo.backpropagation(current, outcome)
                node_log = current
            else:
                child = monte_carlo.expansion(current)
                node_log = child
                if child is None:
                    node_log = current
                    outcome = monte_carlo.simulation(current)
                    monte_carlo.backpropagation(current, outcome)
                else:
                    node_log = child
                    outcome = monte_carlo.simulation(child)
                    monte_carlo.backpropagation(child, outcome)

            ###################### 
            nodes = node_log.path()
            for level, n in enumerate(nodes):
                if n.visits > 0:
                        import math
                        a = 1 - n.wins / n.visits
                        b = math.sqrt(2*math.log(n.parent.visits) / n.visits)
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

            monte_carlo.printTree()

        # print most promising path and see if it converges to chess engine's moves
        # tail -f a.txt
        # grep f5f7 a.txt| wc

if __name__ == "__main__":
    main()