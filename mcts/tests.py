import chess
import chess.svg
import chess.engine
from node import Node
from mcts import MonteCarloTreeSearch


def main():
    root_node = Node(chess.Board(), None, chess.WHITE)
    print(root_node.is_leaf())
    child_node = Node(chess.Board(), root_node, chess.BLACK)
    child_node_2 = Node(chess.Board(), root_node, chess.BLACK)
    root_node.add_child(child_node)
    root_node.add_child(child_node_2)
    # print(user)
    print(root_node.is_leaf())
    # print(root_node)
    monte_carlo = MonteCarloTreeSearch(root_node, 2)
    monte_carlo.expansion(root_node)
    print(monte_carlo.selection())
    

if __name__ == "__main__":
    main()