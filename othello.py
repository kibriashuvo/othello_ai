import sys

EMPTY, BOUNDARY = '.', '#'

BLACK, WHITE = 'X', '0'

players = {BLACK: 'black', WHITE: 'white'}

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1

UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT = -11, -9, 9, 11

DIRECTIONS = {UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT}

CORNERS = [11,18,81,88]

NEIGHBOR_LIST = {11:[12,21,22], 18:[17,28,27], 81:[71,72,82], 88:[87,77,78]}


def squares():
    return [i for i in range(11, 89) if 1 <= i%10 <= 8]

def alphanumericSquares():
    list = []
    for a in 'ABCDEFGH':
        for b in '12345678':
            list.append(a+b)
    return list

def mapSquares():
    return dict(zip(squares(),alphanumericSquares()))


def initialBoard():

    board = [BOUNDARY]*100
    for sq in squares():
        board[sq] = EMPTY

    board[44], board[55] = WHITE, WHITE
    board[45], board[54] = BLACK, BLACK
    return board




def printBoard(board):
    i = 0;
    for sq in board:
        print(sq," ",end="")
        i+=1
        if(i==10):
            print("\n")
            i=0


SQUARE_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]




"Minimax"


def weighted_square(player,board):
    sum = 0
    opp = getOpponent(player)
    for sq in squares():
        if board[sq] == player:
            sum += SQUARE_WEIGHTS[sq]
        elif board[sq] == opp:
            sum -= SQUARE_WEIGHTS[sq]
    return sum






def modified_weighted_square(player,board):
    w = weighted_square(player,board)
    for c_sq in CORNERS:
        if board[c_sq] != EMPTY:
            for NoC in NEIGHBOR_LIST[c_sq]:
                if board[NoC] != EMPTY:
                    w = w + ((5-SQUARE_WEIGHTS[NoC])*1 if board[NoC] == player else -1)

    return w


def minimax(player,board,depth):

    def value(board):
        board_val = -minimax(getOpponent(player),board,depth-1)[0]
        return board_val

    if depth == 0:
        w_scr = weighted_square(player,board)
        return w_scr,None

    move_list,move_dup = possibleMove(player,board)

    if len(move_list) == 0:

        opp_move_list = possibleMove(getOpponent(player),board)
        if len(opp_move_list) == 0:
             final_board_value(board)

        return -minimax(getOpponent(player), board, depth - 1)[0],None

    return max((value(assignGuti(mv,list(board),player)),mv)for mv in move_list)




"Minimax end"


def alpha_beta(player,board,depth,alpha,beta):

    if depth == 0:
        return weighted_square(player,board),None

    def value(board,alpha,beta):
        return -alpha_beta(getOpponent(player),board,depth-1,-beta,-alpha)[0]

    move_list,move_dup = possibleMove(player,board)

    if len(move_list) == 0:

        opp_move_list,move_dup = possibleMove(getOpponent(player),board)

        if len(opp_move_list) == 0:
            return final_board_value(board),None

        return -alpha_beta(getOpponent(player),board,depth-1,-beta,-alpha)[0],None
        #return value(board,alpha,beta),None


    best_move = list(move_list)[0]

    for move in move_list:

        if alpha >= beta:
            break


        val = -alpha_beta(getOpponent(player),assignGuti(move,list(board),player),depth-1,-beta,-alpha)[0]
      #  val = value(assignGuti(move,list(board),player),alpha,beta)

        if val > alpha:
            alpha = val
            best_move = move



    return alpha,best_move




"""
def isValid(move):
    if move in squares():
        return True

def determineDirection(curr,dest):
    diff = dest-curr
    if(abs(diff)<=8):
        if(dest>curr):
            return RIGHT
        else:
            return LEFT
    else:
        if(diff%11==0):
            if dest>curr:
                return DOWN_RIGHT
            else:
                return UP_LEFT
        elif(diff%10==0):
            if dest>curr:
                return DOWN
            else:
                return UP
        elif(diff%9==0):
            if dest>curr:
                return DOWN_LEFT
            else:
                return UP_RIGHT


def sorround_n_conquer(square,direction,board,player):
    place = square+direction
    if(board[place]==player or board[place]==EMPTY):
        return False
    else:
        while(board[place]!=EMPTY):
            place+=direction
            if(board[place]==player):
                return False
       # board[place]=player
       # flipOpponent(square,place,direction,player,board)
        return place


def gutiBazi(start,end,player,board,direction):
    print("Guti")
    i = start+direction
    while(start!=end):
        board[start] = player
        i+=direction


"""



def calculate_score(board):
    b_score = 0
    w_score = 0
    for sq in squares():
        if board[sq] == BLACK:
            b_score += 1
        elif board[sq] == WHITE:
            w_score += 1
    return b_score,w_score

def final_board_value(board):
    b_score,w_score = calculate_score(board)
    return b_score-w_score


def assignGuti(square,board,player):
    #place = sorround_n_conquer(square,direction,board,player)

    #if place:
    board[square] = player
    for dir in DIRECTIONS:
        flipOpponent(square,player,dir,board)

    "testing"
    return board









def formedBracket(square,direction,player,board):
    place = square+direction

    if board[place] != getOpponent(player):
        return False
    else:
        while(board[place]==getOpponent(player)):
            place+=direction
            if board[place]==BOUNDARY or board[place]==EMPTY:
                return False
        return True


def flipOpponent(square,player,direction,board):

    if(formedBracket(square,direction,player,board)):
        var = square+direction
        while(board[var]!=player):
            board[var] = player
            var+=direction










def possibleMove(player,board):
    move_set = set()
    move_dict = {}
    move_duplicates = []

    for sq in squares():
        if(board[sq]==player):
            for direction in DIRECTIONS:
                place = sq+direction;
                if (board[place]==player or board[place]==EMPTY):
                    continue
                while(board[place]==getOpponent(player)):
                  place+=direction

                if(board[place]==player or board[place]==BOUNDARY):
                    continue
                else:
                    move_set.update([place])
                    move_dict.setdefault(place,sq)
                    move_duplicates.append(place)

    return move_set,move_duplicates
    #return len(move_set),move_set,move_dict,move_duplicates



"=============== Playing the game============================"



def maximizer(player,board,moves):

    score,move = max((assignGuti(mv,board.copy(),player),mv)for mv in moves)
    return score,move



def playGame():

    board = initialBoard()
    current_player = BLACK
    printBoard(board)

    while True:

        b_score, w_score = calculate_score(board)
        print("Black:", b_score, "White: ", w_score)
        #move_set = possibleMove(current_player, board)

        if current_player == BLACK:
            move_set,move_dup = possibleMove(current_player, board)
            print(players[current_player], '\'s Move')
            print("Play among these ", move_set)
            #print(move_dict)
            choice = input("Please enter your choice= ");
            if choice == '':
                print("Not a valid move!!")
                continue

            sq = int(choice)

            if(sq not in move_set):
                print("Not a valid move!!")
                continue
            else:
                assignGuti(sq, board, current_player)


        elif current_player == WHITE:
            sc,mv = alpha_beta(WHITE,board.copy(),5,-1111,1111)
            assignGuti(mv,board,current_player)
            print("White made its move on ",mv)




        current_player = next_player(current_player, board)
        printBoard(board)







def next_player(curr,board):
    opp = getOpponent(curr)
    move_set,move_dup = possibleMove(opp, board)

    if(len(move_set)==0):
        print("No possible move for ",players[opp])
        return curr
    else:
        return opp



def getOpponent(player):
    return BLACK if player==WHITE else WHITE

"""

printBoard(board)


placeGuti(45,LEFT,board,BLACK)


board[44] = BLACK

placeGuti(55,UP_LEFT,board,WHITE)

board[44] = WHITE

printBoard(board)

placeGuti(45,RIGHT,board,BLACK)

printBoard(board)

placeGuti(43,UP,board,BLACK)

board[33] = BLACK

printBoard(board)

placeGuti(44,DOWN,board,WHITE)

board[54] = WHITE
printBoard(board)

placeGuti(45,DOWN_LEFT,board,BLACK)



board[54]=BLACK

printBoard(board)

placeGuti(64,LEFT,board,WHITE)
board[63]=WHITE
printBoard(board)

placeGuti(33,DOWN_RIGHT,board,BLACK)
board[44]=BLACK
board[55]=BLACK

printBoard(board)

placeGuti(63,UP_RIGHT,board,WHITE)


printBoard(board)

placeGuti(55,DOWN_LEFT,board,BLACK)

printBoard(board)

placeGuti(63,DOWN,board,WHITE)
printBoard(board)

count , moves,move_dict = possibleMove(BLACK,board)


print(count)

print(moves)

print(move_dict)

print((41-74)%10)

print(determineDirection(54,76))



lis = [1,2,3,4,5]

def test(list,i):
    list.append(i)

n , s = max((test(lis,i),i) for i in range(15,20))


print(lis)



"""

#playGame()



"=============================="




def boardtoSting(board):
	st = ""
	for i in board:
		st +=i
	return st

def writeboard(board):
    f = open('E:\\Othello\\othello_board.txt', 'w')
    for sq in board:
         f.write(sq)

def logger(msg):
    f = open('E:\\Othello\\log_file.txt', 'w')
    f.write(msg)	   

	   
def stringtoBoard(dummy_board):
    board = []
    for sq in dummy_board:
        board.append(sq)
    return board


def gameover():
    f = open('E:\\Othello\\game_over.txt', 'w')
    f.write('1')


def othelloGUI(move, board):

    b_moved = assignGuti(move, board, BLACK)

    n, mv = alpha_beta(WHITE, b_moved.copy(), 5, -1111, 1111)

    if mv:
        w_moved = assignGuti(mv, b_moved, WHITE)
    else:
        logger("WHITE HAS NO VALID MOVES!!!")

    pass_java = possibleMove(BLACK, b_moved)

    if len(pass_java == 0):
        logger("BLACK HAS NO VALID MOVES")
        writemoves("null")
        if not mv:
            gameover()

    
    writemoves(pass_java)
    writeboard(board)

	
def movetostring(mv_set):
	st = ""
	for i in mv_set:
		st += str(i)+"\n"	
	
	f = open('E:\\Othello\\valid_moves.txt', 'w')
	f.write(st)



	
	
initialboard = stringtoBoard(sys.argv[1])
g_moves = int(sys.argv[2])


ff = assignGuti(g_moves,initialboard,BLACK)




n,mv = alpha_beta(WHITE, ff.copy(), 5, -1111, 1111)







if mv != None:
	gg = assignGuti(mv,ff,WHITE)
	writeboard(gg)
	logger("OK")
else:
	logger("NO Moves WHITE")

mv_set,mv_list = possibleMove(BLACK,gg)



movetostring(mv_set)




"""

def piperead():
	i = 1
	data = ""
	while(i=1):
		data += sys.stdin.readline().strip()	
		i-=1
	return data

srr = piperead()
	
writeboard(initialBoard())

str = boardtoSting(initialBoard())+srr

sys.stdout.write(srr + '\n')
sys.stdout.flush()


"""
"""

	
	

"GUI Java"
initialboard = stringtoBoard(sys.argv[1])
g_moves = int(sys.argv[2])


ff = assignGuti(g_moves,initialboard,BLACK)


n,mv = alpha_beta(WHITE, ff.copy(), 5, -1111, 1111)

gg = assignGuti(mv,ff,WHITE)


writeboard(initialBoard())


if mv != None:
	writeboard(gg)
	logger("OK")
else:
	logger("NO Moves WHITE")

mv_set,mv_list = possibleMove(BLACK,gg)

writemoves(mv_list)

"""



"""
bb= initialBoard()


bb[65],bb[66]=BLACK,WHITE


printBoard(bb)


def maximizer(player,board,moves):


    min = 999999999
    for mv in moves:
        bd,ps = assignGuti(mv,board.copy(),player)
        print(mv,ps)

        if final_board_value(board)<min:
            move,min = mv,final_board_value(board)
            print(move,min)
            printBoard(bd)


    score,move = max((assignGuti(mv,board.copy(),player),mv)for mv in moves)
    return score,move






sc,mv = maximizer(BLACK,bb,[34,43,56,67])

print(sc,mv)



MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))

bb = initialBoard()
bb[34],bb[44] = BLACK,BLACK


printBoard(bb)
print(minimax(WHITE,bb.copy(),3))

print(-MAX_VALUE)





"""



"""
Modified werighted Square

(defvar w 6)
(setf my-array (make-array '(10)))
(setf (aref my-array 0) 25)
(setf (aref my-array 1) 99)

(incf w (* (- 5 (aref my-array 0)) (if (eql (aref my-array 1) 99) +1 -1)))

(write w)

if corners are not empty find their neigbours and calculate this--

bottom-line = WEIGHT of board + (WEIGHT[c]- [5*( 1 if  c == player else -1)]




bb = initialBoard()

for i in range(31,37):
    bb[i] = BLACK
for i in range(51,57):
    bb[i] = BLACK

bb[62] = BLACK

bb[42], bb[44], bb[45] = BLACK,BLACK,BLACK

bb[22], bb[26], bb[27],bb[12] = BLACK,BLACK,BLACK,BLACK

bb[11] = WHITE

assignGuti(13,bb,WHITE)
printBoard(bb)

print(weighted_square(WHITE,bb))




"""

#sunshine