import pyxel
from time import time, sleep
from math import sqrt, sin, cos, atan2
from random import random

#==================================================
#------------------>comment
#==================================================

#weapon:duplicator; pixel_l;Bit_Ray;Code_trapper



#==================================================
#------------------>data
#==================================================


enemy = {}
bullet = {}
player = {'x': 0, 'y': 0, 'size': 16, "reload": 100, "hp": 100, 'totalHP' : 100, "main_weapon": "pixel_l", "inventory": ["pixel_l"], "level": 0}
last_direction = [1, 0]  # left direction
screen_size = [256,256]
scene = "menu"
dialogueBox = 1


pixelLuncher = {'damage' : 5, 'reloadTime' : 20}
bitRay = {'damage' : 1, 'reloadTime' : 2}
codeTraper = {'damage' : 5, 'reloadTime' : 50}


#==================================================
#------------------>function
#==================================================
<<<<<<< HEAD
def enemy_spawn(x, y, radius, hp, damage):
    global enemy, player
    if player['level'] == 9:
    
        enemy[f"enemy{time()}"] = {'x': x, 'y': y, 'radius': radius, "hp": hp, "damage": damage, 
        "boss" : True}

    else:
        """Spawns an enemy at a given position with certain radius and health points."""
        enemy[f"enemy{time()}"] = {'x': x, 'y': y, 'radius': radius, "hp": hp, "damage": damage}
        sleep(0.01)
=======
def enemy_spawn(x, y, radius, hp, damage, weapon):
    global enemy
    """Spawns an enemy at a given position with certain radius and health points."""
    enemy[f"enemy{time()}"] = {'x': x, 'y': y, 'radius': radius, "hp": hp, "damage": damage, 'weapon' : weapon}
    if weapon == 'range':
        enemy[list(enemy.keys())[-1]]['reload'] = 20
    sleep(0.01)
>>>>>>> de8363e5fe4ec4b5cf53a3f478ef673e6c16a33f

def bullet_spawn(x, y, size, direction, damage, playerDamage):
    global bullet
    """Spawns a projectile with a certain size and direction."""
    bullet[f"bullet{time()}"] = {'x': x, 'y': y, 'size': size, 'direction': direction, "damage": damage , 'playerDamage': playerDamage}
    sleep(0.01)

def direction_axe():
    """return variation on x and y axes"""
    return (pyxel.btn(pyxel.KEY_Q) - pyxel.btn(pyxel.KEY_D), pyxel.btn(pyxel.KEY_Z) - pyxel.btn(pyxel.KEY_S))

#________________________weapon________________________
def shoot_player():
    """if player["main_weapon"] == "pixel_l":
        pixel_l(player)
    elif player["main_weapon"] == "duplicator":
        duplicator(player)
    elif player["main_weapon"] == "Bit_Ray":
        Bit_Ray(player)
    elif player["main_weapon"] == "Code_trapper":
        Code_trapper(player)"""
    glitch_impact(player)


def pixel_l(player):
    
    if player["reload"] >= 20 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  # reload time
        size = 8  # bullet size
        dx =pyxel.mouse_x-123 - player['size'] / 2 
        dy =pyxel.mouse_y-123 - player['size'] / 2 
        angle = atan2(dy, dx)
        vx=cos(angle)
        vy=sin(angle)

        bullet_x = 123 + player['size'] / 2 
        bullet_y = 123 + player['size'] / 2 

        bullet_spawn(bullet_x, bullet_y, size, [vx * 5, vy * 5],pixelLuncher['damage'] , False)
        player["reload"] -= pixelLuncher['reloadTime']  
    
    if player["reload"] < 100:
        player["reload"] += 1


def glitch_impact(player):
    if player["reload"] >= 20 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  # reload time
        size = 8  # bullet size
        dx =pyxel.mouse_x-123 - player['size'] / 2 
        dy =pyxel.mouse_y-123 - player['size'] / 2 
        angle = atan2(dy, dx)
        for i in range(5):
            angle = atan2(dy, dx)
            r = random()*100
            vx=cos(angle+r)
            vy=sin(angle+r)

            bullet_spawn(pyxel.mouse_x, pyxel.mouse_y, 3, [vx * 10, vy * 10],20)
        player["reload"] -= 20  
    
    if player["reload"] < 100:
        player["reload"] += 1

def duplicator(player):
    """Shoots a projectile in the last recorded direction if the space bar is pressed."""
    if player["reload"] >= 100 and pyxel.btnp(pyxel.KEY_SPACE):  # reload time
        size = player['size'] # bullet size
        damage = (player["reload"]/100)*player['hp']
        vx, vy = last_direction  # use the last direction of the player
            
        bullet_x = 123 + player['size'] / 2 - size/2
        bullet_y = 123 + player['size'] / 2 - size/2

        bullet_spawn(bullet_x, bullet_y, size, [vx * 5, vy * 5], damage, False)
        player["reload"] = 0
    if player["reload"] < 100:
        player["reload"] += 1


def Bit_Ray(player):
   
    if player["reload"] >= 1 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) == 1:  
        
        dx =pyxel.mouse_x-123 - player['size'] / 2 
        dy =pyxel.mouse_y-123 - player['size'] / 2 
        angle = atan2(dy, dx)
        vx=cos(angle)
        vy=sin(angle)
        size = 2
        
        for i in range(1):
            bullet_x = 123 + (player['size']*random())
            bullet_y = 123 + (player['size']*random())
            bullet_spawn(bullet_x, bullet_y, 2, [vx * 20, vy *20], bitRay['damage'], False)
        player["reload"] -= bitRay['reloadTime']
    elif player["reload"] < 100:
        player["reload"] += 1



def Code_trapper(player):
    if player["reload"] >= 50 and pyxel.btnp(pyxel.KEY_SPACE):  # reload time
        size = 4
        damage = codeTraper['damage']

        for i in range((player["size"]//8)+1):
            bullet_x = 123 + i*8 - size/2 
            bullet_y = 123 + player['size'] - size/2
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage, False)
        for i in range((player["size"]//8)+1):
            bullet_x = 123 + i*8 - size/2 
            bullet_y = 123 - size/2
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage, False)
        for i in range((player["size"]//8)-1):
            bullet_x = 123 - size/2 
            bullet_y = 123 - size/2 + (i+1)*8
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage, False)
        for i in range((player["size"]//8)-1):
            bullet_x = 123 - size/2 + player['size']
            bullet_y = 123 - size/2 + (i+1)*8
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage, False)
        
        size = player['size'] / 2
        bullet_x = 123 + player['size'] / 2 - size/2
        bullet_y = 123 + player['size'] / 2 - size/2
        bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage*2, False)

        
        
        player["reload"] -= codeTraper['reloadTime']
    if player["reload"] < 100:
        player["reload"] += 0.5

#________________________enemy update________________________
def update_enemy():
    global enemy, player, dialogueBox
    if not "tick" in player:
        player["tick"] = 0
    player["tick"] +=1

    for name in enemy.keys():
        if "boss" in name and player["tick"]%100 == 0:
            enemy_spawn(enemy[name]['x'], enemy[name]['y'], 1, 1, 10)

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
        vec_x = (123 + player['size'] / 2) - enemy[name]['x']
        vec_y = (123 + player['size'] / 2) - enemy[name]['y']
        norm = sqrt(vec_x ** 2 + vec_y ** 2)
        
        if enemy[name]['weapon'] == 'melee':
            #colition with player
            if norm < enemy[name]['radius'] + player['size'] / 2:
                enemy[name]['x'] -= int(round(vec_x / norm))  * 3
                enemy[name]['y'] -= int(round(vec_y / norm)) * 3
                player['x'] -= int(round(vec_x / norm)) * 3  # Collision reaction
                player['y'] -= int(round(vec_y / norm)) * 3
                player['hp'] -= enemy[name]['damage']
            #normal action
            elif norm > 0:
                enemy[name]['x'] += int(round(vec_x / norm)) * 2 + direction_axe()[0] *3
                enemy[name]['y'] += int(round(vec_y / norm)) * 2 + direction_axe()[1] *3
            
        elif enemy[name]['weapon'] == 'range':
            if norm < 100:
                if enemy[name]['reload'] >= 20:
                    bullet_spawn(enemy[name]['x'], enemy[name]['y'], 8, [ int(round(vec_x / norm))*5 , int(round(vec_y / norm))*5 ], enemy[name]['damage'], True)
                    enemy[name]['reload'] -= 20
            else:
                enemy[name]['x'] += int(round(vec_x / norm)) * 2 + direction_axe()[0] *3
                enemy[name]['y'] += int(round(vec_y / norm)) * 2 + direction_axe()[1] *3
            
            if enemy[name]['reload'] < 20:
                enemy[name]['reload'] += 1
        
        if enemy[name]['x'] > 255 + enemy[name]['radius'] + 10 or enemy[name]['y'] > 255 + enemy[name]['radius'] + 10 or enemy[name]['y'] < 0 - enemy[name]['radius'] - 10 or enemy[name]['x'] < 0 - enemy[name]['radius'] - 10:
                enemy[name]['x'] += int(round(vec_x / norm))
                enemy[name]['y'] += int(round(vec_y / norm))


#________________________bullet update________________________
def update_bullet():
    global bullet, enemy, screen_size, player
    for bulletName in list(bullet.keys()):
        bullet[bulletName]['x'] += bullet[bulletName]['direction'][0] + direction_axe()[0] *3
        bullet[bulletName]['y'] += bullet[bulletName]['direction'][1] + direction_axe()[1] *3

        # delete bullet outside the screen
        if not (0 <= bullet[bulletName]['x'] <= screen_size[0] and 0 <= bullet[bulletName]['y'] <= screen_size[1]):
            del bullet[bulletName]
            continue  
        
        if bullet[bulletName]['playerDamage'] == False:
            for enemyName in list(enemy.keys()):
                distance = sqrt((enemy[enemyName]['x'] - bullet[bulletName]['x']) ** 2 + (enemy[enemyName]['y'] - bullet[bulletName]['y']) ** 2)

                if distance < enemy[enemyName]["radius"] + bullet[bulletName]["size"]+2:
                    enemy[enemyName]["hp"] -= bullet[bulletName]["damage"]

                    del bullet[bulletName]

                    if enemy[enemyName]["hp"] <= 0:
                        del enemy[enemyName]

                    break
        elif bullet[bulletName]['playerDamage'] == True:
            distance = sqrt((127 - bullet[bulletName]['x']) ** 2 + (127 - bullet[bulletName]['y']) ** 2)
            if distance < player["size"]//2 + bullet[bulletName]["size"]+2:
                    player["hp"] -= bullet[bulletName]["damage"]

                    del bullet[bulletName]

#boite de dialogue
def dialogue(title, text, icon = None, aspects = None):
    pyxel.rect(60,60,134,137,3)
    pyxel.rectb(60,60,134,137,0)
    pyxel.text(127-(len(title)//2)*4, 65, title, 7)

    x = 65
    y = 75

    if icon != None:
        pyxel.blt(117,75,0,icon[0],icon[1],20,20)
        y = 100
    
    text = text.split(" ")

    for mot in text:
        if x + len(mot) > 170:
            x = 65
            y += 8
        pyxel.text(x,y,mot,7)
        x += 4*len(mot) + 3
        
    x = 65
    y += 16
    if aspects != None:
        pyxel.text(x,y,"aspect : ",7)
        for aspect in aspects.keys():
            pyxel.text(x,y,f"{aspect} : {aspects[aspect]}",7)
            y += 8

    pyxel.text(127-(len("presser entre pour fermer")//2)*4,180,"presser entré pour fermer",7)


#==================================================
#------------------>update
#==================================================
def update():
    global player, enemy, bullet, last_direction, screen_size, scene, dialogueBox, pixelLuncher, codeTraper, bitRay

    if dialogueBox != 0:
        if pyxel.btnp(pyxel.KEY_RETURN):
            dialogueBox = 0
    
    elif scene == "menu":
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 100 < pyxel.mouse_x < 160 and 100< pyxel.mouse_y < 120:
                enemy = {}
                bullet = {}
                player['hp'] = 100
                player['level'] = 0
                player['inventory'] = ['pixel_l']
                
                pixelLuncher = {'damage' : 5, 'reloadTime' : 20}
                bitRay = {'damage' : 1, 'reloadTime' : 2}
                codeTraper = {'damage' : 5, 'reloadTime' : 50}
                scene = "room"
                dialogueBox = 2
            
            elif 100 < pyxel.mouse_x < 160 and 145< pyxel.mouse_y < 160:
                pyxel.quit()

    elif scene == "room":
        if len(list(enemy.keys())) == 0:
            #x, y, radius, hp, damage
            if player['level'] == 0:
<<<<<<< HEAD
                dialogueBox = 0
                pixelLuncher = {'damage' : 10, 'reloadTime' : 30}
                
                enemy_spawn(500, 250, 10, 100, 10)
            elif player['level'] == 1:
                dialogue("Nouveau", "Vous avez debloqué le code trapper, appuiyer sur espace pour l'utiliser")
                codeTraper = {'damage' : 5, 'reloadTime' : 50}
                player['inventory'].append("Code_trapper")

                enemy_spawn(500, 499, 10, 100, 10)
                enemy_spawn(500, 1, 10, 100, 10)
            elif player['level'] == 2:
                dialogue("Evolution", "votre lance pixel a evolue")
                pixelLuncher['reloadTime'] = 20 
                
                enemy_spawn(500, 250, 20, 400, 40)
            elif player['level'] == 3:
                dialogue("Evolution", "votre code trapper a evolue")
                codeTraper = {'damage' : 6, 'reloadTime' : 40}
                
                enemy_spawn(500, 250, 2, 200, 10)
=======
                enemy_spawn(500, 250, 10, 100, 10, 'melee')
            elif player['level'] == 1:
                dialogueBox = 3
                pixelLuncher['damage'] = 10
                enemy_spawn(500, 499, 10, 100, 10, 'melee')
                enemy_spawn(500, 1, 10, 100, 10, 'range')
            elif player['level'] == 2:
                dialogueBox = 3
                pixelLuncher['reloadTime'] = 10
                enemy_spawn(500, 250, 20, 400, 40, 'melee')
            elif player['level'] == 3:
                dialogueBox = 3
                pixelLuncher['damage'] = 20
                enemy_spawn(500, 250, 2, 200, 10, 'melee')
>>>>>>> de8363e5fe4ec4b5cf53a3f478ef673e6c16a33f
            elif player['level'] == 4:
                dialogue("Nouveau", "vous avez debloquer le bitRay, presse la souris pour l'active")
                player['inventory'].append("bitRay ")
                bitRay = {'damage' : 1, 'reloadTime' : 2}
                
                for i in range(6):
                    enemy_spawn(500,i*100 +1, 10, 100, 10, 'melee')
            elif player['level'] == 5:
<<<<<<< HEAD
                dialogue("Evolution", "votre lance pixel a evolue")
                pixelLuncher = {'damage' : 10, 'reloadTime' : 10}

                enemy_spawn(1, 1, 16, 100, 10)
                enemy_spawn(1, 500, 16, 100, 10)
                enemy_spawn(500, 500, 16, 100, 10)
                enemy_spawn(500, 1, 16, 100, 10)
            elif player['level'] == 6:
                dialogue("Evolution", "votre code_trapper a evolue")
                codeTraper = {'damage' : 6, 'reloadTime' : 25}


                enemy_spawn(500, 250, 25, 500, 100)
=======
                enemy_spawn(1, 1, 16, 100, 10, 'melee')
                enemy_spawn(1, 500, 16, 100, 10, 'melee')
                enemy_spawn(500, 500, 16, 100, 10, 'melee')
                enemy_spawn(500, 1, 16, 100, 10, 'melee')
            elif player['level'] == 6:
                enemy_spawn(500, 250, 25, 500, 100, 'melee')
>>>>>>> de8363e5fe4ec4b5cf53a3f478ef673e6c16a33f
            elif player['level'] == 7:
                dialogue("Evolution", "votre bit_ray a evolue")
                bitRay = {'damage' : 2, 'reloadTime' : 2}
                for i in range(3):
                    for j in range(3):
                        if j !=1 or i != 1:
<<<<<<< HEAD
                            enemy_spawn(250*i, 250*j, 16, 100, 10)
            
            elif player['level'] == 8:
                dialogue("Evolution", "votre lance pixel a evolue")
                pixelLuncher = {'damage' : 15, 'reloadTime' : 10}

                dialogue("Nouveau", "Vous avez debloquer le duplicator, pressé espace pour l'active")
                player['inventory'].append("duplicator")

                enemy_spawn(500, 250, 1, 200, 100)
            
            elif player['level'] == 9:
                dialogue("Evolution", "votre code_trapper a evolue")
                codeTraper = {'damage' : 10, 'reloadTime' : 25}
                for i in range(50):
                    enemy_spawn(500, i*10, 1, 10, 10)
                enemy_spawn(500, 500, 50, 999, 999)
            elif player['level'] == 9:
                dialogue("???", "Le roi des cercles arrive")
                enemy_spawn(500, 500, 50, 999, 999)

=======
                            enemy_spawn(250*i, 250*j, 16, 100, 10, 'melee')
            elif player['level'] == 8:
                enemy_spawn(500, 250, 1, 200, 100, 'melee')
            elif player['level'] == 9:
                enemy_spawn(600, 250, 10, 10000, 999, 'melee')
>>>>>>> de8363e5fe4ec4b5cf53a3f478ef673e6c16a33f
            player['level'] += 1

        #player direction
        move_x,move_y = direction_axe()
        if move_x != 0 or move_y != 0:
            last_direction = [-move_x,-move_y]
        
        newIndex = int(player["inventory"].index(player["main_weapon"]) + int(pyxel.mouse_wheel))
        if newIndex < 0:
            newIndex = len(player["inventory"])-1
        elif newIndex > len(player["inventory"])-1:
            newIndex = 0

        player["main_weapon"] = player["inventory"][newIndex]

        #player  move
        player['x'] += move_x * 3
        player['y'] += move_y * 3

        if player["x"] < 0:
            player["x"] = 255
        player["x"] %= 256

        if player["y"] < 0:
            player["y"] = 255
        player["y"] %= 256
            
        #hp +
        if 0 < player["hp"] < 100:
            player["hp"] += 0.1
        """if player["hp"] < 50:
            player["hp"] += 50"""

        

        shoot_player()

        update_bullet()

        update_enemy()

        if player["hp"] <= 0:
            scene = "game_over"
            pyxel.image(2).load(0 , 0 ,r".\game_over.png")
    
    elif scene == "game_over":
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 90 < pyxel.mouse_x < 160 and 80< pyxel.mouse_y < 100:
                enemy = {}
                bullet = {}
                player['hp'] = 100
                player['level'] = 0
                player['inventory'] = ['pixel_l']
    
                pixelLuncher = {'damage' : 5, 'reloadTime' : 20}
                bitRay = {'damage' : 1, 'reloadTime' : 2}
                codeTraper = {'damage' : 5, 'reloadTime' : 50}
                scene = "room"
                dialogueBox = 2

            elif 50 < pyxel.mouse_x < 210 and 125< pyxel.mouse_y < 145:
                scene = "menu"
                pyxel.image(2).load(0 , 0 ,r".\menu.png")
            elif 100 < pyxel.mouse_x < 165 and 170 < pyxel.mouse_y < 190:
                pyxel.quit()

    

#==================================================
#------------------>draw
#==================================================
def draw():
    """Draws all game elements on the screen."""
    pyxel.cls(0)

    weapons = ["pixel_l", "duplicator","Bit_Ray","Code_trapper",0]
    
    if scene == "menu":
        pyxel.blt(0,0,2,0,0,256,256)


    elif player["hp"] > 0 and scene == "room":
        
        #background picture
        for x in range(3):
            for y in range(3):
                pyxel.blt((player["x"] + (x * 256) - 256),(player["y"] + (y* 256) - 256),1,0,0,256,256)
        
        # Draw player
        pyxel.rect(123, 123, player['size'], player['size'], 7)

        
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
        bar_width = int((player["hp"] / player['totalHP']) * 100)
        if player["hp"] < 10:
            pyxel.rect(10, 250, bar_width, 5, 8) 
        elif player["hp"] < 100:
            pyxel.rect(10, 250, bar_width, 5, 7)  
        else:
            pyxel.rect(10, 250, bar_width, 5, 2)  
        pyxel.rectb(10, 250, 100, 5, 9)

        #display current level
        pyxel.text(114, 30, f'''level {player["level"]}''', 7)


        for i, weapon in enumerate(weapons):
            if weapon == player["main_weapon"]:
                pyxel.rectb(145+22*i, 233, 22, 22, 1)
            if weapon in player["inventory"]:
                pyxel.blt(146+22*i,234,0,20*i,0,20,20)
            else:
                pyxel.blt(146+22*i,234,0,100,0,20,20)


    elif scene == "game_over":
        pyxel.blt(0,0,2,0,0,256,256)
    
    if dialogueBox == 1:
        dialogue("project x", "vous etes un resitant carré qui se bat contre les envaisseurs cercles. au fur de votre aventure voud débloquerais des armes et armure. utiliser ZQSD pour ce déplacer")
    if dialogueBox == 2:
        dialogue("Nouveau", "vous avez deploquer le lance pixel. Apuyer sur le clique gauche de la souris pour tirrer", [0,0], pixelLuncher)
    if dialogueBox == 3:
        dialogue("Evolution", "votre lance pixel a evolue", [0,0], pixelLuncher)
    if dialogueBox == 0:
        pass
    
    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT): #mouse
        pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 5, 5, 8)
    else:
        pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 5, 5, 10)

# Initialisation de Pyxel
pyxel.init(screen_size[0], screen_size[1])

#load all image
pyxel.load(r".\resource.pyxres")
pyxel.image(1).load(0 , 0 ,r".\room.png")
pyxel.image(2).load(0 , 0 ,r".\menu.png")


# Lancement du jeu
pyxel.run(update, draw)