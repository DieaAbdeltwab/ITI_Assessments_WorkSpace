import os
def clear_terminal():
    # Check the OS name
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')
        
PLAYER_1_SYMBOL = "X"
PLAYER_2_SYMBOL = "O"

def print_xo_gui (list_xo):
    print(f"+---+---+---+")
    print(f"| {list_xo[0][0]} | {list_xo[0][1]} | {list_xo[0][2]} |")
    print(f"+---+---+---+")
    print(f"| {list_xo[1][0]} | {list_xo[1][1]} | {list_xo[1][2]} |")
    print(f"+---+---+---+")
    print(f"| {list_xo[2][0]} | {list_xo[2][1]} | {list_xo[2][2]} |")
    print(f"+---+---+---+")    
    
def update_list_xo (list_xo , xo_position_key , player_turn  ) :
    update_success = False
    if xo_position_key <= 3 :
        if list_xo[0][xo_position_key-1] != PLAYER_1_SYMBOL and list_xo[0][xo_position_key-1] != PLAYER_2_SYMBOL :
            list_xo[0][xo_position_key-1] = player_turn
            update_success =  True
    elif xo_position_key <= 6 :
        if list_xo[1][xo_position_key-4] != PLAYER_1_SYMBOL and list_xo[1][xo_position_key-4] != PLAYER_2_SYMBOL :
            list_xo[1][xo_position_key-4] = player_turn
            update_success = True
    elif xo_position_key <= 9 :
        if list_xo[2][xo_position_key-7] != PLAYER_1_SYMBOL and list_xo[2][xo_position_key-7] != PLAYER_2_SYMBOL :
            list_xo[2][xo_position_key-7] = player_turn
            update_success = True
    return  update_success          

       
def end_game_xo (list_xo) :
    end_game_report = True
    winer_symbol    = False
    if list_xo[0][0] == list_xo[1][1] == list_xo[2][2] or  list_xo[0][2] == list_xo[1][1] == list_xo[2][0] :
        winer_symbol =  list_xo[1][1]
    else :
        for counter in range (0,3):
            if  list_xo[counter][0] == list_xo[counter][1] == list_xo[counter][2] :
                winer_symbol =  list_xo[counter][0]
            elif list_xo[0][counter] == list_xo[1][counter] == list_xo[2][counter] :
                winer_symbol =  list_xo[0][counter]
    for counter_x in range (3):
        for counter_y in range (3):
            if list_xo[counter_x][counter_y] != "X" and list_xo[counter_x][counter_y] != "O" : 
                end_game_report =  winer_symbol
    return end_game_report  
                

def main_xo_game ( ) :
    players_turn = PLAYER_1_SYMBOL 
    xo_list = [ [x+1,x+2,x+3] for x in range(0,9,3) ]
    while True :
        print_xo_gui(xo_list)
        print (f"Player { 1 if players_turn== PLAYER_1_SYMBOL else 2} : { players_turn  } ")
        try :
            key = int(input("Enter number From 1 to 9 and 0 to quit (GUI index) : "))
        except ValueError:
            clear_terminal()
            print("Enter Valed input !")
        else :
            clear_terminal()
            if key == 0:
                print("Goodbye...")
                break
            elif key < 10 :
                if players_turn == PLAYER_1_SYMBOL: 
                    if update_list_xo(xo_list , key , players_turn  ) :
                        players_turn = PLAYER_2_SYMBOL
                    else :
                        print ("Choose a valid Plase :empty ")
                elif players_turn == PLAYER_2_SYMBOL:
                    if update_list_xo(xo_list , key , players_turn  ) :
                        players_turn = PLAYER_1_SYMBOL
                    else :
                        print ("Choose a valid Plase :empty ")
                
            
                if PLAYER_1_SYMBOL == end_game_xo(xo_list) :
                    print_xo_gui(xo_list)
                    print ("We have winer is : Player 1  ")
                    break
                elif PLAYER_2_SYMBOL == end_game_xo(xo_list) :
                    print_xo_gui(xo_list)
                    print ("We have winer is : Player 2  ")
                    break
                elif True == end_game_xo (xo_list) :
                    print_xo_gui(xo_list)
                    print ("We Don't have Winner : game Ended  ")
                    break
            else :
                print("Enter Valed Number !")
            


while True :
    try :
        start_end = int(input ("Enter 1 to start Game and 0 to end Game : "))
    except ValueError:
        print("Enter Valed input !")
    else :
        if start_end == 1 :
            main_xo_game(  )
        elif start_end == 0 :
            print("Goodbye...")
            break
        else :
            print("Enter Valed Number !")

            

        
             