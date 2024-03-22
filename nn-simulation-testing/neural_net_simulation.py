import chess
import chess.svg
import chess.engine
import random
from tqdm import tqdm
from queue import Queue
import csv
from typing import Any
from ctypes import *
import math
from operator import itemgetter
import pathlib
import numpy as np

def predict(boardFen, times, threshold):
    result = {'win': 0, 'lose': 0, 'draw': 0}
    nnue = cdll.LoadLibrary("./libnncpuprobe.so")
    nnue.nncpu_init(b"nn-04cf2b4ed1da.nnue")
    for x in tqdm(range(times)):
        board = chess.Board(boardFen)
        while not board.is_game_over():
            legal_moves = list(board.legal_moves)
            probs = []
            for m in legal_moves:
                temp_board = board.copy()
                temp_board.push(m)
                fen = temp_board.fen()
                score = nnue.nncpu_evaluate_fen(fen.encode())
                probs.append(score)
            probs = [prob - max(probs) for prob in probs]
            denominator = 0
            for p in probs:
                denominator += math.e**p
            for i in range(len(probs)):
                probs[i] = math.e**probs[i] / denominator
            random_number = random.random()
            move = None
            if random_number <= threshold:
                move = random.choice(legal_moves)
            else:
                move = np.random.choice(a=legal_moves, p=probs)
            board.push(move)
        res = board.result()
        if res == '1-0':
            result['win']+=1
        elif res == '0-1':
            result['lose']+=1
        else:
            result['draw']+=1
    return result

def predictv2(boardFen, times, threshold):
    result = {'win': 0, 'lose': 0, 'perfect': 0, 'draw': 0}
    nnue = cdll.LoadLibrary("./libnncpuprobe.so")
    nnue.nncpu_init(b"nn-04cf2b4ed1da.nnue")
    is_right_ending = True
    for x in tqdm(range(times)):
        board = chess.Board(boardFen)
        while not board.is_game_over():
            legal_moves = list(board.legal_moves)
            probs = []
            for m in legal_moves:
                temp_board = board.copy()
                temp_board.push(m)
                fen = temp_board.fen()
                score = nnue.nncpu_evaluate_fen(fen.encode())
                probs.append(score)
            probs = [prob - max(probs) for prob in probs]
            denominator = 0
            for p in probs:
                denominator += math.e**p
            for i in range(len(probs)):
                probs[i] = math.e**probs[i] / denominator
            random_number = random.random()
            move = None
            if random_number <= threshold:
                move = random.choice(legal_moves)
            else:
                move = np.random.choice(a=legal_moves, p=probs)
            board.push(move)
            if (not board.is_check()) and board.turn == chess.BLACK:
                is_right_ending = False
        res = board.result()
        if res == '1-0':
            result['win']+=1
        elif res == '0-1':
            result['lose']+=1
        elif is_right_ending:
            result['perfect']+=1
            print('perfect')
        else:
            result['draw']+=1
    return result

def main():
    if True:
        # is_right_ending = True
        # board = chess.Board("1r6/p1p3k1/4B1p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 1 27")
        # while not board.is_game_over():
        #     board.push(chess.Move.from_uci("f5f7"))
        #     print(board.fen())
        #     print(board)
        #     if (not board.is_check()) and board.turn == chess.BLACK:
        #         is_right_ending = False
        #     board.push(chess.Move.from_uci("g7g8"))
        #     print(board.fen())
        #     print(board)
        #     if (not board.is_check()) and board.turn == chess.BLACK:
        #         is_right_ending = False
        #     board.push(chess.Move.from_uci("f7f5"))
        #     if (not board.is_check()) and board.turn == chess.BLACK:
        #         is_right_ending = False
        #     board.push(chess.Move.from_uci("g8g7"))
        #     if (not board.is_check()) and board.turn == chess.BLACK:
        #         is_right_ending = False
        with open('./results4/threefold-5.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Wins", "Losses", "Perfect", "Draws", "Simulations", "Fen", "Random Threshold"])

            simulations = 10000
            times = 50
            # FEN is threefold repetition
            fen = "1r6/p1p3k1/4B1p1/5R2/8/1Pb5/q1P2PP1/3K3R w - - 1 27"

            for x in tqdm(range(times)):
                dict = predictv2(fen, simulations, 0.2)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['perfect'], dict['draw'], simulations, fen, 0.2])
            writer.writerow([""])
            
            for x in tqdm(range(times)):
                dict = predictv2(fen, simulations, 0.8)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['perfect'], dict['draw'], simulations, fen, 0.8])
            writer.writerow([""])

if __name__ == "__main__":
    main()