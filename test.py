import pyxel
from time import time, sleep
from math import sqrt, sin, cos, atan2 ,degrees
from random import random
#==================================================
#------------------>comment
#==================================================

#weapon:duplicator; pixel_l


#==================================================
#------------------>data
#==================================================
enemy = {}
bullet = {}
player = {'x': 50, 'y': 50, 'size': 32, "reload": 100, "hp": 100, "weapon": "duplicator", "level": 1}
last_direction = [1, 0]  # left direction
screen_size = [512,512]


#==================================================
#------------------>function
#==================================================
def enemy_spawn(x, y, radius, hp, damage):
    global enemy
    """Spawns an enemy at a given position with certain radius and health points."""
    enemy[f"enemy{time()}"] = {'x': x, 'y': y, 'radius': radius, "hp": hp, "damage": damage}
    sleep(0.01)

def bullet_spawn(x, y, radius, direction, damage):
    global bullet
    """Spawns a projectile with a certain radius and direction."""
    bullet[f"bullet{time()}"] = {'x': x, 'y': y, 'radius': radius, 'direction': direction, "damage": damage}
    sleep(0.01)

def direction_axe():
    """return variation on x and y axes"""
    return (pyxel.btn(pyxel.KEY_D) - pyxel.btn(pyxel.KEY_Q), pyxel.btn(pyxel.KEY_S) - pyxel.btn(pyxel.KEY_Z))

#________________________weapon________________________
def shoot_player():
    if player["weapon"] == "pixel_l":
        pixel_l(player)
    elif player["weapon"] == "duplicator":
        duplicator(player)
        
    
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

        bullet_spawn(bullet_x, bullet_y, size, [vx * 5, vy * 5],10)
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

        bullet_spawn(bullet_x, bullet_y, 32, [vx * 5, vy * 5], damage)
        player["reload"] = 0
    if player["reload"] < 100:
        player["reload"] += 5
#________________________enemy tick________________________
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

            if distance < enemy[enemyName]["radius"] + bullet[bulletName]["radius"]:
                enemy[enemyName]["hp"] -= bullet[bulletName]["damage"]

                del bullet[bulletName]

                if enemy[enemyName]["hp"] <= 0:
                    del enemy[enemyName]

                break  

#==================================================
#------------------>tick
#==================================================
def update():
    global player, enemy, bullet, last_direction, screen_size

    if len(list(enemy.keys())) == 0:
        #x, y, radius, hp, damage
        if player['level'] == 0:
            enemy_spawn(500, 250, 20, 100, 0)
        elif player['level'] == 1:
            enemy_spawn(500, 499, 20, 100, 10)
            enemy_spawn(500, 1, 20, 100, 10)
        elif player['level'] == 2:
            enemy_spawn(500, 250, 40, 400, 40)
        elif player['level'] == 3:
            enemy_spawn(500, 250, 2, 200, 10)
        elif player['level'] == 4:
            for i in range(6):
                enemy_spawn(500,i*100 +1, 20, 100, 10)
        elif player['level'] == 5:
            enemy_spawn(1, 1, 32, 100, 10)
            enemy_spawn(1, 500, 32, 100, 10)
            enemy_spawn(500, 500, 32, 100, 10)
            enemy_spawn(500, 1, 32, 100, 10)
        elif player['level'] == 6:
            enemy_spawn(500, 250, 50, 500, 100)
        elif player['level'] == 7:
            for i in range(3):
                for j in range(3):
                    if j !=1 or i != 1:
                        enemy_spawn(250*i, 250*j, 32, 100, 10)
        elif player['level'] == 8:
            enemy_spawn(500, 250, 1, 200, 100)
        elif player['level'] == 9:
            enemy_spawn(600, 200, 300, 10000, 999)
        player['level'] += 1

    #player direction
    move_x,move_y = direction_axe()
    

    #player  move
    player['x'] += move_x * 3
    player['y'] += move_y * 3

    #save dirrection for the weapon
    if move_x != 0 or move_y != 0:
        last_direction = [move_x, move_y]

    #containe player on windows border
    player['x'] = max(0, min(player['x'], screen_size[0] - player['size']))
    player['y'] = max(0, min(player['y'], screen_size[1] - player['size']))

    #reload +
    
    #hp +
    if 0 < player["hp"] < 100:
        player["hp"] += 0.1

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
    
    if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)): #mouse
        pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 5, 5, 8)
    else:
        pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 5, 5, 10)
    
    pyxel.rect(player['x'] + player['size'] / 2 , player['y'] + player['size'] / 2 , 2, 2, 1)
    if player["hp"] > 0:
        # Draw player
        pyxel.rect(player['x'], player['y'], player['size'], player['size'], 7)

        # Draw enemy
        for name in enemy.keys():
            pyxel.circ(enemy[name]['x'], enemy[name]['y'], enemy[name]['radius'], 8)

        # Draw bullet
        for name in bullet.keys():
            pyxel.rect(bullet[name]['x'], bullet[name]['y'], bullet[name]['radius'], bullet[name]['radius'], 7)

        # Draw reload bar for reload
        bar_width = int((player["reload"] / 100) * 100)  
        if player["reload"] < 10:
            pyxel.rect(10, 490, bar_width, 5, 8)  
        elif player["reload"] < 100:
            pyxel.rect(10, 490, bar_width, 5, 7)  
        else:
            pyxel.rect(10, 490, bar_width, 5, 11) 
        pyxel.rectb(10, 490, 100, 5, 1)  

        # Draw reload bar for player's HP
        bar_width = int((player["hp"] / 100) * 100)
        if player["hp"] < 10:
            pyxel.rect(10, 500, bar_width, 5, 8) 
        elif player["hp"] < 100:
            pyxel.rect(10, 500, bar_width, 5, 7)  
        else:
            pyxel.rect(10, 500, bar_width, 5, 11)  
        pyxel.rectb(10, 500, 100, 5, 1) 

        #display current level
        pyxel.text(200, 50, f'level {player['level']}', 7)
    else:
        xs = cos(time() * 10) * 10
        ys = sin(time() * 10) * 10
        for i in range(11):
            for j in range(11):
                pyxel.text(i * 50 + xs, j * 50 + ys, 'GAME OVER', 8)
        

# Initialisation de Pyxel
pyxel.init(screen_size[0], screen_size[1])

# Lancement du jeu
pyxel.run(update, draw)
