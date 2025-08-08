from random import randint

player = {}
game_map = []
fog = []
portal_location = None

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    with open('level1.txt', 'r') as map_file:
        for line in map_file:
            row = list(line.rstrip('\n'))
            map_struct.append(row)
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()


# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, game_map, player):
    for y in range(player['y'] - 1, player['y'] + 2):
        for x in range(player['x'] - 1, player['x'] + 2):
            if 0 <= y < len(fog) and 0 <= x < len(fog[0]):
                fog[y][x] = game_map[y][x]


def initialize_game(game_map, fog, player, name):
    # initialize map
    load_map("level1.txt", game_map)

    # initialize fog
    for line in game_map:
        row = []
        for char in line:
            row.append('?')
        fog.append(row)
    
    # initialize player
    player['symbol'] = game_map[0][0]
    
    # player dictionary
    player['x'] = 0
    player['y'] = 0
    player['symbol'] = 'M'
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['name'] = name
    player['backpack'] = 10
    player['pickaxe'] = 1
    player['pickaxe_mineral'] = 'copper'
    player['load'] = 0
    player['steps'] = 0

    clear_fog(fog, game_map, player)
 
 
# This function is for when player in mine    
def mine(mine_menu_input):
    global game_map, fog, player, game_state
    x, y = 0, 0
    if mine_menu_input == 'W':
       y = -1
    elif mine_menu_input == 'A':
        x = -1
    elif mine_menu_input == 'S':
       y = 1
    elif mine_menu_input == 'D':
        x = 1
    elif mine_menu_input == 'M':
         draw_map(game_map, fog, player)
         return
    elif mine_menu_input == 'I':
        show_information(player)
        return
    elif mine_menu_input == 'P':
        print('You place your portal stone here and zap back to town.')
        global portal_location
        portal_location = (player['x'], player['y'])
        
        copper, copper_earned = sell_minerals()
        print('You sell {} copper ore for {} GP.'.format(copper, copper_earned))
        print('You now have {} GP!'.format(player['GP']))
        
        player['day'] += 1
        player['turns'] = TURNS_PER_DAY
        player['load'] = 0
        
        game_state = 'town'
        return
    elif mine_menu_input == 'Q':
        game_state = 'main'
        return
    
    new_x = player['x'] + x
    new_y = player['y'] + y
            
    player['turns'] -= 1
    player['steps'] += 1
    
    if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
        print("You cannot move outside the map!")
        return
    
    tile = game_map[new_y][new_x]
    
    if tile in mineral_names:
        if player['load'] >= player['backpack']:
            print("You can't carry any more, so you can't go that way.")
            return
        else:
            if tile == 'C':
                max_amount = 5
            elif tile == 'S':
                max_amount = 3
            elif tile == 'G':
                max_amount = 2
            mined = randint(1,max_amount)
            
            space = player['backapck'] - player['load']
            if mined > space:
                print('You mined {} pieces of {}'.format(mined, mineral_names[tile]))
                print('...but you can only carry {} more piece(s)!'.format(space))
                mined = space
            else:
                print('You mined {} pieces of {}'.format(mined, mineral_names[tile]))
                
            player[mineral_names[tile]] += mined
            player['load'] += mined
            
            game_map[new_y][new_x] = '.'
            fog[new_y][new_x] = '.'
    
    player['x'] = new_x
    player['y'] = new_y
    
    clear_fog(fog, game_map, player)
    
    if new_x == 0 and new_y == 0:
        print('You returned back to town.')
        game_state = 'town'
        return
    
    if player['turns'] <= 0:
        print('You are exhausted.')
        print('You place your portal stone here and zap back to town.')
        copper, copper_earned = sell_minerals()
        print('You sell {} copper ore for {} GP.'.format(copper, copper_earned))
        print('You now have {} GP!'.format(player['GP']))
        player['day'] += 1
        player['turns'] = TURNS_PER_DAY
        player['load'] = 0
        game_state = 'town'
        
    
# This function prints the mine menu
def show_mine_menu():
    print('---------------------------------------------------')
    print('                     DAY {}                        '
          .format(player['day']))
    print('---------------------------------------------------')
    print('Day {}'.format(player['day']))
    draw_view(game_map, fog, player)
    print('Turns left: {}      Load: {}/{}      Steps: {}'
          .format(player['turns'], player['load'], player['backpack'], player['steps']))
    print('(WASD) to move')
    print('(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu')
    mine_menu_input = input('Action? ').upper()
    return mine_menu_input
    
    
# This function draws the entire map, covered by the fog
def draw_map(game_map, fog, player):
    print('+' + '-'*MAP_WIDTH + '+')
    for y in range(len(game_map)):
        row = '|'
        for x in range(len(game_map[y])):
            if (x, y) == (player['x'], player['y']):
                row += player['symbol']
            elif portal_location != None and (x,y) == portal_location:
                row += 'P'
            else:
                row += fog[y][x]
        row += '|'
        print(row)
    
    print('+' + '-'*MAP_WIDTH + '+')


# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    print('+' + '-'*3 +'+')
    for y in range(player['y']-1, player['y']+2):
        row = '|'
        for x in range(player['x']-1, player['x']+2):
            if 0 <= y < len(game_map) and 0 <= x < len(game_map[0]):
                row += game_map[y][x]
        row += '|'
        print(row)
    
    print('+' + '-'*3 +'+')


# This function shows the information for the player
def show_information():
    print('----- Player Information -----')
    print('Name: {}'.format(player['name']))
    print('Portal position: ({}, {})'.format(player['x'], player['y']))
    print('Pickaxe level: {} ({})'.format(player['pickaxe'], player['pickaxe_mineral']))
    print('------------------------------')
    print('Load: {}/{}'.format(player['load'] ,player['backpack']))
    print('------------------------------')
    print('GP: {}'.format(player['GP']))
    print('Steps taken: {}'.format(player['steps']))
    print('------------------------------')
    show_town_menu()
    return


# This function saves the game
def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
    return

        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return


# This function prints the main menu
def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")
    main_menu_input = input('Your choice? ').upper()
    return main_menu_input
 
 
#This functions adds the amount earned into the dictionary   
def sell_minerals():
    global player
    copper_price = randint(prices['copper'][0], prices['copper'][1])
    silver_price = randint(prices['silver'][0], prices['silver'][1])
    gold_price = randint(prices['gold'][0], prices['gold'][1])
    copper_earned = (player['copper']*copper_price)
    silver_earned = (player['silver']*silver_price)
    gold_earned = (player['gold']*gold_price)
    player['GP'] += copper_earned + silver_earned + gold_earned
    copper = player['copper']
    silver = player['silver']
    gold = player['gold']
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    return copper, copper_earned


# This function prints the town menu
def show_town_menu():
    print()
    print('Day {}'.format(player['day']))
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
    town_menu_input = input('Your choice? ').upper()
    return town_menu_input
    
    
# This function prints the shop menu    
def show_shop_menu():
    new_capacity = player['backpack']+2
    backpack_price = player['backpack']*2
    print()
    print("----------------------- Shop Menu -------------------------")
    print("(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP")
    print("(B)ackpack upgrade to carry {} items for {} GP".format(new_capacity, backpack_price))
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print("GP: {}".format(player['GP']))
    print("-----------------------------------------------------------")
    shop_menu_input = input('Your choice? ').upper()
    return backpack_price, shop_menu_input


#This function upgrades the backpack capacity    
def backpack_upgrade(backpack_price):
    global player
    player['backpack'] += 2
    player['GP'] -= backpack_price
    
            

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")
    
while True:
    if game_state == 'main':
        action = show_main_menu()
        if action == 'N':
            name = input("Enter your name: ")
            initialize_game(game_map, fog, player, name)
            game_state = 'town'
        elif action == 'L':
            load_game(game_map, fog, player)
            game_state = 'town'
        elif action == 'Q':
            game_state = 'main'
            break
        else:
            print('Invalid input.')
            game_state = 'town'

    elif game_state == 'town':
        action = show_town_menu()
        if action == 'B':
            game_state = 'shop'
        elif action == 'I':
            show_information()
        elif action == 'M':
            draw_map(game_map, fog, player)
        elif action == 'V':
            save_game(game_map, fog, player)
            print("Game saved.")
        elif action == 'Q':
            game_state = 'main'
        else:
            print('Invalid input.')
            
    elif game_state == 'shop':
        backpack_price, action = show_shop_menu()
        if action == 'B':
            if player['GP'] >= backpack_price:
                backpack_upgrade()
                print('Congratulations! You can now carry {} items.'
                      .format(player['backpack']))
                game_state = 'shop'
            else:
                print('Sorry you dont have enough GP.')
                game_state = 'shop'
        elif action == 'L':
            show_town_menu()
            game_state = 'town'
        else:
            print('Invalid input.')
            
    elif game_state == 'mine':
        mine()  # inside this, game_state might be changed to 'town'
        if action == 'B':
            print('hi')
        else:
            print('Invalid input.')


