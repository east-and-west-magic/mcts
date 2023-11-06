import chess
import chess.svg
import chess.engine
import random
from tqdm import tqdm

def predict(boardFen, times):
    result = {'win': 0, 'lose': 0, 'draw': 0}
    # outcome = {
    #     'checkmate': 0, 
    #     'stalemate': 0, 
    #     'insufficient': 0, 
    #     'seventy_five': 0,
    #     'five_reps': 0,
    #     'fifty': 0,
    #     'three_reps': 0
    # }

    for x in tqdm(range(times)):
        board = chess.Board(boardFen)
        while not board.is_game_over():
            moves = list(board.legal_moves)
            r = random.randint(0, len(moves) - 1)
            moveChosen = moves[r]
            board.push(moveChosen)
            # print(board)
        res = board.result()
        # out = board.outcome().termination.value 
        if res == '1-0':
            result['win']+=1
        elif res == '0-1':
            result['lose']+=1
        else:
            result['draw']+=1
        
    #     if out == 1:
    #         outcome['checkmate']+=1
    #     elif out == 2:
    #         outcome['stalemate']+=1
    #     elif out == 3:
    #         outcome['insufficient']+=1
    #     elif out == 4:
    #         outcome['seventy_five']+=1
    #     elif out == 5:
    #         outcome['five_reps']+=1
    #     elif out == 6:
    #         outcome['fifty']+=1
    #     elif out == 7:
    #         outcome['three_reps']+=1
    # print(outcome)
    return result

def generateConfig(moves, whiteStrength, blackStrength):
    engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\amyta\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe")
    board = chess.Board()
    for x in range(moves):
        if board.is_game_over():
            break
        res = engine.play(board, chess.engine.Limit(time=whiteStrength['time'], depth=whiteStrength['depth'], nodes=whiteStrength['nodes']))
        board.push(res.move)
        # print(board)

        res = engine.play(board, chess.engine.Limit(time=blackStrength['time'], depth=blackStrength['depth'], nodes=blackStrength['nodes']))
        board.push(res.move)
        # print(board)

    engine.quit()
    return board.fen()

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
    fen = '3q3r/6p1/6k1/5p2/PP6/3r4/2Q2RP1/2R3K1 w - - 5 36'
    f.write('board configuration with fen representation: ' + fen + '\n')
    f.write('ran ' + str(simulations) + ' simulations ' + str(times) + ' times\n')
    for x in tqdm(range(times)):
        f.write(str(predict(fen, simulations)) + '\n')
    f.close()

if __name__ == "__main__":
    main()