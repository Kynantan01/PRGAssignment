from random import randint

player = {}
game_map = []
fog = []

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
    
# This function draws the entire map, covered by the fog
def draw_map(game_map, fog, player):
    for y in range(8, len(game_map)):
        row = ''
        for x in range(8, len(game_map[y])):
            if x == player['x'] and y == player['y']:
                row += player['symbol']
            else:
                row += fog[y][x]
        print(row)

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    for y in range(player['y']-1, player['y']+2):
        row = ''
        for x in range(player['x']-1, player['x']+2):
            if 0 <= y < len(game_map) and 0 <= x < len(game_map[0]):
                row += game_map[y][x]
        print(row)

# This function shows the information for the player
def show_information(player):
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
    show_town_menu
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
    main_menu_input = input('Your choice? ')
    return main_menu_input
 
#This functions adds the amount earned into the dictionary   
def sell_minerals():
    copper_price = randint(prices['copper'][0], prices['copper'][1])
    silver_price = randint(prices['silver'][0], prices['silver'][1])
    gold_price = randint(prices['gold'][0], prices['gold'][1])
    gp_earned = (player['copper']*copper_price)+(player['silver']*silver_price)+(player['gold']*gold_price)
    player['GP'] += gp_earned

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
    town_menu_input = input('Your choice? ')
    return town_menu_input
    
# This function prints the shop menu    
def shop_menu():
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
    shop_menu_input = input('Your choice? ')
    return backpack_price, shop_menu_input

#This function upgrades the backpack capacity    
def backpack_upgrade(backpack_price):
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
    


