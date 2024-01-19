import chess
import chess.svg
import chess.engine
from node import Node
from mcts import MonteCarloTreeSearch
from tqdm import tqdm


def main():
    if False:
        root_node = Node(chess.Board(), None, chess.WHITE, 0, 0)
        child_node = Node(chess.Board(), root_node, chess.BLACK)
        child_node_2 = Node(chess.Board(), root_node, chess.BLACK)
        root_node.add_child(child_node)
        root_node.add_child(child_node_2)
        monte_carlo = MonteCarloTreeSearch(root_node, 2)
        monte_carlo.expansion(root_node)
        monte_carlo.selection()
    
    # Tree 1
    if False:
        root_node = Node(chess.Board("8/4bk1p/2p5/p1p1p3/q1P1P1Qp/2P1BP2/6K1/8 w - - 0 42"), None, chess.WHITE, 40, 100)

        child_node1 = Node(chess.Board("2Q5/4bk1p/2p5/p1p1p3/q1P1P2p/2P1BP2/6K1/8 b - - 1 42"), root_node, chess.BLACK, 30, 50)
        root_node.add_child(child_node1)
        child_node2 = Node(chess.Board("8/4bkQp/2p5/p1p1p3/q1P1P2p/2P1BP2/6K1/8 b - - 1 42"), root_node, chess.BLACK, 30, 50)
        root_node.add_child(child_node2)

        child_node3 = Node(chess.Board("2Q5/4b2p/2p3k1/p1p1p3/q1P1P2p/2P1BP2/6K1/8 w - - 2 43"), child_node1, chess.WHITE, 15, 30)
        child_node1.add_child(child_node3)
        child_node4 = Node(chess.Board("2Q5/4b2p/2p2k2/p1p1p3/q1P1P2p/2P1BP2/6K1/8 w - - 2 43"), child_node1, chess.WHITE, 5, 20)
        child_node1.add_child(child_node4)
        child_node5 = Node(chess.Board("8/4b1kp/2p5/p1p1p3/q1P1P2p/2P1BP2/6K1/8 w - - 0 43"), child_node2, chess.WHITE, 10, 25)
        child_node2.add_child(child_node5)
        child_node6 = Node(chess.Board("8/4b1Qp/2p1k3/p1p1p3/q1P1P2p/2P1BP2/6K1/8 w - - 2 43"), child_node2, chess.WHITE, 10, 25)
        child_node2.add_child(child_node6)

        child_node7 = Node(chess.Board("6Q1/4b2p/2p3k1/p1p1p3/q1P1P2p/2P1BP2/6K1/8 b - - 3 43"), child_node3, chess.BLACK, 10, 15)
        child_node3.add_child(child_node7)
        child_node8 = Node(chess.Board("5Q2/4b2p/2p3k1/p1p1p3/q1P1P2p/2P1BP2/6K1/8 b - - 3 43"), child_node3, chess.BLACK, 5, 15)
        child_node3.add_child(child_node8)
        child_node9 = Node(chess.Board("6Q1/4b2p/2p2k2/p1p1p3/q1P1P2p/2P1BP2/6K1/8 b - - 3 43"), child_node4, chess.BLACK, 7, 10)
        child_node4.add_child(child_node9)
        child_node10 = Node(chess.Board("5Q2/4b2p/2p2k2/p1p1p3/q1P1P2p/2P1BP2/6K1/8 b - - 3 43"), child_node4, chess.BLACK, 8, 10)
        child_node4.add_child(child_node10)
        child_node11 = Node(chess.Board("8/4b1kp/2p5/p1p1p1B1/q1P1P2p/2P2P2/6K1/8 b - - 1 43"), child_node5, chess.BLACK, 10, 15)
        child_node5.add_child(child_node11)
        child_node12 = Node(chess.Board("8/4b1kp/2p5/p1B1p3/q1P1P2p/2P2P2/6K1/8 b - - 0 43"), child_node5, chess.BLACK, 5, 10)
        child_node5.add_child(child_node12)
        child_node13 = Node(chess.Board("6Q1/4b2p/2p1k3/p1p1p3/q1P1P2p/2P1BP2/6K1/8 b - - 3 43"), child_node6, chess.BLACK, 9, 15)
        child_node6.add_child(child_node13)
        child_node14 = Node(chess.Board("5Q2/4b2p/2p1k3/p1p1p3/q1P1P2p/2P1BP2/6K1/8 b - - 3 43"), child_node6, chess.BLACK, 6, 10)
        child_node6.add_child(child_node14)

        if True:
            print("test 1")
            monte_carlo = MonteCarloTreeSearch(root_node, 2)
            current = monte_carlo.selection()
            print("children")
            monte_carlo.expansion(current)
            for child in current.children:
                print(child)
        if False:
            print("test 2")
            monte_carlo = MonteCarloTreeSearch(root_node, 10000)
            current = monte_carlo.selection()
            print("children")
            monte_carlo.expansion(current)
            for child in current.children:
                print(child)

        if True:
            print("test 3")
            monte_carlo = MonteCarloTreeSearch(root_node, 2)
            monte_carlo.selection()

            print("test 4")
            monte_carlo2 = MonteCarloTreeSearch(root_node, 100)
            monte_carlo2.selection()


    # Tree 2
    if False:
        root_node = Node(chess.Board("8/8/8/1p6/2b5/2kp4/8/4K3 w - - 0 171"), None, chess.WHITE, 11, 21)

        child_node1 = Node(chess.Board("8/4bkQp/2p5/p1p1p3/q1P1P2p/2P1BP2/6K1/8 b - - 1 42"), root_node, chess.BLACK, 7, 10)
        root_node.add_child(child_node1)
        child_node2 = Node(chess.Board("8/8/8/1p6/2b5/2kp4/8/3K4 b - - 1 171"), root_node, chess.BLACK, 3, 8)
        root_node.add_child(child_node2)
        child_node3 = Node(chess.Board("8/8/8/1p6/2b5/2kp4/5K2/8 b - - 1 171"), root_node, chess.BLACK, 0, 3)
        root_node.add_child(child_node3)

        child_node4 = Node(chess.Board("8/5b2/8/1p6/8/2kp4/8/5K2 w - - 2 172"), child_node1, chess.WHITE, 2, 4)
        child_node1.add_child(child_node4)
        child_node5 = Node(chess.Board("8/8/4b3/1p6/8/2kp4/8/5K2 w - - 2 172"), child_node1, chess.WHITE, 1, 6)
        child_node1.add_child(child_node5)
        child_node6 = Node(chess.Board("6b1/8/8/1p6/8/2kp4/8/3K4 w - - 2 172"), child_node2, chess.WHITE, 1, 2)
        child_node2.add_child(child_node6)
        child_node7 = Node(chess.Board("8/5b2/8/1p6/8/2kp4/8/3K4 w - - 2 172"), child_node2, chess.WHITE, 2, 3)
        child_node2.add_child(child_node7)
        child_node8 = Node(chess.Board("8/8/4b3/1p6/8/2kp4/8/3K4 w - - 2 172"), child_node2, chess.WHITE, 2, 3)
        child_node2.add_child(child_node8)

        child_node9 = Node(chess.Board("8/5b2/8/1p6/8/2kp4/8/4K3 b - - 3 172"), child_node4, chess.BLACK, 2, 3)
        child_node5.add_child(child_node9)
        child_node10 = Node(chess.Board("8/5b2/8/1p6/8/2kp4/8/2K5 b - - 3 172"), child_node4, chess.BLACK, 3, 3)
        child_node5.add_child(child_node10)

        if False:
            print("test 1")
            monte_carlo = MonteCarloTreeSearch(root_node, 100)
            current = monte_carlo.selection()
            print("children")
            monte_carlo.expansion(current)
            for child in current.children:
                print(child)
        if False:
            print("test 2")
            monte_carlo = MonteCarloTreeSearch(root_node, 5)
            current = monte_carlo.selection()
            print("children")
            monte_carlo.expansion(current)
            for child in current.children:
                print(child)
        
        if True:
            print("test 3")
            monte_carlo = MonteCarloTreeSearch(root_node, 2)
            monte_carlo.selection()

            print("test 4")
            monte_carlo2 = MonteCarloTreeSearch(root_node, 100)
            monte_carlo2.selection()
    
    # Tree 3
    if False:
        root_node = Node(chess.Board("1r6/p1p3k1/4B1p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 1 27"), None, chess.WHITE, 80, 200)

        child_node1 = Node(chess.Board("1r4B1/p1p3k1/6p1/5R2/8/1Pb5/q1P2PP1/3K3R b - - 2 27"), root_node, chess.BLACK, 60, 100)
        root_node.add_child(child_node1)
        child_node2 = Node(chess.Board("1rB5/p1p3k1/6p1/5R2/8/1Pb5/q1P2PP1/3K3R b - - 2 27"), root_node, chess.BLACK, 60, 100)
        root_node.add_child(child_node2)

        child_node3 = Node(chess.Board("6r1/p1p3k1/6p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 0 28"), child_node1, chess.WHITE, 30, 60)
        child_node1.add_child(child_node3)
        child_node4 = Node(chess.Board("5rB1/p1p3k1/6p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 3 28"), child_node1, chess.WHITE, 10, 40)
        child_node1.add_child(child_node4)
        child_node5 = Node(chess.Board("2r5/p1p3k1/6p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 0 28"), child_node2, chess.WHITE, 20, 50)
        child_node2.add_child(child_node5)
        child_node6 = Node(chess.Board("r1B5/p1p3k1/6p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 3 28"), child_node2, chess.WHITE, 20, 50)
        child_node2.add_child(child_node6)

        child_node7 = Node(chess.Board("5Rr1/p1p3k1/6p1/8/8/1Pb5/q1P2PP1/3K3R b - - 1 28"), child_node3, chess.BLACK, 20, 30)
        child_node3.add_child(child_node7)
        child_node8 = Node(chess.Board("6r1/p1p2Rk1/6p1/8/8/1Pb5/q1P2PP1/3K3R b - - 1 28"), child_node3, chess.BLACK, 10, 30)
        child_node3.add_child(child_node8)
        child_node9 = Node(chess.Board("5r2/p1p3kB/6p1/5R2/8/1Pb5/q1P2PP1/3K3R b - - 4 28"), child_node4, chess.BLACK, 14, 20)
        child_node4.add_child(child_node9)
        child_node10 = Node(chess.Board("5r2/p1p2Bk1/6p1/5R2/8/1Pb5/q1P2PP1/3K3R b - - 4 28"), child_node4, chess.BLACK, 16, 20)
        child_node4.add_child(child_node10)
        child_node11 = Node(chess.Board("2r2R2/p1p3k1/6p1/8/8/1Pb5/q1P2PP1/3K3R b - - 1 28"), child_node5, chess.BLACK, 20, 30)
        child_node5.add_child(child_node11)
        child_node12 = Node(chess.Board("2r5/p1p2Rk1/6p1/8/8/1Pb5/q1P2PP1/3K3R b - - 1 28"), child_node5, chess.BLACK, 10, 20)
        child_node5.add_child(child_node12)
        child_node13 = Node(chess.Board("r7/p1pB2k1/6p1/5R2/8/1Pb5/q1P2PP1/3K3R b - - 4 28"), child_node6, chess.BLACK, 18, 30)
        child_node6.add_child(child_node13)
        child_node14 = Node(chess.Board("r7/pBp3k1/6p1/5R2/8/1Pb5/q1P2PP1/3K3R b - - 4 28"), child_node6, chess.BLACK, 12, 20)
        child_node6.add_child(child_node14)

        if False:
            print("test 1")
            monte_carlo = MonteCarloTreeSearch(root_node, 2)
            current = monte_carlo.selection()
            # print("children")
            monte_carlo.expansion(current)
            # for child in current.children:
                # print(child)
        if False:
            print("test 2")
            monte_carlo = MonteCarloTreeSearch(root_node, 10000)
            current = monte_carlo.selection()
            print("children")
            monte_carlo.expansion(current)
            # for child in current.children:
                # print(child)
            
        if True:
            # print("test 3")
            # monte_carlo = MonteCarloTreeSearch(root_node, 2)
            # monte_carlo.selection()

            for i in range(5):
                print("test " + str(i))
                monte_carlo2 = MonteCarloTreeSearch(root_node, 1)
                current = monte_carlo2.selection()
                # print("current: " + str(current))
                child = monte_carlo2.expansion(current)
                print("child: " + str(child))
                outcome = monte_carlo2.simulation(child)
                print("outcome: " + str(outcome))
                monte_carlo2.backpropagation(child, outcome)

    # Tree 4 - Strong Loss, From Week-5/time2
    if False:
        root_node = Node(chess.Board("8/8/8/1p6/2b5/2kp4/8/4K3 w - - 0 171"), None, chess.WHITE, 0, 0)
        for i in range(100):
            print("test " + str(i + 1))
            monte_carlo = MonteCarloTreeSearch(root_node, 100)
            current = monte_carlo.selection()
            if not current.is_end():
                # print("current: " + str(current))
                child = monte_carlo.expansion(current)
                print("child: " + str(child))
                outcome = monte_carlo.simulation(child)
                print("outcome: " + str(outcome))
                monte_carlo.backpropagation(child, outcome)

    # Tree 5 - Strong Win, From Week-5/time6
    if False:
        root_node = Node(chess.Board("n7/P4r2/2P1N3/2K5/R7/6kP/8/8 w - - 1 69"), None, chess.WHITE, 0, 0)
        for i in range(100):
            print("test " + str(i + 1))
            monte_carlo = MonteCarloTreeSearch(root_node, 100)
            current = monte_carlo.selection()
            if not current.is_end():
                # print("current: " + str(current))
                child = monte_carlo.expansion(current)
                print("child: " + str(child))
                outcome = monte_carlo.simulation(child)
                print("outcome: " + str(outcome))
                monte_carlo.backpropagation(child, outcome)

    # Tree 6 - Strange Test Case, From Week-5/time6
    if True:
        import random
        random.seed(123)

        root_node = Node(chess.Board("1r6/p1p3k1/4B1p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 1 27"), None, chess.WHITE, 0, 0, None)
        monte_carlo = MonteCarloTreeSearch(root_node, 1)

        # for i in tqdm(range(10)):
        for i in tqdm(range(100)):
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

            if True:
                if "f5f7" in [str(m) for m in reversed(moves)][:1]:
                    monte_carlo.printTree()
                elif i < 20:
                    monte_carlo.printTree()
                elif i < 200:
                    if (i+1) % 10 == 0:
                        monte_carlo.printTree()
                elif i < 2000:
                    if (i+1) % 100 == 0:
                        monte_carlo.printTree()
                else:
                    if (i+1) % 1_000 == 0:
                        monte_carlo.printTree()
            ###################### 

            print("")

        # print most promising path and see if it converges to chess engine's moves
        # tail -f a.txt
        # grep f5f7 a.txt| wc

if __name__ == "__main__":
    main()