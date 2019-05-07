import random, time
from bigml.api import BigML

# everything between this and the next comment is part of my implementation of greed

POSSIBLE_MOVES = [[x, y] for x in [-1, 0, 1] for y in [-1, 0, 1]]

def gen_board(size):
    board = [[random.randint(1, min(9, size - 1)) for x in range(size)] for y in range(size)]
    cursor = [random.randint(0, size - 1), random.randint(0, size - 1)]
    return board, cursor

def display(board, cursor):
    size = len(board)
    tmp_board = [[board[x][y] for y in range(size)] for x in range(size)]
    tmp_board[cursor[0]][cursor[1]] = 'X'
    for row in tmp_board:
        for element in row:
            print(element, end=' ')
        print('')

def serialize(tree):
    inputs = [[element for row in t[1] for element in row] + t[2] for t in tree][1:]
    outputs = [t[3] for t in tree][:-1]
    serialized_arr = [in_e + [out_e] for in_e, out_e in zip(inputs, outputs)]

    serialized_strs = [] 
    for row in serialized_arr[::-1]:
        serialized_strs.append(','.join(map(str, row)))
    return serialized_strs

def get_space_value(board, cursor):
    size = len(board)
    if cursor[0] >= 0 and cursor[1] >= 0 and cursor[0] < size and cursor[1] < size:
        return board[cursor[0]][cursor[1]]
    return 0

def move(board, cursor, move):
    size = len(board)
    coords_to_fill = []
    length = get_space_value(board, [cursor[0] + move[0], cursor[1] + move[1]])
    tmp_board = [[get_space_value(board, [x, y]) for y in range(size)] for x in range(size)]

    for i in range(1, length + 1):
        new_coord = [cursor[0] + i*move[0], cursor[1] + i*move[1]]
        coords_to_fill.append([cursor[0] + i*move[0], cursor[1] + i*move[1]])

    for coord in coords_to_fill:
        if get_space_value(board, [coord[0], coord[1]]) == 0:
            return False
        tmp_board[coord[0]][coord[1]] = 0

    if len(coords_to_fill) > 0:
        tmp_cursor = coords_to_fill[-1]
        tmp_board[cursor[0]][cursor[1]] = 0
    else:
        return False

    return tmp_board, tmp_cursor

def score(board):
    return [element for row in board for element in row].count(0) / len(board) ** 2

def minimax(board, cursor, prev_move=None, depth=0, tree=[]):
    children = [[move(board, cursor, p_move), POSSIBLE_MOVES.index(p_move)] for p_move in POSSIBLE_MOVES] 
    legal_children = [child for child in children if child[0] != False]

    if len(legal_children) == 0:
        tree.append([depth, board, cursor, prev_move, score(board)])
        return board, cursor, prev_move, tree

    best_board = board 
    best_score = 0
    best_cursor = cursor 
    best_move = [0, 0] 
    best_tree = None

    for child in legal_children:
        child_board, child_cursor, child_move, child_tree = minimax(child[0][0], child[0][1], child[1], depth + 1, tree)
        
        if score(child_board) > best_score:
            best_board = child_board
            best_cursor = child_cursor
            best_move = child_move
            best_score = score(child_board)
            best_tree = child_tree

    best_tree.append([depth, board, cursor, prev_move, score(board)])

    return best_board, best_cursor, best_move, best_tree

def minimax_wrap(b0, c0):
    b1, c1, m1, t1 = minimax(b0, c0, prev_move=None, depth=0, tree=[])
    t1 = t1[::-1]
    max_value = None
    max_index = 0
    for i in range(len(t1)):
        if not max_value or t1[i][4] > max_value[4]:
            max_value = t1[i]
            max_index = i
    best_tree = [t1[max_index]]

    i = max_value[0]
    j = max_index
    while i > 0:
        i -= 1
        k = j
        while t1[k][0] != i:
            k -= 1
        best_tree.append(t1[k])

    return best_tree

BOARD_SIZE = 4

# end implementation

'''
# Comment out the quotes and edit BEST_MODEL to have the bot play a random board
api = BigML()
b0, c0 = gen_board(BOARD_SIZE)

b1, c1, m1, t1 = minimax(b0, c0, prev_move=None, depth=0, tree=[])
print(POSSIBLE_MOVES[m1]) # best move

state = {'field%d' % (i+1): random.randint(1, BOARD_SIZE - 1) for i in range(16)}
state['field17'] = random.randint(0, BOARD_SIZE - 1)
state['field18'] = random.randint(0, BOARD_SIZE - 1)

BEST_MODEL = 'deepnet/5cd09525de2d4d73f1000103'

prediction = api.create_prediction(BEST_MODEL, state)
predicted_move = POSSIBLE_MOVES[int(round(prediction['object']['output']))]
print(predicted_move) # predicted move
'''

#'''
# Comment out the quotes and edit NUM_ITER to generate data
F_NAME = 'greed_training.csv'
NUM_ITER = 5000
f = open(F_NAME, 'w')

for i in range(NUM_ITER):
    b, c = gen_board(BOARD_SIZE)
    t = minimax_wrap(b, c)
    s = serialize(t)[0] # only using first board to reduce number of possible cases
    f.write(s+'\n')

f.close()
#'''
