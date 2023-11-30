import chess
import random
import chess.svg

board = chess.Board()

valores = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}

def random_move(board):
  legal_moves = []
  for i in board.legal_moves:
    legal_moves.append(i)
  board.push(random.choice(legal_moves))

def funcao_melhorMovimento(board):
  best_moves = []
  max = -999
  for i in board.legal_moves:
    board.push(i)
    move_value = min(board,2) + valor_board(board)
    if (move_value == max):
      best_moves.append(i)
    elif (move_value > max):
      best_moves.clear()
      best_moves.append(i)
      max = move_value
    board.pop()
  board.push(random.choice(best_moves))

def min(board, profundidade):
  pior = 999
  for i in board.legal_moves:
    board.push(i)
    if (profundidade != 0):
      move_value = valor_board(board) + max(board, profundidade - 1)
    else:
      board.pop()
      return 0
    if (move_value < pior):
      pior = move_value
    board.pop()
  return pior


def max(board, profundidade):
  max = -999
  for i in board.legal_moves:
    board.push(i)
    if (profundidade != 0):
      move_value = valor_board(board) + min(board, profundidade - 1)
    else:
      board.pop()
      return 0
    if (move_value > max):
      max = move_value
    board.pop()
  return max


def valor_board(board):
  count = 0;
  pm = board.piece_map()
  for i in pm:
    val = valores[pm[i].piece_type]
    if pm[i].color == chess.WHITE:
      count-=val
    if pm[i].color == chess.BLACK:
      count+=val
  return count;

# Loop principal
while (board.is_game_over() == False):
  while True:
    try:
      move = input("Jogada: ")
      board.push_san(move)
      display(board)
    except:
      print("erro")

    if move == 'ia':
      funcao_melhorMovimento(board)
      display(board)