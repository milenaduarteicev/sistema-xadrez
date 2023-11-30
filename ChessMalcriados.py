# Milena Duarte
# Max Ramon
# Marcos Vinnicius

import chess
import random
import chess.polyglot
from google.colab import drive

drive.mount("/content/drive")

board = chess.Board()
board

def obterMelhorJogada(board=board):
  jogadas = melhoresJogadas(board)
  melhorJogada = None
  if len(jogadas)>0:
    melhorJogada = jogadas[0].move
  if not melhorJogada:
    print("Não achou jogada")
    melhorJogada = random.sample(list(board.legal_moves), 1)[0]
  return melhorJogada


def melhoresJogadas(board=board):
  jogadas = []
  with chess.polyglot.open_reader("/content/drive/MyDrive/Xadrez/bookfish.bin") as reader:
    for entry in reader.find_all(board):
      jogadas.append(entry)
  return jogadas


print("Melhor jogada agora: ", obterMelhorJogada())

def evaluation(board):
    i = 0
    evaluation = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        evaluation = evaluation + (getPieceValue(str(board.piece_at(i))) if x else -getPieceValue(str(board.piece_at(i))))
    return evaluation


def getPieceValue(piece):
    if(piece == None):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == 'K' or piece == 'k':
        value = 900
    return value

def minimax(profundidade, board, maximizando):
  if(profundidade == 0):
      return -evaluation(board)
  possibleMoves = melhoresJogadas(board)
  if(maximizando):
      bestMove = -9999
      for x in possibleMoves:
          move = chess.Move.from_uci(str(x.move))
          board.push(move)
          bestMove = max(bestMove,minimax(profundidade - 1, board, not maximizando))
          board.pop()
      return bestMove
  else:
      bestMove = 9999
      for x in possibleMoves:
          move = chess.Move.from_uci(str(x.move))
          board.push(move)
          bestMove = min(bestMove, minimax(profundidade - 1, board, not maximizando))
          board.pop()
      return bestMove

def minimaxRoot(board, depth, isMaximizing):
    possibleMoves = melhoresJogadas(board)
    bestMove = -9999
    secondBest = -9999
    thirdBest = -9999
    bestMoveFinal = None
    print("Quantidade de jogadas Root:", len(possibleMoves))
    for x in possibleMoves:
      move = chess.Move.from_uci(str(x.move))
      board.push(move)
      value = max(bestMove, minimax(depth - 1, board, not isMaximizing))
      board.pop()
      if( value > bestMove):
          print("Best score: " ,str(bestMove))
          print("Best move: ",str(bestMoveFinal))
          print("Second best: ", str(secondBest))
          thirdBest = secondBest
          secondBest = bestMove
          bestMove = value
          bestMoveFinal = move
    return bestMoveFinal



def receberJogada(board=board):
  while True:
      try:
        jogada_oponente = input("Digite a jogada do oponente: ")
        jogada = chess.Move.from_uci(jogada_oponente)
        if jogada in board.legal_moves:
          return jogada
        else:
          print("Jogada inválida! Tente novamente.")
      except ValueError:
        print("Entrada inválida! Tente novamente.")

def escolherLado():
    while True:
        lado = input("Você quer ser as brancas ou as pretas? (b/p): ")
        if lado.lower() == 'b':
            return True
        elif lado.lower() == 'p':
            return False
        else:
            print("Escolha inválida! Tente novamente.")

i = -1
print("########### PARTIDA COMEÇOU ###########")
# Loop principal do jogo
quem_comeca = input("Quem começa jogando? (o/ia): ").lower()
jogador_branco = quem_comeca == 'o'
print()

while True:
    print()
    if (jogador_branco and board.turn) or (not jogador_branco and not board.turn):
        print("Vez do oponente")
        jogada = receberJogada(board)
        board.push(jogada)
        print(board)
    else:
        print("Sua vez de jogar")
        jogada_ia = obterMelhorJogada(board)
        board.push(jogada_ia)
        print("Jogada da IA:", jogada_ia)
        print(board)

    continuar = input("Continuar jogo? (s/n): ")
    if (board.is_game_over()) or (continuar == 'n'):
        print("O jogo acabou!")
        break
    else:
      continue

    