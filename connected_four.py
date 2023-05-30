#import Library 
from pettingzoo.classic import connect_four_v3
import math
import random
import numpy as np
# Create Environment
env = connect_four_v3.env(render_mode="human")

ROWS=6
COLS=7
maximizer=1
minimizer=2



def drop_piece(tabel,row,col,piece):
    table[row][col]=piece
def get_next_open_row(table,col):
    for r in range (ROWS-1,-1,-1):
        if table[r][col]==0:
            return 0
        
def winning_move(table,piece):
    for c in range(COLS-3):
        for r in range(ROWS):
            if table[r][c] == piece and table[r][c+1] == piece and table[r][c+2] == piece and table[r][c+3] == piece:
                return True
    for c in range(COLS):
        for r in range(ROWS-3):
            if table[r][c] == piece and table[r+1][c] == piece and table[r+2][c] == piece and table[r+3][c] == piece:
                return True
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if table[r][c] == piece and table[r-1][c+1] == piece and table[r-2][c+2] == piece and table[r-3][c+3] == piece:
                return True
    for c in range(3,COLS):
        for r in range(3, ROWS):
            if table[r][c] == piece and table[r-1][c-1] == piece and table[r-2][c-2] == piece and table[r-3][c-3] == piece:
                return True

def evaluate_array_score(array,piece):
    if piece==1:
        opponent_piece=minimizer
    else:
        opponent_piece=maximizer
    score=0
    if array.count(piece)==4:
        score+=100
    elif array.count(piece)==3 and array.count(0)==1:
        score+=5
    elif array.count(piece)==2 and array.count(0)==2:
        score+=2
    if array.count(opponent_piece)==3 and array.count(0)==1:
        score-=4
    return score



def score (table, piece):
    score =0
    center_array=[int(i) for i in list(table[:,COLS//2])]
    center_count=center_array.count(piece)
    score+=center_count*6
    #ofoghi
    for r in range (ROWS):
        row_array = [int(i) for i in list(table[r,:])]
        for c in range (COLS-3):
            array=row_array[c:c+4]
            score+=evaluate_array_score(array,piece)

    for c in range (COLS):
        col_array= [int(i) for i in list(table[:,c])]
        for r in range (ROWS-3):
            array=col_array[r:r+4]
            score+=evaluate_array_score(array,piece)
    for r in range (3,ROWS):
        for c in range (COLS-3):
            array=[table[r-i][c+i] for i in range (4)]
            score+=evaluate_array_score(array,piece)
    for r in range (3,ROWS):
        for c in range (3,COLS):
            array=[table[r-i][c-i] for i in range (4)]
            score+=evaluate_array_score(array,piece)

    return score

def is_valid_location(table, col):
    return table[0][col] == 0

def is_terminal_node(table):
    return winning_move(table,maximizer) or winning_move(table,minimizer) or len (get_valid_locations(table))==0
def get_valid_locations(table):
    valid_locations = []
    for column in range(COLS):
        if is_valid_location(table, column):
            valid_locations.append(column)
    return valid_locations



def minimax(table,depth,alpha,beta,maximizing_player):
    valid_locations=get_valid_locations(table)
    is_terminal=is_terminal_node(table)
    if depth==0 or is_terminal:
        if is_terminal:
            if winning_move(table,maximizer):
                return (None,100000)
            elif winning_move(table,minimizer):
                return (None,-10000)
            else:
                return (None,0)
        else:
            return (None,score(table,maximizer))
    if maximizing_player:
        value= -math.inf
        column=random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(table,col)
            t_copy=table.copy()
            drop_piece(t_copy,row,col,maximizer)
            _,new_score=minimax(t_copy,depth-1,alpha,beta,False)
            if new_score>value:
                value=new_score
                column=col
            alpha= max(value,alpha)
            if alpha >=beta:
                break
        return column,value
    else:
        value=math.inf
        column=random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(table,col)
            t_copy=table.copy()
            drop_piece(t_copy,row,col,minimizer)
            _,new_score=minimax(t_copy,depth-1,alpha,beta,True)
            # print("new_score",new_score,type(new_score))
            # print("value",value,type(value))
            if new_score<value:
                value=new_score
                column = col
            beta=min(value,beta)
            if alpha>=beta:
                break
        return column , value
    

def create_table(env,k):
    
    observation, _, _, _, _ = env.last()
    list=observation["observation"]
    table=np.zeros((ROWS,COLS))
    if k ==1:
        l=0
    else:
        l=1
    for i in range (ROWS):
        for j in range (COLS):
            if list[i][j][k]==1:
                table[i][j]=1
            if list[i][j][l]==1:
                table[i][j]=2
            
    return table
env.reset()
a=0
act=0
for agent in env.agent_iter():
    a%=2
    act+=1
    observation, reward, termination, truncation, info = env.last()
    table=create_table(env,a)
    print("action :",act)
    print(table)

    if termination or truncation:

        action = None

    else:
        # if a==1:

        action,minimax_score=minimax(table,5,-math.inf,math.inf,True)
        # else:
        #     action,_=minimax(table,5,-math.inf,math.inf,True)
        print(action)

    
    a+=1
    env.step(action)
    env.render()



    

env.close()
