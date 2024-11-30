def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != " ":
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    n = len(board)
    y_start = y_end - (length -1) * d_y
    x_start = x_end - (length -1) * d_x
    
    y_before = y_start - d_y
    x_before = x_start - d_x
    y_after = y_end + d_y
    x_after = x_end + d_x
    
    if 0 <= y_before < n and 0 <= x_before < n:
        before_valid = True 
    else:
        before_valid = False
    
    if 0 <= y_after < n and 0 <= x_after < n:
        after_valid = True
    else:
        after_valid = False
    
    if before_valid and board[y_before][x_before] == " ":
        before_empty = True 
    else:
        before_empty = False

    
    if after_valid and board[y_after][x_after] == " ":
        after_empty = True
    else:
        after_empty = False
    
    if not before_valid and not after_valid:
        return "CLOSED"
    elif before_empty and after_empty:
        return "OPEN"
    elif before_empty or after_empty:
        return "SEMIOPEN"
    else:
        return "CLOSED"
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    
    open = 0
    semi = 0
    n = len(board)
    
    y = y_start
    x = x_start
    
    while 0 <= y < n and 0 <= x < n:
        end_y = y + (length -1) * d_y
        end_x = x + (length -1) * d_x
        
        if not (0 <= end_y < n and 0 <= end_x < n):
            break

        valid = True 
        
        if 0 <= y - d_y < n and 0 <= x - d_x < n:
            if board[y -d_y][x -d_x] == col:
                valid = False
        
        if 0 <= end_y + d_y < n and 0 <= end_x + d_x < n:
            if board[end_y +d_y][end_x +d_x] == col:
                valid = False
        
        if valid:
            for i in range(length):
                if board[y + i*d_y][x + i*d_x] != col:
                    valid = False
                    break
            if valid:
                t = is_bounded(board, end_y, end_x, length, d_y, d_x)
                if t == "OPEN":
                    open += 1
                elif t == "SEMIOPEN":
                    semi += 1
        y += d_y
        x += d_x
    
    return open, semi

def detect_rows(board, col, length):
    semi, open = 0, 0
    for i in range(len(board)):
        a, b = detect_row(board, col, i, 0, length, 0, 1)
        open += a
        semi += b
        a, b = detect_row(board, col, 0, i, length, 1, 0) 
        open += a
        semi += b

    for i in range(len(board) - length + 1):
        a, b = detect_row(board, col, i, 0, length, 1, 1)  
        open += a
        semi += b

    for i in range(len(board) - length):
        a, b = detect_row(board, col, 0, i+1, length, 1, 1)  
        open += a
        semi += b

    for i in range(len(board) - length + 1):
        a, b = detect_row(board, col, i, len(board) - 1, length, 1, -1)
        open += a
        semi += b

    for i in range(len(board) - length):
        a, b = detect_row(board, col, 0, len(board) - 1-i, length, 1, -1)
        open += a
        semi += b
    return open, semi

def search_max(board):
    max = -100000
    y, x = 0, 0 
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == " ":
                board[i][j] = 'b'  
                scre = score(board)  
                if scre > max:
                    y = i
                    x = j
                    max = scre  
                board[i][j] = ' ' 

    return y, x

def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
    if " " not in [i for row in board for i in row]:
        return "Draw"

    for i in range(len(board)):
        for j in range(len(board)-4):
            if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == board[i][j+4] != ' ':
                return "Black won" if board[i][j] == 'b' else "White won"
            if board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i] == board[j+4][i] != ' ':
                return "Black won" if board[j][i] == 'b' else "White won"
    
    for i in range(len(board)-4):
        for j in range(len(board)-4):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4] != ' ':
                return "Black won" if board[i][j] == 'b' else "White won" 
            if board[i][j+4] == board[i+1][j+3] == board[i+2][j+2] == board[i+3][j+1] == board[i+4][j] != ' ':
                return "Black won" if board[i][j+4] == 'b' else "White won"

    return "Continue Playing"


def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board          


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res       
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

def test_edge_cases():
    # Test 1: Corner sequences
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 1, 1, 5, "b")  # Diagonal from top-left
    assert is_bounded(board, 4, 4, 5, 1, 1) == "SEMIOPEN"
    
    # Test 2: Edge sequences
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 0, 1, 5, "w")  # Horizontal at top
    assert is_bounded(board, 0, 4, 5, 0, 1) == "SEMIOPEN"
    
    # Test 3: Near-edge sequences
    board = make_empty_board(8)
    put_seq_on_board(board, 1, 1, 1, 0, 5, "b")  # Vertical near left
    open, semi = detect_row(board, "b", 1, 1, 5, 1, 0)
    print(f"Test 3 results - open: {open}, semi: {semi}")
    assert open == 1 and semi == 0
    
    # Test 4: Overlapping sequences
    board = make_empty_board(8)
    put_seq_on_board(board, 3, 3, 0, 1, 5, "w")
    put_seq_on_board(board, 3, 5, 1, 0, 5, "w")
    result = is_win(board)
    assert result == "White won"
    
    print("All edge case tests passed!")

# Run the tests
if __name__ == "__main__":
    test_edge_cases()