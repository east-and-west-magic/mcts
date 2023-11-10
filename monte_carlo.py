import chess
import chess.svg
import chess.engine
import random
from tqdm import tqdm
from queue import Queue
import csv

def predict(boardFen, times):
    result = {'win': 0, 'lose': 0, 'draw': 0}
    for x in tqdm(range(times)):
        board = chess.Board(boardFen)
        while not board.is_game_over():
            moves = list(board.legal_moves)
            r = random.randint(0, len(moves) - 1)
            moveChosen = moves[r]
            board.push(moveChosen)
        res = board.result()
        if res == '1-0':
            result['win']+=1
        elif res == '0-1':
            result['lose']+=1
        else:
            result['draw']+=1
    return result

def generateConfig(movesFromEnd, parameter, whiteStrength, blackStrength):
    engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\amyta\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe")
    fenQueue = Queue(maxsize = movesFromEnd) 
    board = chess.Board()
    if parameter == 'time':
        while not board.is_game_over():
            res = engine.play(board, chess.engine.Limit(time=whiteStrength['time']))
            board.push(res.move)

            res = engine.play(board, chess.engine.Limit(time=blackStrength['time']))
            board.push(res.move)

            if (fenQueue.full()):
                fenQueue.get()
            fenQueue.put(board.fen())
    elif parameter == 'depth':
        while not board.is_game_over():
            res = engine.play(board, chess.engine.Limit(depth=whiteStrength['depth']))
            board.push(res.move)

            res = engine.play(board, chess.engine.Limit(depth=blackStrength['depth']))
            board.push(res.move)

            if (fenQueue.full()):
                fenQueue.get()
            fenQueue.put(board.fen())
    else:
        while not board.is_game_over():
            res = engine.play(board, chess.engine.Limit(nodes=whiteStrength['nodes']))
            board.push(res.move)

            res = engine.play(board, chess.engine.Limit(nodes=blackStrength['nodes']))
            board.push(res.move)

            if (fenQueue.full()):
                fenQueue.get()
            fenQueue.put(board.fen())


    engine.quit()
    return fenQueue.get()

def main():
    # using hardcoded configuration
    if False:
        print(predict('8/8/8/p7/2kb4/7r/2K5/5R2 w - - 4 41', 1000))
        # using hardcoded configuration where black is one move from winning
        print(predict('8/7p/7r/4K3/5q1r/8/6k1/1R6 w - - 2 81', 1000))

        # using generated configuration where white is stronger
        fen = generateConfig(35, {'time': 0.1, 'depth': 20, 'nodes': 1000}, {'time': 0.01, 'depth': 1, 'nodes': 5})
        # print(chess.Board(fen))
        # print(fen)
        print(predict(fen, 1000))
        # most results end in a draw
        f = open("results.txt", "a")
        simulations = 50000
        times = 50
        # fen = generateConfig(35, {'time': 0.1, 'depth': 20, 'nodes': 10000}, {'time': 0.1, 'depth': 20, 'nodes': 5000})
        f.write('board configuration with fen representation: ' + fen + '\n')
        f.write('ran ' + str(simulations) + ' simulations ' + str(times) + ' times\n')
        for x in tqdm(range(times)):
            f.write(str(predict(fen, simulations)) + '\n')
        f.close()

    if False:
        with open('./Week-4-Results/time.csv', 'w', newline='') as file:
            writer = csv.writer(file)
     
            writer.writerow(["Number", "Wins", "Losses", "Draws", "Simulations", "White Time", "Black Time", "Fen"])

            simulations = 10000
            times = 50
            
            fen = generateConfig(10, 'time', {'time': 0.1}, {'time': 0.05})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 0.1, 0.05, fen])
            writer.writerow([""])

            fen = generateConfig(10, 'time', {'time': 0.05}, {'time': 0.1})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 0.05, 0.1, fen])
            writer.writerow([""])

            fen = generateConfig(20, 'time', {'time': 0.1}, {'time': 0.05})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 0.1, 0.05, fen])
            writer.writerow([""])
    
    if False:
        with open('./Week-4-Results/depth.csv', 'w', newline='') as file:
            writer = csv.writer(file)
     
            writer.writerow(["Number", "Wins", "Losses", "Draws", "Simulations", "White Time", "Black Time", "Fen"])

            simulations = 10000
            times = 50
            
            fen = generateConfig(10, 'depth', {'depth': 20}, {'depth': 15})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 0.1, 0.05, fen])
            writer.writerow([""])

            fen = generateConfig(10, 'depth', {'depth': 15}, {'depth': 20})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 0.05, 0.1, fen])
            writer.writerow([""])

            fen = generateConfig(20, 'depth', {'depth': 20}, {'depth': 15})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 0.1, 0.05, fen])
            writer.writerow([""])

            fen = generateConfig(20, 'depth', {'depth': 15}, {'depth': 20})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 0.05, 0.1, fen])
            writer.writerow([""])
    if True:
        with open('./Week-4-Results/depth2.csv', 'w', newline='') as file:
            writer = csv.writer(file)
     
            writer.writerow(["Number", "Wins", "Losses", "Draws", "Simulations", "White Depth", "Black Depth", "Moves From End", "Fen"])

            simulations = 50000
            times = 50

            fen = generateConfig(20, 'depth', {'depth': 20}, {'depth': 15})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 20, 15, 20, fen])
            writer.writerow([""])

            fen = generateConfig(20, 'depth', {'depth': 15}, {'depth': 20})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 20, 15, 20, fen])
            writer.writerow([""])

        with open('./Week-4-Results/time2.csv', 'w', newline='') as file:
            writer = csv.writer(file)
     
            writer.writerow(["Number", "Wins", "Losses", "Draws", "Simulations", "White Time", "Black Time", "Moves From End", "Fen"])

            simulations = 50000
            times = 50
            
            fen = generateConfig(10, 'time', {'time': 0.1}, {'time': 0.05})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 0.1, 0.05, 10, fen])
            writer.writerow([""])

            simulations = 10000

            fen = generateConfig(20, 'time', {'time': 0.05}, {'time': 0.1})
            for x in tqdm(range(times)):
                dict = predict(fen, simulations)
                writer.writerow([x + 1, dict['win'], dict['lose'], dict['draw'], simulations, 0.05, 0.1, 20, fen])
            writer.writerow([""])


if __name__ == "__main__":
    main()