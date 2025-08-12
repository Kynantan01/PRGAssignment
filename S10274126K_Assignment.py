# Kynan Tan S10274126K 
# This is a program of a game called Sundrop Caves
from random import randint

player = {}
game_map = []
fog = []
portal_location = None
magic_torch = False
winner = {}
top_scores = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    global MAP_WIDTH
    global MAP_HEIGHT
    
    
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
    player['pickaxe_lvl'] = 1
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
    else:
        print('Invalid input.')
        return
    
    new_x = player['x'] + x
    new_y = player['y'] + y
            
    player['turns'] -= 1
    player['steps'] += 1
    
    if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
        print("You cannot move outside the map!")
        return
    
    tile = game_map[new_y][new_x]
    
    pickaxe_minerals = {
        1 : ['C'],
        2 : ['C', 'S'],
        3 : ['C', 'S', 'G']
    }
    
    mineable_minerals = pickaxe_minerals[player['pickaxe_lvl']]
    
    if tile in mineral_names and tile not in mineable_minerals:
        print('Your pickaxe is not strong enough to mine this.')
        return
    
    
    
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
            
            space = player['backpack'] - player['load']
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
        portal_location = (player['x'], player['y'])
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
    global portal_location
    print('+' + '-'*MAP_WIDTH + '+')
    for y in range(len(game_map)):
        row = '|'
        for x in range(len(game_map[y])):
            if portal_location != None and (x,y) == portal_location:
                row += 'P'
            elif (x, y) == (player['x'], player['y']):
                row += player['symbol']
            else:
                row += fog[y][x]
        row += '|'
        print(row)
    
    print('+' + '-'*MAP_WIDTH + '+')


# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    if magic_torch == False:
        vision_radius = 2
        start_x = max(0, player['x'] - vision_radius)
        start_y = max(0, player['y'] - vision_radius)
        end_x = min(len(game_map[0]), player['x'] + vision_radius + 1)
        end_y = min(len(game_map), player['y'] + vision_radius + 1)

        print('+' + '-' * (end_x - start_x) + '+')
        for y in range(start_y, end_y):
            row = '|'
            for x in range(start_x, end_x):
                if (x, y) == (player['x'], player['y']):
                    row += player['symbol']
                elif portal_location is not None and (x, y) == portal_location:
                    row += 'P'
                else:
                    row += fog[y][x]
            row += '|'
            print(row)
        print('+' + '-' * (end_x - start_x) + '+')
    else:
        vision_radius = 2
        start_x = max(0, player['x'] - vision_radius)
        start_y = max(0, player['y'] - vision_radius)
        end_x = min(len(game_map[0]), player['x'] + vision_radius + 1)
        end_y = min(len(game_map), player['y'] + vision_radius + 1)

        print('+' + '-' * (end_x - start_x) + '+')
        for y in range(start_y, end_y):
            row = '|'
            for x in range(start_x, end_x):
                if (x, y) == (player['x'], player['y']):
                    row += player['symbol']
                elif portal_location is not None and (x, y) == portal_location:
                    row += 'P'
                else:
                    row += fog[y][x]
            row += '|'
            print(row)
        print('+' + '-' * (end_x - start_x) + '+')


# This function shows the information for the player
def show_information():
    print('----- Player Information -----')
    print('Name: {}'.format(player['name']))
    print('Portal position: ({}, {})'.format(player['x'], player['y']))
    print('Pickaxe level: {} ({})'
          .format(player['pickaxe_lvl'], player['pickaxe_mineral']))
    print('------------------------------')
    print('Load: {}/{}'.format(player['load'] ,player['backpack']))
    print('------------------------------')
    print('GP: {}'.format(player['GP']))
    print('Steps taken: {}'.format(player['steps']))
    print('------------------------------')
    return


# This function saves the game
def save_game():
    global game_map, fog, player
    map_save = 'map_save.txt'
    fog_save = 'fog_save.txt'
    player_save = 'player_save.txt'
    
    # save map
    with open(map_save, 'w') as map_file:
        for row in game_map:
            map_file.write(''.join(row) + '\n')
        
    # save fog
    with open(fog_save, 'w') as fog_file:
        for row in fog:
            fog_file.write(''.join(row) + '\n')
        
    # save player
    with open(player_save, 'w') as player_file:
        for key, value in player.items():
            player_file.write('{}={}\n'.format(key, value))
    return

        
# This function loads the game
def load_game():
    global game_map, fog, player
    
    # load map
    with open('map_save.txt', 'r') as map_file:
        game_map.clear()
        for line in map_file:
            game_map.append(list(line.rstrip('\n')))
        
    # load fog
    with open('fog_save.txt', 'r') as fog_file:
        fog.clear()
        for line in fog_file:
            fog.append(list(line.rstrip('\n')))
        
    # load player
    with open('player_save.txt', 'r') as player_file:
        player.clear()
        for line in player_file:
            line = line.strip()
            if not line:
                continue
            key, value = line.split('=')
            if value.isdigit():
                value = int(value)
            player[key] = value
    return 


# This function prints the main menu
def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
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
    new_pickaxe = player['pickaxe_lvl']+1
    magic_torch_price = 50
    if player['pickaxe_lvl'] + 1 == 2:
        pickaxe_price = 50
    elif player['pickaxe_lvl'] + 1 == 3:
        pickaxe_price = 150
    else:
        pickaxe_price = 0
    
    print()
    print("----------------------- Shop Menu -------------------------")
    if player['pickaxe_lvl'] < 3:
        print("(P)ickaxe upgrade to Level {} to mine silver ore for {} GP"
            .format(new_pickaxe, pickaxe_price))
    print("(B)ackpack upgrade to carry {} items for {} GP"
          .format(new_capacity, backpack_price))
    if magic_torch == False:
        print('(M)agic torch upgrade to see more in the mine for {} GP.'
              .format(magic_torch_price))
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print("GP: {}".format(player['GP']))
    print("-----------------------------------------------------------")
    shop_menu_input = input('Your choice? ').upper()
    return backpack_price, pickaxe_price, shop_menu_input


# This function upgrades the backpack capacity    
def backpack_upgrade(backpack_price):
    global player
    player['backpack'] += 2
    player['GP'] -= backpack_price
    

# This function upgrades the pickaxe
def pickaxe_upgrade(pickaxe_price):
    global player
    player['pickaxe_lvl'] += 1
    if player['pickaxe_lvl'] == 2:
        player['pickaxe_mineral'] = 'silver'
    elif player['pickaxe_lvl'] == 3:
        player['pickaxe_mineral'] = 'gold'
    player['GP'] -= pickaxe_price    
            
            
# This function creates a file of the top scores
def save_top_scores():
    global player
    with open('top_scores.txt', 'a') as scores_file:
        scores_file.write('{},{},{},{}\n'
                          .format(player['name'], player['day'],player['GP'], player['steps']))
        
        
# This function loads the top scores
def load_top_scores():
    global top_scores
    with open('top_scores.txt', 'r') as scores_file:
        for line in scores_file:
            name, days, gp, steps =line.strip().split(',')
            top_scores.append({
                'name' : name,
                'days' : int(days),
                'gp' : int(gp),
                'steps' : int(steps)   
            })
            
    top_scores.sort(key=lambda s: (s['days'], s['steps'], -s['gp']))
        
            
# This function shows the top scores
def show_top_scores():
    load_top_scores()
    print()
    print('---------------- Top 5 Sundrop Caves Players ----------------')
    if not top_scores:
        print('No scores yet!')
        return
    print("{:<5} {:<15} {:<10} {:<10} {:<10}".format('Rank', 'Name', 'Days', 'GP', 'Steps'))
    count = 1
    for s in top_scores[:5]:
        print('{}. {:<15}, {:<10}, {:<10}, {:<10}'
              .format(count, s['name'], s['days'], s['gp'], s['steps']))
        count += 1


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
        elif action == 'H':
            show_top_scores()
        else:
            print('Invalid input.')
            
    elif player['GP'] >= 500:
        print('Woo-hoo! Well done, {}, you have {} GP!'
              .format(player['name'], player['GP']))
        print('You now have enough to retire and play video games evry day.')
        print('And it only took you {} days and {} steps! You win!'
              .format(player['day'], player['steps']))
        winner['name'] = player['name']
        game_state = 'main'

    elif game_state == 'town':
        action = show_town_menu()
        if action == 'B':
            game_state = 'shop'
        elif action == 'I':
            show_information()
        elif action == 'M':
            draw_map(game_map, fog, player)
        elif action == 'E':
            game_state = 'mine'
        elif action == 'V':
            save_game()
            print("Game saved.")
        elif action == 'Q':
            game_state = 'main'
        else:
            print('Invalid input.')
            
    elif game_state == 'shop':
        backpack_price, pickaxe_price, action = show_shop_menu()
        cor_input = False
        if player['pickaxe_lvl'] < 3:
            if action == 'P':
                cor_input = True
                if player['GP'] >= pickaxe_price:
                    pickaxe_upgrade(pickaxe_price)
                    if player['pickaxe_lvl'] == 2:
                        print('Congratulations! You can now mine silver!')
                    elif player['pickaxe_lvl'] == 3:
                        print('Congratulations! You can now mine gold!')
                else:
                        print("Sorry you don't have enough GP.")
                        
        if action == 'B':
            cor_input = True
            if player['GP'] >= backpack_price:
                backpack_upgrade(backpack_price)
                print('Congratulations! You can now carry {} items.'
                      .format(player['backpack']))
            else:
                print('Sorry you dont have enough GP.')
                
        if magic_torch == False:        
            if action == 'M':
                cor_input = True
                if player['GP'] >= 50:
                    magic_torch = True
                    player['GP'] -= 50
                    print('Congratulations! You can now see further.')
                else:
                    print("Sorry you don't have enough GP.") 
                          
        if action == 'L':
            cor_input = True
            game_state = 'town'
            
        if cor_input == False:
            print('Invalid input.')
            
    elif game_state == 'mine':
        action = show_mine_menu()
        if action == 'M':
            draw_map(game_map, fog, player)
        elif action == 'I':
            show_information()
        elif action == 'P':
            print('You place your portal stone here and zap back to town.')
            portal_location = (player['x'], player['y'])
            copper, copper_earned = sell_minerals()
            print('You sell {} copper ore for {} GP.'.format(copper, copper_earned))
            print('You now have {} GP!'.format(player['GP']))
            
            player['day'] += 1
            player['turns'] = TURNS_PER_DAY
            player['load'] = 0
            
            game_state = 'town'
        elif action == 'Q':
            game_state = 'main'      
        else:
            mine(action)