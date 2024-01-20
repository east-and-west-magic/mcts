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

        root_node = Node(chess.Board("1r6/p1p3k1/4B1p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 1 27"), None, chess.WHITE, 0, 0, None)
        monte_carlo = MonteCarloTreeSearch(root_node, 1)

        # for i in tqdm(range(10)):
        for i in tqdm(range(50)):
            print("Test " + str(i + 1) + ":")
            current = monte_carlo.selection()
            if current.is_end():
                current_board = chess.Board(current.board.fen())
                assert current_board.is_game_over()
                outcome = monte_carlo.simulation(current)
                monte_carlo.backpropagation(current, outcome)
            else:
                child = monte_carlo.expansion(current)
                if child is None:
                    outcome = monte_carlo.simulation(current)
                    monte_carlo.backpropagation(current, outcome)
                else:
                    outcome = monte_carlo.simulation(child)
                    monte_carlo.backpropagation(child, outcome)

            ###################### 
            moves = []
            tmp = child
            while tmp.move is not None:
                moves.append(tmp.move)
                tmp = tmp.parent
            for level, move in enumerate(reversed(moves)):
                print(f"[steve] level: {level+1} move: {move} path: {[str(m) for m in reversed(moves)]}")

            monte_carlo.printTree()

        # print most promising path and see if it converges to chess engine's moves
        # tail -f a.txt
        # grep f5f7 a.txt| wc

if __name__ == "__main__":
    main()