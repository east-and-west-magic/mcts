import chess
import chess.svg
import chess.engine
from node import Node
from mcts import MonteCarloTreeSearch


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
    if True:
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
        child_node7.add_child(child_node14)

        monte_carlo = MonteCarloTreeSearch(root_node, 2)



    
    # Tree 2
    if False:
        root_node
    

if __name__ == "__main__":
    main()