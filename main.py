import pyxel
from time import time, sleep
from math import sqrt, sin, cos
from random import random

# init global variable
enemy = {}
bullet = {}
player = {'x': 50, 'y': 50, 'size': 16, "reload": 100, "hp": 100, "weapon": "pixel_l", "level": 0}
last_direction = [1, 0]  # left direction
screen_size = [256,256]

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
    global player
    """Shoots a projectile in the last recorded direction if the space bar is pressed."""
    if player["reload"] >= 10 and pyxel.btnp(pyxel.KEY_SPACE):  # reload time
        size = sqrt(player["reload"]) / 2  # bullet size
        vx, vy = last_direction  # use the last direction of the player

        bullet_x = player['x'] + player['size'] / 2 - size
        bullet_y = player['y'] + player['size'] / 2 - size

        bullet_spawn(bullet_x, bullet_y, size, [vx * 5, vy * 5], player["reload"])
        player["reload"] = 0  # reset reload

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

#________________________bullet tick________________________
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

#________________________tick_______________________________________
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
    if player["reload"] < 100:
        player["reload"] += 1
    #hp +
    if 0 < player["hp"] < 100:
        player["hp"] += 0.1

    #abandoned function
    shoot_player()

    update_bullet()

    update_enemy()
    

#________________________draw________________________
def draw():
    """Draws all game elements on the screen."""
    pyxel.cls(0)

    #background pictur
    pyxel.blt(0,0,0,0,0,256,256)
    
    if player["hp"] > 0:
        # Draw player
        pyxel.rect(player['x'], player['y'], player['size'], player['size'], 7)

        # Draw enemy
        for name in enemy.keys():
            pyxel.circ(enemy[name]['x'], enemy[name]['y'], enemy[name]['radius'], 8)

        # Draw bullet
        for name in bullet.keys():
            size = bullet[name]['radius'] * 2  
            pyxel.rect(bullet[name]['x'], bullet[name]['y'], size, size, 7)

        # Draw reload bar for reload
        bar_width = int((player["reload"] / 100) * 100)  
        if player["reload"] < 10:
            pyxel.rect(10, 245, bar_width, 5, 8)  
        elif player["reload"] < 100:
            pyxel.rect(10, 245, bar_width, 5, 7)  
        else:
            pyxel.rect(10, 245, bar_width, 5, 11) 
        pyxel.rectb(10, 245, 100, 5, 1)  

        # Draw reload bar for player's HP
        bar_width = int((player["hp"] / 100) * 100)
        if player["hp"] < 10:
            pyxel.rect(10, 250, bar_width, 5, 8) 
        elif player["hp"] < 100:
            pyxel.rect(10, 250, bar_width, 5, 7)  
        else:
            pyxel.rect(10, 250, bar_width, 5, 11)  
        pyxel.rectb(10, 250, 100, 5, 1) 

        #display current level
        pyxel.text(125, 10, f'''level {player["level"]}''', 7)

    else:
        xs = cos(time() * 10) * 10
        ys = sin(time() * 10) * 10
        for i in range(11):
            for j in range(11):
                pyxel.text(i * 50 + xs, j * 50 + ys, 'GAME OVER', 8)

# Initialisation de Pyxel
pyxel.init(screen_size[0], screen_size[1])

#load backgroud pictur
pyxel.load("room.pyxres")

# Lancement du jeu
pyxel.run(update, draw)