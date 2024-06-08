from random import randint

brain = {
  "111200022": [[(0,1),0],[(0,1),1],[(0,2),2]],
  "111020202": [[(0,0),0],[(0,0),1]],
  "011122200": [[(0,1),2],[(0,2),1]],
  "011012200": [[(0,1),2],[(1,1),0],[(1,1),1]],
  "110202002": [[(0,1),0],[(0,1),1],[(0,1),2]],
  "101200002": [[(0,2),2]],
  "101220020": [[(0,0),1],[(0,2),1],[(0,2),2]],
  "011210002": [[(0,1),0],[(0,2),2],[(1,1),1],[(1,1),2]],
  "011020002": [[(0,2),1],[(0,2),2]],
  "101120002": [[(0,0),1],[(0,2),1],[(1,0),0]],
  "101102020": [[(1,0),0],[(1,0),1]],
  "011020200": [[(0,2),1],[(0,2),2]],
  "010122000": [[(0,1),2],[(1,0),0]],
  "100120000": [[(0,0),1],[(1,0),0]],
  "100112000": [[(1,0),0],[(1,1),2]],
  "100222000": [[(0,0),1]],
  "010210000": [[(0,1),0],[(1,1),1]],
  "001120000": [[(0,2),1],[(0,2),2],[(1,0),0]],
  "001112000": [[(1,0),0],[(1,1),1]],
}

def get_moves(space, player):
  r, c = space
  moves = []

  row = r - 1 if player == 2 else r + 1

  if c > 0 and board[row][c - 1] == (1 if player == 2 else 2):
    moves.append((row, c - 1))

  if board[row][c] == 0:
    moves.append((row, c))

  if c < 2 and board[row][c + 1] == (1 if player == 2 else 2):
    moves.append((row, c + 1))

  return moves

def is_over(player):
  if 2 in board[0] or 1 in board[2]:
    return True
  
  for r, row in enumerate(board):
    for c, space in enumerate(row):
      if space == player and len(get_moves((r,c), player)) > 0:
        return False

  return True

def player_move():
  player_count = 0
  piece_num = 0
  piece = (-1, -1)
  pieces = [(-1, -1) for i in range(3)]

  while piece_num <= 0 or piece_num > player_count:
    player_count = 0

    print()

    for r, row in enumerate(board):
      for c, space in enumerate(row):
        if space == 1:
          print("\033[42m", end="")
        elif space == 2:
          
          print("\033[41m", end="")
        else:
          print("\033[40m", end="")

        if space == 2 and len(get_moves((r, c), 2)) > 0:
          pieces[player_count] = (r, c)
          player_count += 1
          print(f" {player_count} ", end="")
        else:
          print("   ", end="")

        print("\033[0m", end="")
      print()

    try:
      piece_num = int(input("\nWhich piece would you like to move? "))
    except:
      continue

  piece = pieces[piece_num - 1]

  move_num = 0
  move_count = 0
  move = (-1, -1)
  moves = [(-1, -1) for i in range(3)]

  while move_num <= 0 or move_num > move_count:
    move_count = 0

    print()

    for r, row in enumerate(board):
      for c, space in enumerate(row):
        if (r, c) == piece:
          print("\033[44m", end="")
        elif space == 1:
          print("\033[42m", end="")
        elif space == 2:
          print("\033[41m", end="")
        else:
          print("\033[40m", end="")

        if r == piece[0] - 1 and (c == piece[1] and space == 0 or abs(piece[1] - c) == 1 and space == 1):
            moves[move_count] = (r, c)
            move_count += 1
            print(f" {move_count} ", end="")
        else:
          print("   ", end="")

        print("\033[0m", end="")
      print()

    try:
      move_num = int(input("\nWhere would you like to move? "))
    except:
      continue

  move = moves[move_num - 1]

  board[move[0]][move[1]] = 2
  board[piece[0]][piece[1]] = 0

def display():
  print()

  for r, row in enumerate(board):
    for c, space in enumerate(row):
      if space == 1:
        print("\033[42m", end="")
      elif space == 2:
        
        print("\033[41m", end="")
      else:
        print("\033[40m", end="")

      print("   \033[0m", end="")
    print()

def show_brain():
  for id, moves in brain.items():
    print(f"{id}: {moves}")

player_wins = 0
computer_wins = 0

while True:
  mode = ""

  while mode not in ["p", "q", "b"]:
    mode = input("press p to play, q to quit, or b to view the brain: ")
  
  if mode == "q":
    break
  if mode == "b":
    show_brain()
    continue

  board = [
    [1 for i in range(3)],
    [0 for i in range(3)],
    [2 for i in range(3)]
  ]

  turn = 0
  computer_moves = []
  while not is_over((turn + 1) % 2 + 1):

    if turn % 2 == 0:
      player_move()

      display()

    else:
      board_id = ""
      is_reversed = False

      for row in board:
        for space in row:
          board_id += str(space)

      if not board_id in brain.keys():
        is_reversed = True
        board_id = ""
        for row in board:
          for space in reversed(row):
            board_id += str(space)

      computer_moves.append([board_id, brain[board_id].pop(randint(0, len(brain[board_id]) - 1))])

      [move_from, move_to] = computer_moves[-1][1]

      if is_reversed:
        board[move_from[0]][2 - move_from[1]] = 0
        board[move_from[0] + 1][2 - move_to] = 1
      else:
        board[move_from[0]][move_from[1]] = 0
        board[move_from[0] + 1][move_to] = 1

    turn += 1
    
  display()

  if turn % 2 == 0:
    computer_wins += 1
    print("Computer Wins!!!")

    for move in computer_moves:
      brain[move[0]].append(move[1])
      brain[move[0]].append(move[1])
  else:
    player_wins += 1
    print("You Win!!!")

  print()
  print("Computer | You")
  print(f"    {computer_wins}    |  {player_wins}")
