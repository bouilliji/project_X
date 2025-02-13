import pyxel
from time import time, sleep
from math import sqrt, sin, cos, atan2
from random import random

#==================================================
#------------------>comment
#==================================================

#weapon:duplicator; pixel_l;Bit_Ray;Code-trapper



#==================================================
#------------------>data
#==================================================
enemy = {}
bullet = {}
player = {'x': 50, 'y': 50, 'size': 16, "reload": 100, "hp": 100, "main_weapon": "duplicator", "inventory": ["pixel_l" , "duplicator","Bit_Ray","Code_trapper"], "level": 0}
last_direction = [1, 0]  # left direction
screen_size = [256,256]



#==================================================
#------------------>function
#==================================================
def enemy_spawn(x, y, radius, hp, damage):
    global enemy
    """Spawns an enemy at a given position with certain radius and health points."""
    enemy[f"enemy{time()}"] = {'x': x, 'y': y, 'radius': radius, "hp": hp, "damage": damage}
    sleep(0.01)

def bullet_spawn(x, y, size, direction, damage):
    global bullet
    """Spawns a projectile with a certain size and direction."""
    bullet[f"bullet{time()}"] = {'x': x, 'y': y, 'size': size, 'direction': direction, "damage": damage}
    sleep(0.01)

def direction_axe():
    """return variation on x and y axes"""
    return (pyxel.btn(pyxel.KEY_D) - pyxel.btn(pyxel.KEY_Q), pyxel.btn(pyxel.KEY_S) - pyxel.btn(pyxel.KEY_Z))

#________________________weapon________________________
def shoot_player():
    if player["main_weapon"] == "pixel_l":
        pixel_l(player)
    elif player["main_weapon"] == "duplicator":
        duplicator(player)
    elif player["main_weapon"] == "Bit_Ray":
        Bit_Ray(player)
    elif player["main_weapon"] == "Code_trapper":
        Code_trapper(player)

def pixel_l(player):
    
    if player["reload"] >= 20 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  # reload time
        size = 8  # bullet size
        dx =pyxel.mouse_x-player['x'] - player['size'] / 2 
        dy =pyxel.mouse_y-player['y'] - player['size'] / 2 
        angle = atan2(dy, dx)
        vx=cos(angle)
        vy=sin(angle)

        bullet_x = player['x'] + player['size'] / 2 
        bullet_y = player['y'] + player['size'] / 2 

        bullet_spawn(bullet_x, bullet_y, size, [vx * 5, vy * 5],20)
        player["reload"] -= 20  
    
    if player["reload"] < 100:
        player["reload"] += 1
        
def duplicator(player):
    """Shoots a projectile in the last recorded direction if the space bar is pressed."""
    if player["reload"] >= 100 and pyxel.btnp(pyxel.KEY_SPACE):  # reload time
        size = player['size'] # bullet size
        damage = (player["reload"]/100)*player['hp']
        vx, vy = last_direction  # use the last direction of the player
            
        bullet_x = player['x'] + player['size'] / 2 - size/2
        bullet_y = player['y'] + player['size'] / 2 - size/2

        bullet_spawn(bullet_x, bullet_y, size, [vx * 5, vy * 5], damage)
        player["reload"] = 0
    if player["reload"] < 100:
        player["reload"] += 1


def Bit_Ray(player):
   
    if player["reload"] >= 1 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) == 1:  
        
        dx =pyxel.mouse_x-player['x'] - player['size'] / 2 
        dy =pyxel.mouse_y-player['y'] - player['size'] / 2 
        angle = atan2(dy, dx)
        vx=cos(angle)
        vy=sin(angle)
        size = 2
        damage = 2
        
        for i in range(1):
            bullet_x = player['x'] + (player['size']*random())
            bullet_y = player['y'] + (player['size']*random())
            bullet_spawn(bullet_x, bullet_y, 2, [vx * 20, vy *20], damage)
        player["reload"] -= 2
    elif player["reload"] < 100:
        player["reload"] += 1



def Code_trapper(player):
    if player["reload"] >= 50 and pyxel.btnp(pyxel.KEY_SPACE):  # reload time
        size = 4
        damage = 4
        print("je suis la")

        for i in range(player["size"]+1):
            bullet_x = player['x'] + i*8 - size/2 
            bullet_y = player['y'] + player['size'] - size/2
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage)
        for i in range(player["size"]+1):
            bullet_x = player['x'] + i*8 - size/2 
            bullet_y = player['y'] - size/2
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage)
        for i in range(player["size"]-1):
            bullet_x = player['x'] - size/2 
            bullet_y = player['y'] - size/2 + (i+1)*8
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage)
        for i in range(player["size"]-1):
            bullet_x = player['x'] - size/2 + player['size']
            bullet_y = player['y'] - size/2 + (i+1)*8
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage)
        
        damage = player['size'] / 2
        size = player['size'] / 2
        bullet_x = player['x'] + player['size'] / 2 - size/2
        bullet_y = player['y'] + player['size'] / 2 - size/2
        bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage)

        
        
        player["reload"] -= 50
    if player["reload"] < 100:
        player["reload"] += 0.5

#________________________enemy update________________________
def update_enemy():
    global enemy, player
    for name in enemy.keys():

        #hitbox with other enemy
        for otherName in enemy.keys():
            if name != otherName :
                dx = enemy[otherName]['x']-enemy[name]['x']
                dy = enemy[otherName]['y']-enemy[name]['y']
                dist_to_other = sqrt(dx**2 + dy**2)

                if dist_to_other < enemy[otherName]['radius'] + enemy[name]['radius']:
                    if dist_to_other > 0:
                        enemy[name]['x'] -= dx / dist_to_other
                        enemy[name]['y'] -= dy / dist_to_other
                        enemy[otherName]['x'] += dx / dist_to_other
                        enemy[otherName]['y'] += dy / dist_to_other

        #calcul values vector
        vec_x = (player['x'] + player['size'] / 2) - enemy[name]['x']
        vec_y = (player['y'] + player['size'] / 2) - enemy[name]['y']
        norm = sqrt(vec_x ** 2 + vec_y ** 2)
        

        #colition with player
        if norm < enemy[name]['radius'] + player['size'] / 2:
            enemy[name]['x'] -= int(round(vec_x / norm))  * 3
            enemy[name]['y'] -= int(round(vec_y / norm)) * 3
            player['x'] += int(round(vec_x / norm)) * 3  # Collision reaction
            player['y'] += int(round(vec_y / norm)) * 3
            player['hp'] -= enemy[name]['damage']
        #normal action
        elif norm > 0:
            enemy[name]['x'] += int(round(vec_x / norm)) * 2
            enemy[name]['y'] += int(round(vec_y / norm)) * 2

#________________________bullet update________________________
def update_bullet():
    global bullet, enemy, screen_size
    for bulletName in list(bullet.keys()):
        bullet[bulletName]['x'] += bullet[bulletName]['direction'][0]
        bullet[bulletName]['y'] += bullet[bulletName]['direction'][1]

        # delete bullet outside the screen
        if not (0 <= bullet[bulletName]['x'] <= screen_size[0] and 0 <= bullet[bulletName]['y'] <= screen_size[1]):
            del bullet[bulletName]
            continue  

        for enemyName in list(enemy.keys()):
            distance = sqrt((enemy[enemyName]['x'] - bullet[bulletName]['x']) ** 2 + (enemy[enemyName]['y'] - bullet[bulletName]['y']) ** 2)

            if distance < enemy[enemyName]["radius"] + bullet[bulletName]["size"]+2 :
                enemy[enemyName]["hp"] -= bullet[bulletName]["damage"]

                del bullet[bulletName]

                if enemy[enemyName]["hp"] <= 0:
                    del enemy[enemyName]

                break  


#==================================================
#------------------>update
#==================================================
def update():
    global player, enemy, bullet, last_direction, screen_size

    if len(list(enemy.keys())) == 0:
        #x, y, radius, hp, damage
        if player['level'] == 0:
            enemy_spawn(500, 250, 10, 100, 10)
        elif player['level'] == 1:
            enemy_spawn(500, 499, 10, 100, 10)
            enemy_spawn(500, 1, 10, 100, 10)
        elif player['level'] == 2:
            enemy_spawn(500, 250, 20, 400, 40)
        elif player['level'] == 3:
            enemy_spawn(500, 250, 2, 200, 10)
        elif player['level'] == 4:
            for i in range(6):
                enemy_spawn(500,i*100 +1, 10, 100, 10)
        elif player['level'] == 5:
            enemy_spawn(1, 1, 16, 100, 10)
            enemy_spawn(1, 500, 16, 100, 10)
            enemy_spawn(500, 500, 16, 100, 10)
            enemy_spawn(500, 1, 16, 100, 10)
        elif player['level'] == 6:
            enemy_spawn(500, 250, 25, 500, 100)
        elif player['level'] == 7:
            for i in range(3):
                for j in range(3):
                    if j !=1 or i != 1:
                        enemy_spawn(250*i, 250*j, 16, 100, 10)
        elif player['level'] == 8:
            enemy_spawn(500, 250, 1, 200, 100)
        elif player['level'] == 9:
            enemy_spawn(600, 250, 10, 10000, 999)
        player['level'] += 1

    #player direction
    move_x,move_y = direction_axe()
    
    newIndex = int(player["inventory"].index(player["main_weapon"]) + int(pyxel.mouse_wheel))
    if newIndex < 0:
        newIndex = len(player["inventory"])-1
    elif newIndex > len(player["inventory"])-1:
        newIndex = 0

    player["main_weapon"] = player["inventory"][newIndex]

    #player  move
    player['x'] += move_x * 3
    player['y'] += move_y * 3

    #containe player on windows border
    player['x'] = max(0, min(player['x'], screen_size[0] - player['size']))
    player['y'] = max(28, min(player['y'], screen_size[1] - player['size']))

    #hp +
    if 0 < player["hp"] < 100:
        player["hp"] += 0.1
    if 50 > player["hp"]:
        player["hp"] += 50

    #abandoned function
    shoot_player()

    update_bullet()

    update_enemy()
    

#==================================================
#------------------>draw
#==================================================
def draw():
    """Draws all game elements on the screen."""
    pyxel.cls(0)

    weapons = ["pixel_l", "duplicator","Bit_Ray","Code_trapper",0]
    
    
    if player["hp"] > 0:
        
        #background pictur
        pyxel.load("room.pyxres")
        pyxel.blt(0,0,0,0,0,256,256)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): #mouse
            pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 5, 5, 8)
        else:
            pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 5, 5, 10)
        # Draw player
        pyxel.rect(player['x'], player['y'], player['size'], player['size'], 7)

        
        # Draw enemy
        for name in enemy.keys():
            pyxel.circ(enemy[name]['x'], enemy[name]['y'], enemy[name]['radius'], 8)

        # Draw bulletdddd
        for name in bullet.keys():
            pyxel.rect(bullet[name]['x'], bullet[name]['y'], bullet[name]['size'], bullet[name]['size'], 7)

        # Draw reload bar for reload
        bar_width = int((player["reload"] / 100) * 100)
        if player["reload"] < 10:
            pyxel.rect(10, 245, bar_width, 5, 8)  
        elif player["reload"] < 100:
            pyxel.rect(10, 245, bar_width, 5, 7)  
        else:
            pyxel.rect(10, 245, bar_width, 5, 2) 
        pyxel.rectb(10, 245, 100, 5, 9)

        # Draw reload bar for player's HP
        bar_width = int((player["hp"] / 100) * 100)
        if player["hp"] < 10:
            pyxel.rect(10, 250, bar_width, 5, 8) 
        elif player["hp"] < 100:
            pyxel.rect(10, 250, bar_width, 5, 7)  
        else:
            pyxel.rect(10, 250, bar_width, 5, 2)  
        pyxel.rectb(10, 250, 100, 5, 9)

        #display current level
        pyxel.text(114, 30, f'''level {player["level"]}''', 7)


        pyxel.load("icon.pyxres")
        for i, weapon in enumerate(weapons):
            if weapon == player["main_weapon"]:
                pyxel.rectb(145+22*i, 233, 22, 22, 1)
            if weapon in player["inventory"]:
                pyxel.blt(146+22*i,234,0,20*i,0,20,20)
            else:
                pyxel.blt(146+22*i,234,0,40,20,20,20)


    else:
        xs = cos(time() * 10) * 10
        ys = sin(time() * 10) * 10
        for i in range(11):
            for j in range(11):
                pyxel.text(i * 50 + xs, j * 50 + ys, 'GAME OVER', 8)

# Initialisation de Pyxel
pyxel.init(screen_size[0], screen_size[1])

#load backgroud picture


pyxel.load("icon.pyxres")

# Lancement du jeu
pyxel.run(update, draw)