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

#variable for weapon amelioration
pixelLuncher = {'damage' : 5, 'reloadTime' : 20}
glitchImpact = {'damage' : 2, 'reloadTime' : 15}
bitRay = {'damage' : 1, 'reloadTime' : 2}
codeTraper = {'damage' : 5, 'reloadTime' : 50}


#==================================================
#------------------>function
#==================================================


def enemy_spawn(x, y, radius, hp, damage):
    global enemy, player
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
    return (pyxel.btn(pyxel.KEY_Q) - pyxel.btn(pyxel.KEY_D), pyxel.btn(pyxel.KEY_Z) - pyxel.btn(pyxel.KEY_S))

#________________________weapon________________________
def shoot_player():
    #use weapon according to the main one
    if player["main_weapon"] == "pixel_l":
        pixel_l(player)
    elif player["main_weapon"] == "duplicator":
        duplicator(player)
    elif player["main_weapon"] == "Bit_Ray":
        Bit_Ray(player)
    elif player["main_weapon"] == "code_trapper":
        Code_trapper(player)
    elif player["main_weapon"] == "glitch_impact":
        glitch_impact(player)


#fonction for all the weapon

#pixel lunxher
def pixel_l(player):
    
    #verifie key and reload to soot
    if player["reload"] >= 20 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  # reload time

        #defined the dirrection of the bullet
        dx =pyxel.mouse_x-123 - player['size'] / 2 
        dy =pyxel.mouse_y-123 - player['size'] / 2 
        angle = atan2(dy, dx)
        vx=cos(angle)
        vy=sin(angle)

        #defined the spawn position of the bullet
        bullet_x = 123 + player['size'] / 2 
        bullet_y = 123 + player['size'] / 2 

        bullet_spawn(bullet_x, bullet_y, 8, [vx * 5, vy * 5],pixelLuncher['damage'])
        player["reload"] -= pixelLuncher['reloadTime']


def glitch_impact(player):

    #verifie key and reload to soot
    if player["reload"] >= glitchImpact['reloadTime'] and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  # reload time

        # difined only diraction of the bullet because bullet spawn position is cursor 
        dx =pyxel.mouse_x-123 - player['size'] / 2 
        dy =pyxel.mouse_y-123 - player['size'] / 2 
        angle = atan2(dy, dx)
        for i in range(5):
            r = random()*100
            vx=cos(angle+r)
            vy=sin(angle+r)

            bullet_spawn(pyxel.mouse_x, pyxel.mouse_y, 3, [vx * 10, vy * 10], glitchImpact['damage'])
        player["reload"] -= glitchImpact['reloadTime']  
    

def duplicator(player):
    """Shoots a projectile in the last recorded direction if the space bar is pressed."""

    #verifie key and reload to soot
    if player["reload"] >= 30 and pyxel.btnp(pyxel.KEY_SPACE):  # reload time
        size = player['size'] # bullet size
        damage = (player["reload"]/100)*player['hp']
        vx, vy = last_direction  # use the last direction of the player
        
        #defined bullet spawn position
        bullet_x = 123 + player['size'] / 2 - size/2
        bullet_y = 123 + player['size'] / 2 - size/2

        bullet_spawn(bullet_x, bullet_y, size, [vx * 5, vy * 5], damage)
        player["reload"] -= 30


def Bit_Ray(player):
   
    #verifie key and reload to soot
    if player["reload"] >= bitRay['reloadTime'] and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) == 1:  # reload time
        
        #difined bullet dirrection 
        dx =pyxel.mouse_x-123 - player['size'] / 2 
        dy =pyxel.mouse_y-123 - player['size'] / 2 
        angle = atan2(dy, dx)
        vx=cos(angle)
        vy=sin(angle)
        
        #difined bullet spawn position
        for i in range(1):
            bullet_x = 123 + (player['size']*random())
            bullet_y = 123 + (player['size']*random())
            bullet_spawn(bullet_x, bullet_y, 2, [vx * 20, vy *20], bitRay['damage'])
        player["reload"] -= bitRay['reloadTime']



def Code_trapper(player):
    
    #verifie key and reload to soot
    if player["reload"] >= codeTraper['reloadTime'] and pyxel.btnp(pyxel.KEY_SPACE):  # reload time
        size = 4
        damage = codeTraper['damage']

        #make bullet whith no direction in function of player size
        #those three for loop are for the eitgh bullet around
        for i in range((player["size"]//8)+1):
            bullet_x = 123 + i*8 - size/2 
            bullet_y = 123 + player['size'] - size/2
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage)
        for i in range((player["size"]//8)+1):
            bullet_x = 123 + i*8 - size/2 
            bullet_y = 123 - size/2
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage)
        for i in range((player["size"]//8)-1):
            bullet_x = 123 - size/2 
            bullet_y = 123 - size/2 + (i+1)*8
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage)
        for i in range((player["size"]//8)-1):
            bullet_x = 123 - size/2 + player['size']
            bullet_y = 123 - size/2 + (i+1)*8
            bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage)
        
        #then we make the big center one
        size = player['size'] / 2
        bullet_x = 123 + player['size'] / 2 - size/2
        bullet_y = 123 + player['size'] / 2 - size/2
        bullet_spawn(bullet_x, bullet_y, size, [0, 0], damage*2)

        
        
        player["reload"] -= codeTraper['reloadTime']

#________________________enemy update________________________
def update_enemy():
    global enemy, player, dialogueBox
    if not "tick" in player:
        player["tick"] = 0
    player["tick"] +=1

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
        vec_x = (123 + player['size'] / 2) - enemy[name]['x']
        vec_y = (123 + player['size'] / 2) - enemy[name]['y']
        norm = sqrt(vec_x ** 2 + vec_y ** 2)
        

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
        
        if enemy[name]['x'] > 255 + enemy[name]['radius'] + 10 or enemy[name]['y'] > 255 + enemy[name]['radius'] + 10 or enemy[name]['y'] < 0 - enemy[name]['radius'] - 10 or enemy[name]['x'] < 0 - enemy[name]['radius'] - 10:
            enemy[name]['x'] += int(round(vec_x / norm))
            enemy[name]['y'] += int(round(vec_y / norm))

#________________________bullet update________________________
def update_bullet():
    global bullet, enemy, screen_size
    for bulletName in list(bullet.keys()):
        bullet[bulletName]['x'] += bullet[bulletName]['direction'][0] + direction_axe()[0] *3
        bullet[bulletName]['y'] += bullet[bulletName]['direction'][1] + direction_axe()[1] *3

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
    global player, enemy, bullet, last_direction, screen_size, scene, dialogueBox, pixelLuncher, codeTraper, bitRay, glitchImpact

    #close dialogue bose withe return key
    if dialogueBox != 0:
        if pyxel.btnp(pyxel.KEY_RETURN):
            dialogueBox = 0
    
    elif scene == "menu":
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #make action because of the position of mouse click (button zone)
            if 100 < pyxel.mouse_x < 160 and 100< pyxel.mouse_y < 120:

                #pass to arena scene
                scene = "arena"
                
                #init all var
                enemy = {}
                bullet = {}
                player['hp'] = 100
                player['level'] = 0
                player['inventory'] = ["pixel_l"]
                player["main_weapon"] = "pixel_l"
                pixelLuncher = {'damage' : 10, 'reloadTime' : 30}
                glitchImpact = {'damage' : 2, 'reloadTime' : 15}
                codeTraper = {'damage' : 3, 'reloadTime' : 50}
                bitRay = {'damage' : 4, 'reloadTime' : 2}

                #init the second dialogue box
                dialogueBox = 2
            

            elif 100 < pyxel.mouse_x < 160 and 145< pyxel.mouse_y < 160:
                pyxel.quit()

    elif scene == "arena":

        #this id all the game level( enemy spaxn and weapon update)
        if len(list(enemy.keys())) == 0:
            #x, y, radius, hp, damage

            if player['level'] == 0:
                enemy_spawn(500, 128, 10, 100, 10)

            elif player['level'] == 1:
                dialogueBox = 3
                player['inventory'].append("glitch_impact")

                enemy_spawn(500, 128, 10, 100, 10)
                enemy_spawn(-250, 128, 10, 100, 10)

            elif player['level'] == 2:
                dialogueBox = 4
                pixelLuncher['damage'] = 20

                enemy_spawn(500, 128, 15, 200, 20)

            elif player['level'] == 3:
                dialogueBox = 5
                player['inventory'].append("code_trapper")

                enemy_spawn(500, 128, 10, 100, 10)
                enemy_spawn(-250, -250, 10, 100, 10)
                enemy_spawn(500, 500, 10, 100, 10)

            elif player['level'] == 4:
                dialogueBox = 6
                glitchImpact['damage'] = 3

                enemy_spawn(500,128, 20, 300, 35)

            elif player['level'] == 5:
                dialogueBox = 4
                pixelLuncher["damage"] = 30

                enemy_spawn(-250, -250, 16, 100, 10)
                enemy_spawn(-250, 500, 16, 100, 10)
                enemy_spawn(500, 500, 16, 100, 10)
                enemy_spawn(500, -250, 16, 100, 10)

            elif player['level'] == 6:
                dialogueBox = 7
                player['inventory'].append("Bit_Ray")

                enemy_spawn(500, 128, 25, 500, 40)

            elif player['level'] == 7:
                dialogueBox = 4
                pixelLuncher["damage"] = 25
                pixelLuncher["reloadTime"] = 15
                
                enemy_spawn(-250,-250,10,100,15)
                enemy_spawn(180,-250,10,100,15)
                enemy_spawn(500,128,10,100,15)
                enemy_spawn(180,500,10,100,15)
                enemy_spawn(-250,500,10,100,15)
            
            elif player['level'] == 8:
                dialogueBox = 8
                codeTraper['damage'] = 5
                for x in range(5):
                    for y in range(2):
                        enemy_spawn(150*x-250,y*750-250,8,50,5)
                enemy_spawn(-250,128,8,50,5)
            
            elif player['level'] == 9:
                dialogueBox = 6
                glitchImpact['damage'] = 5

                for x in range(2):
                    for y in range(2):
                        enemy_spawn(x*750-250,y*750-250,8,50,5)

            elif player['level'] == 10:
                dialogueBox = 9
                player['inventory'].append("duplicator")

                for x in range(5):
                    for y in range(2):
                        enemy_spawn(150*x-250,y*750-250,10,100,7)

            elif player['level'] == 11:
                dialogueBox = 8
                codeTraper['damage'] = 10

                enemy_spawn(-250,-250,10,200,15)
                enemy_spawn(180,-250,10,200,15)
                enemy_spawn(500,128,10,200,15)
                enemy_spawn(180,500,10,200,15)
                enemy_spawn(-250,500,10,200,15)
            
            elif player['level'] == 12:
                dialogueBox = 4
                pixelLuncher['damage'] = 50

                enemy_spawn(-250,-250,30,1000,70)
            
            elif player['level'] == 13:
                dialogueBox = 10
                bitRay['damage'] = 8

                for x in range(5):
                    for y in range(2):
                        enemy_spawn(150*x-250,y*750-250,10,100,8)
                enemy_spawn(-250,128,10,100,9)

            elif player['level'] == 14:
                dialogueBox = 10
                glitchImpact['damage'] = 10

                for x in range(3):
                    for y in range(2):
                        enemy_spawn(250*x-250,y*750-250,15,200,15)
            
            elif player['level'] == 15:
                dialogueBox = 11

                enemy_spawn(500,128,50,3000,80)

            player['level'] += 1

        #player direction
        move_x,move_y = direction_axe()
        if move_x != 0 or move_y != 0:
            last_direction = [-move_x,-move_y]
        
        #use scorl to cange weapon and replace index in the list limite
        newIndex = int(player["inventory"].index(player["main_weapon"]) + int(pyxel.mouse_wheel))
        if newIndex < 0:
            newIndex = len(player["inventory"])-1
        elif newIndex > len(player["inventory"])-1:
            newIndex = 0

        player["main_weapon"] = player["inventory"][newIndex]

        #player  move
        player['x'] += move_x * 3
        player['y'] += move_y * 3

        #make the player position return to zero when reach 256 and vice-versa
        if player["x"] < 0:
            player["x"] = 255
        player["x"] %= 256

        if player["y"] < 0:
            player["y"] = 255
        player["y"] %= 256
        
        #reload +
        if player["reload"] < 100:
            player["reload"] += 1

        #hp +
        if 0 < player["hp"] < 100:
            player["hp"] += 0.2

        #weapon
        shoot_player()

        #move bullet
        update_bullet()

        #move enemy
        update_enemy()

        #game over
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
                player["main_weapon"] = "pixel_l"
    
                pixelLuncher = {'damage' : 5, 'reloadTime' : 20}
                bitRay = {'damage' : 1, 'reloadTime' : 2}
                codeTraper = {'damage' : 5, 'reloadTime' : 50}
                scene = "arena"
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

    #reset screen
    pyxel.cls(0)

    #all the weapon in game
    weapons = [ "pixel_l", "glitch_impact", "code_trapper", "Bit_Ray", "duplicator"]
    
    #draw the menu
    if scene == "menu":
        pyxel.blt(0,0,2,0,0,256,256)


    elif player["hp"] > 0 and scene == "arena":
        
        #draw arena in bacground (this is the backgroud who move not the player)
        for x in range(3):
            for y in range(3):
                pyxel.blt((player["x"] + (x * 256) - 256),(player["y"] + (y* 256) - 256),1,0,0,256,256)
        
        # Draw player
        pyxel.rect(123, 123, player['size'], player['size'], 7)

        
        # Draw enemy
        for name in enemy.keys():
            pyxel.circ(enemy[name]['x'], enemy[name]['y'], enemy[name]['radius'], 8)

        # Draw bullet
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

        #draw inventory bar
        for i, weapon in enumerate(weapons):
            if weapon == player["main_weapon"]:
                pyxel.rectb(145+22*i, 233, 22, 22, 1)
            if weapon in player["inventory"]:
                pyxel.blt(146+22*i,234,0,20*i,0,20,20)
            else:
                #draw padlock
                pyxel.blt(146+22*i,234,0,100,0,20,20)

    #draw game over menu
    elif scene == "game_over":
        pyxel.blt(0,0,2,0,0,256,256)
    
    #draw the dialogue box for all the situation because of dialogueBox var
    if dialogueBox == 1:
        dialogue("project x", "vous etes un resitant carré qui se bat contre les envaisseurs cercles. au fur de votre aventure voud débloquerais des armes et armure. utiliser ZQSD pour ce déplacer. Information : la taille des enemies correspond a ses point de vie.")
    if dialogueBox == 2:
        dialogue("Nouveau", "vous avez deploquer le lance pixel. Appuyer sur le clique gauche de la souris pour tirrer", [0,0], pixelLuncher)
    if dialogueBox == 3:
        dialogue("Nouveau", "Vous avez debloquer le glitch impact. Appuyer sur le clique droit de la souris pour declancher l'explotion", [20,0], glitchImpact)
    if dialogueBox == 4:
        dialogue("Evolution", "Votre lance pixel a evolue", [0,0], pixelLuncher)
    if dialogueBox == 5:
        dialogue("Nouveau", "Vous avez debloqué le code trapper. Appuyer sur espace pour poser un piège", [40,0], codeTraper)
    if dialogueBox == 6:
        dialogue("Evolution", "Votre glitch impact a évolue", [20,0], glitchImpact)
    if dialogueBox == 7:
        dialogue("Nouveau", "Vous avez debloquer le bitRay, rester appuyer pour envoyer un deluge de balle", [60,0], bitRay)
    if dialogueBox == 8:
        dialogue("Evolution", "Votre code trapper a evolue", [40,0], codeTraper)
    if dialogueBox == 9:
        dialogue("Nouveau", "Vous avez debloquer le duplicator. Appuyer sur espace pour lancer un clone de vous dans votre direction", [80,0], {"damage":"point de vie", "relaodTime":30})
    if dialogueBox == 10:
        dialogue("Evolution", "Votre bit ray a evoluer", [60,0], bitRay)
    if dialogueBox == 11:
        dialogue("Atention", "Le roi des cercle est aparue pour vous terrasser. Il possède 3000 point de vie. faite très atention a vous et bonne chance")

    #draw mouse cursor
    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT): #mouse
        pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 5, 5, 8)
    else:
        pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 5, 5, 10)

# Initialisation de Pyxel
pyxel.init(screen_size[0], screen_size[1])

#load all image
pyxel.load(".\\resource.pyxres")
pyxel.image(1).load(0 , 0 ,".\\arena.png")
pyxel.image(2).load(0 , 0 ,".\\menu.png")


#game start
pyxel.run(update, draw)