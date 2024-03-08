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

def softmax(x):
    x = x - np.max(x)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)

def predictv1(boardFen, times):
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
            probs = softmax(probs)
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

def predictv2(boardFen, times):
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
            probs[0] = math.e**probs[0] / denominator
            for i in range(len(probs) - 1):
                probs[i + 1] = math.e**probs[i + 1] / denominator + probs[i]
            random_number = random.random()
            move = None
            for i in range(len(probs)):
                if (random_number <= probs[i]):
                    move = legal_moves[i]
                    break
            board.push(move)
        res = board.result()
        if res == '1-0':
            result['win']+=1
        elif res == '0-1':
            result['lose']+=1
        else:
            result['draw']+=1
    return result

def main():
    if False:
        with open('./results/a.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Wins", "Losses", "Draws", "Simulations", "Fen", "End Result"])

            simulations = 1000
            times = 25
            # first FEN in time6.csv
            fen = "8/1K1r4/8/8/8/8/6k1/1R6 w - - 37 109"
            
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "1/2-1/2"])
            writer.writerow([""])

            simulations = 5000
            times = 25
            fen = "8/1K1r4/8/8/8/8/6k1/1R6 w - - 37 109"
            
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "1/2-1/2"])
            writer.writerow([""])

            simulations = 10000
            times = 25
            fen = "8/1K1r4/8/8/8/8/6k1/1R6 w - - 37 109"
            
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "1/2-1/2"])
            writer.writerow([""])

            simulations = 50000
            times = 25
            fen = "8/1K1r4/8/8/8/8/6k1/1R6 w - - 37 109"
            
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "1/2-1/2"])
            writer.writerow([""])

    if False:
        with open('./results/b.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Wins", "Losses", "Draws", "Simulations", "Fen", "End Result"])

            simulations = 1000
            times = 25
            # first FEN in time6.csv
            fen = "8/8/8/1p6/2b5/2kp4/8/4K3 w - - 0 171"
            
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

            simulations = 2500
            
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

            simulations = 5000
            
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

            simulations = 7500
            
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

            simulations = 10000
            
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

            simulations = 20000
            
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

    if True:
        with open('./results/c.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Wins", "Losses", "Draws", "Simulations", "Fen"])

            simulations = 1000
            times = 25
            # FEN in main.py
            fen = "8/8/r7/8/8/2k5/8/1K6 b - - 0 1"

            for x in tqdm(range(times)):
                dict = predictv1(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen])
            writer.writerow([""])

            simulations = 5000
            
            for x in tqdm(range(times)):
                dict = predictv1(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen])
            writer.writerow([""])

            simulations = 10000
            
            for x in tqdm(range(times)):
                dict = predictv1(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen])
            writer.writerow([""])
        
        with open('./results/d.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Wins", "Losses", "Draws", "Simulations", "Fen"])

            simulations = 1000
            times = 25
            # FEN in main.py
            fen = "8/8/r7/8/8/2k5/8/1K6 b - - 0 1"

            for x in tqdm(range(times)):
                dict = predictv2(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen])
            writer.writerow([""])

            simulations = 5000
            
            for x in tqdm(range(times)):
                dict = predictv2(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen])
            writer.writerow([""])

            simulations = 10000
            
            for x in tqdm(range(times)):
                dict = predictv2(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen])
            writer.writerow([""])
        
        with open('./results/e.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Wins", "Losses", "Draws", "Simulations", "Fen", "End Result"])

            simulations = 1000
            times = 25
            # FEN in time6.csv
            fen = "8/8/8/3k4/8/2K1r3/8/8 w - - 12 75"

            for x in tqdm(range(times)):
                dict = predictv1(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

            simulations = 5000
            
            for x in tqdm(range(times)):
                dict = predictv1(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

            simulations = 10000
            
            for x in tqdm(range(times)):
                dict = predictv1(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])
        
        with open('./results/f.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Wins", "Losses", "Draws", "Simulations", "Fen", "End Result"])

            simulations = 1000
            times = 25
            # FEN in time6.csv
            fen = "8/8/8/3k4/8/2K1r3/8/8 w - - 12 75"

            for x in tqdm(range(times)):
                dict = predictv2(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

            simulations = 5000
            
            for x in tqdm(range(times)):
                dict = predictv2(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

            simulations = 10000
            
            for x in tqdm(range(times)):
                dict = predictv2(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, fen, "0-1"])
            writer.writerow([""])

if __name__ == "__main__":
    main()