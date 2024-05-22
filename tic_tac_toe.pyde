import random

def setup():
    global game_state, board, square_width, square_height, turn, score, load_time, next_game, max_score, finished_input

    score = [0, 0] #x wins, o wins
    
    board = [
             [ 0, 0, 0 ],
             [ 0, 0, 0 ],
             [ 0, 0, 0 ]
             ] # board is a 2D array 
    
    game_state = 0 # 0 means start screen, 1 means game running, 2 means game over, 3 means the user is inputting the score that the game will go to, 4 means the current game is over
    
    size(900, 900)
    
    square_height, square_width = 300, 300
    
    turn = 1 # 1 means the players turn (X) , -1 means the other's turn (O)
    
    next_game = True
    load_time = 0
    max_score = 1
    finished_input = False

def draw():
    global game_state, board, turn, clickable_squares, current_game_state, score, next_game, load_time, max_score, finished_input

    winner = None # Sets the current winner of the current game to None, not the overall winner

    if game_state == 0 and next_game == True: #Checks if game state is on start screen 
        start_screen()
        
    if game_state == 1: #Checks if game state is on game running
        next_game = False
        current_game_state = game_running()

        if not current_game_state[0] == 'game running': # Check if game is not running (game is over) and set the game state to game over
            game_state = 4
            load_time = millis()
            
    if game_state == 4: #Checks if the game is over and displays the winner on the screen is there is not
        
        winner = end_screen(current_game_state)

        board = [
            [ 0, 0, 0 ],
            [ 0, 0, 0 ],
            [ 0, 0, 0 ]
            ] #Updates the board so that is empty for the next game

        if millis() - load_time > 1000: # This adds a 1000ms delay between the game displaying the winner and resetting the board
            
            fill(255)
            rect(0,0,900,900)
 
            if not winner == None: # This checks who the winner is an increments the score accordingly
                if winner == "x won":
                    score[0] = score[0] + 1
                if winner == "o won":
                    score[1] = score[1] + 1
                if winner == "tie":
                    score = score
                game_state = 1
    
    

    if game_state == 3: #Checks if the game state is on the user inputting menu and displays the max score menu
        
        fill(255)
        rectMode(CORNER)
        rect(0, 0, 900, 900)
        fill(0)
        textSize(25)
        text("What score will the game go to?", 100, 100)
        text("Use UP arrow to increment, DOWN arrow to decrement", 100, 200)
        text("Press C to continue", 100, 300)
        textSize(45)
        text(max_score, 500, 500)
        if finished_input == True: # Takes finished_input from the keyPressed function and checks if it True to go to the next menu
            game_state = 1
        
    if not (game_state == 0 or game_state == 3 or game_state == 4): #Checks if the game state is not on the starting menu, game over menu or the input score menu and displays the score if it is not
        score_display(score)
        
    if score[0] >= max_score or score[1] >= max_score: # Checks if the score has reached the max score set by the user and switches the game state to game over if True
        game_state = 2
    
    if game_state == 2: #This checkes if the user is on the end game screen and draws the congradulatory stick figure animation
        
        #Randomizes the position of the arms of the stick figure
        arm_x1, arm_y1 = 268 + random.randint(0, 100), 579 + random.randint(0, 100)
        arm_x2, arm_y2 = 647 + random.randint(0, 100), 547 + random.randint(0, 100)
        
        leg_x1, leg_y1 = 352 + random.randint(0, 100), 797 + random.randint(0, 100)
        leg_x2, leg_y2 = 565 + random.randint(0, 100), 794 + random.randint(0, 100)
        
        #This draws the body of the stickman
        fill(255)
        rect(0, 0, 900, 900)
        fill(0)
        line(452, 461, 466, 688)
        
        # This draws the legs
        line(466, 688, leg_x1, leg_y1)
        line(466, 688, leg_x2, leg_y2)
        
        fill(255)
        ellipse(343, 311, 200, 200)
        
        #This draws the arms
        line(460, 586, arm_x1, arm_y1)
        line(460, 586, arm_x2, arm_y2)
        
        #Draws the eyes of the mouth 
        ellipse(390, 375, 30, 30)
        ellipse(487, 373, 30, 30)
        line(384, 448, 439, 473)
        line(439, 473, 501, 433)
        
        winner_displayer(score)
        
    pass
    
def game_running():
    #Draws the outline of the 3x3 grid for the board
    fill(255)
    rectMode(CORNER)
    for j in range(3):
        for i in range(3):
            rect(square_width * i, square_height * j, square_width, square_height)

    #Draws the x's and o's for when the game is played
    ellipseMode(CORNER)
    for j in range(3):
        for i in range(3):
            if board[i][j] == -1: # Draw O
                ellipse(clickable_squares[i][j][0] + 50, clickable_squares[i][j][1] + 50, 200, 200) 
            elif board[i][j] == 1: # Draw X
                line(clickable_squares[i][j][0], clickable_squares[i][j][1], clickable_squares[i][j][0] + 300, clickable_squares[i][j][1] + 300)
                line(clickable_squares[i][j][0] + 300, clickable_squares[i][j][1], clickable_squares[i][j][0], clickable_squares[i][j][1] + 300)

    #Updates the current state of the game to be lost, won or tied or currently ongoing.
    current_state = game_board_evaluator(board)  
      
    return(current_state)

def start_screen():
    
    #Creates the play button rectangle
    fill(255)
    rectMode(CENTER)
    rect(450, 450, 200, 50)
    
    #Creates play button text
    textSize(40)
    textAlign(CENTER)
    fill(0)
    text("Play", 450, 465)
    
    #Creates the instructions text
    textSize(12)
    textAlign(TOP)
    text("Instructions : The game is played on a grid that's 3 squares by 3 squares. ", 215, 540)
    text("You are X, your friend (or the computer in this case) is O. ", 215, 580)
    text(" The first player to get 3 of her marks in a row (up, down, across, or diagonally) is the winner. ", 215, 620)
    text(" When all 9 squares are full, the game is over.", 215, 660)
    
def mousePressed():
    global game_state, board, square_height, square_width, loading_time, turn, clickable_squares, next_game
    #This is the clickable areas for the start_screen, the clickable play button
    clickable_areas = {"start" : [[352, 427], [551, 477]]}
    
    #Checks when mouse is pressed, if x and y are within the bounds of the start button
    if mouseX in range(clickable_areas["start"][0][0], clickable_areas["start"][1][0]):
        if mouseY in range(clickable_areas["start"][0][1], clickable_areas["start"][1][1]):
            #Checks if user is on the start menu
            if game_state == 0:
                loading_time = millis()
                game_state = 3
    
    #2D Array of the top left coordinate of the clickable squares, each square is 300x300
    clickable_squares = [[(0, 0), (300, 0), (600, 0)],
                         [(0, 300), (300, 300), (600, 300)],
                         [(0, 600), (300, 600), (600, 600)]]
    
    #Checks if the game state is on the playing board and if a bit of time has elapsed since the play button was pressed and finds which square the mouse was pressed in
    if game_state == 1 and loading_time - millis() < 0:
        for j in range(len(clickable_squares)):
            for i in range(len(clickable_squares[j])):
                if mouseX in range(clickable_squares[j][i][0], clickable_squares[j][i][0] + square_width):
                    if mouseY in range(clickable_squares[j][i][1], clickable_squares[j][i][1] + square_height):
                        current = game_board_updater( (i,j), board, turn )
                        
                        if current == None:
                            return
                        
                        turn = current[0]
                        board = current[1]                        
                        
                        #i, j is the form x, y in a 3x3 grid 
                        # 0,0 1,0 2,0
                        # 0,1 1,1 2,1
                        # 0,2 1,2 2,2       
                             
    if game_state == 4:
        next_game = True

def game_board_updater(coords, board, turn):
    #This function takes in the coordinates of the square pressed and updates the board with the appropriate symbol
    x = coords[0]
    y = coords[1]
    #Updates the 2D array of the current board with the square pressed and the turn that the user is on
    if board[y][x] == 0:
        if turn == -1:
            board[y][x] = turn
            return (1, board)
        if turn == 1:
            board[y][x] = turn
            return (-1, board)

def game_board_evaluator(board):
    #This function takes in the board and checks all diagonals, rows and columns for if there is winner and returns the state of the board (if there is a winner or not)
    state = rows_checker(board)
    
    if state == "no winner":
        state = columns_checker(board)
    if state == "no winner":
        state = diagonals_checker(board)
    if state == "no winner":
        state = tie_checker(board)
                
    return state

def rows_checker(board):
    #Check all rows for matching (lefts to right)
    
    for sign in (-1, 1):
        if board[0][0] == sign and board[0][1] == sign and board[0][2] == sign:
            return ("first row", sign)
        if board[1][0] == sign and board[1][1] == sign and board[1][2] == sign:
            return ("second row", sign)
        if board[2][0] == sign and board[2][1] == sign and board[2][2] == sign:
            return("third row", sign)
    else:
        return ("no winner")

def columns_checker(board):
    #Check all columns for matching (up to down)
    
    for sign in (-1, 1):
        if board[0][0] == sign and board[1][0] == sign and board[2][0] == sign:
            return ("first column", sign)
        if board[0][1] == sign and board[1][1] == sign and board[2][1] == sign:
            return ("second column", sign)
        if board[0][2] == sign and board[1][2] == sign and board[2][2] == sign:
            return("third column", sign)    
    else:
        return ("no winner")

def diagonals_checker(board):
    #Check all diagonals for matching
    
    for sign in (-1, 1):
        if board[0][0] == sign and board[1][1] == sign and board[2][2] == sign:
            return ("top left corner to bottem right corner", sign)
        if board[0][2] == sign and board[1][1] == sign and board[2][0] == sign:
            return ("top right corner to bottem left corner", sign)
    else:
        return ("no winner")

def tie_checker(board):    
    #Check if it is a tie
    
    if rows_checker(board) == "no winner" and columns_checker(board) == "no winner" and diagonals_checker(board) == "no winner":
        tie = ("tie" ,True)
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    tie = ("game running", False)
    
    return (tie)

def score_input_taker():
    #This function creates an interface that accepts a number for the score that the game will go to
    rectMode(TOP)
    fill(0)
    rect(0, 0, 900, 900)
    pass
    
def score_display(score):
    #This function displays the current score
    xwins = score[0]
    owins = score[1]
    message = str("x:" + str(xwins) + " o:" + str(owins))

    textSize(20)
    fill(0)
    text(str("x: " + str(xwins) + " o: " + str(owins)), 30, 50)


def turn_display():
    #This function displays whos turn it is
    pass

def end_screen(current_state): #score is in the form [x score, o score]
    #This function creates the end screen when a player has won the game

    textSize(25)    

    fill(0)
    if current_state[0] == 'tie':
        text("This was a draw!", 100, 100)

        return ("tie")
    if current_state[1] == 1:
        text("The player who is playing X has won!", 100, 100)

        return ("x won")
    elif current_state[1] == -1:
        text("The player who is playing O has won!", 100, 100)

        return ("o won")
        

def keyPressed():
    global next_game, current_input, score, game_state, max_score, finished_input
    #This function is involved in checking the input during the score input

    if key == CODED:
        if keyCode == UP:
            max_score += 1
        elif keyCode == DOWN and max_score > 1:
            max_score -= 1
    if key == "c":
        finished_input = True
    pass
    
def winner_displayer(score): 
    #This function takes in a score in array form of [x score, o score] finds the greater score and displays the ultimate winner in on the screen
    fill(0)
    textSize(35)
    if score[0] > score[1]:
        text("X is the ultimate winner!", 100, 100)
    if score[0] < score[1]:
        text("O is the ultimate winner!", 100, 100)
