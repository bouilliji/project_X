#==============================================================================
#---------------------------------->import
#==============================================================================
import pyxel
from time import time, sleep
from math import *
from random import random
#==============================================================================
#---------------------------------->comment
#==============================================================================
"""
weapon:
    duplicator;pixel_pistol;bit_ray;code_trapper;disperser;mini_pix;glitch_impact,laser
armor:
    none,glitch armor
core:
    regular,giant,small,perfect,light,heavy,titan


le x,y du joueur correspondra au centre.

m -> maximal
c -> current
inv ->inventaire
s ->speed

bonus work like this:
[a,b,c]
where :
a -> name of bonus
b -> target data
c -> amount

"""
#==============================================================================
#---------------------------------->data
#==============================================================================
enemy = {} #empty
bullet = {} #empty
weapon = {"reload":0 ,"reload_speed" : 0,"reload_max":1
          ,"refresh":1,"refresh_need":1 
          ,"special":[]}

player = {'x': 0, 'y': 0,'size': 16  #base
        ,"hp":100, "hpm":100,"hps":0.1, #hitpoint
        "speed":2,"damage":20, "defense":1,
         } #and other

player["cw"] = "code_trapper"
player["ca"] = "None"
player["cc"] = "regular"
player["bonus"] = []
player["inventory"] = ["regular","pixel_pistol"]

game = {"scene" : "menu","dialogueBox" : 1,"level":0, "tick":0,
         "camera_x" :0,"camera_y" :0 , "screen_size" : [256,256]
         , "chunk_x":2, "chunk_y":2,
         "min_border_x":0,"min_border_y":0,
         "max_border_x":0,"max_border_y":0}

game["min_border_x"] = -123
game["min_border_y"] = -123

game["max_border_x"] = -123+(game["chunk_x"]*256)
game["max_border_y"] = -123+(game["chunk_y"]*256)

#==============================================================================
#---------------------------------->function
#==============================================================================
#
def arrondi(nombre):
    if nombre > 0:
        return ceil(nombre)
    else:
        return floor(nombre)



def enemy_spawn(data): #x,y,size,damage,speed,acc,reload,projectile,special,detection
    global enemy
    s = {}
    for cle,val in data.items():
        s[cle] = val
        
    if "x" not in s: s["x"] = 0
    if "y" not in s: s["y"] = 0
    if "size" not in s: s["size"] = 10
    if "damage" not in s: s["damage"] = 5
    if "speed" not in s: s["speed"] = 1
    if "acc" not in s: s["acc"] = 0
    if "vx" not in s: s["vx"] = 0
    if "vy" not in s: s["vy"] = 0
    if "max_acc" not in s: s["max_acc"] = s["acc"]*25
    if "reload" not in s: s["reload"] = 0
    if "projectile" not in s: s["projectile"] = []
    if "special" not in s: s["special"] = "common"
    if "detection" not in s: s["detection"] = s["size"]*12
    
    s["x"] += random()-0.5 
    s["y"] += random()-0.5
    enemy[id(enemy)] = s

def bullet_spawn(data={}): #all data of an bullet - > x,y,vx,vy,size,damage,tick,transperce,punch,accx,accy 
    global bullet,player
    s = {}
    for cle,val in data.items():
        s[cle] = val

    if "x" not in s: s["x"] = player["x"]+14
    if "vx" not in s: s["vx"] = 0
    if "accx" not in s: s["accx"] = 0
    if "y" not in s: s["y"] = player["y"]
    if "vy" not in s: s["vy"] = 0
    if "accy" not in s: s["accy"] = 0
    if "size" not in s: s["size"] = 2
    if "damage" not in s: s["damage"] = 10
    if "transperce" not in s: s["transperce"] = 1
    if "punch" not in s: s["punch"] = 0
    if "tick" not in s: s["tick"] = 100
    if "heavy" not in s : s["heavy"] = 0 # between 0 and 1

    bullet[id(bullet)] = s

def mouse_coord():
    global game
    x = game["camera_x"]+pyxel.mouse_x-14
    y = -game["camera_y"]+pyxel.mouse_y
    return(x,y)

def mouse_click():
    global game
    game["mouse"] = 0
    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT): game["mouse"] = 2
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): game["mouse"] = 1
    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT): game["mouse"] = 3
    return(game["mouse"])



def id(dico): #take dico and return an ID
    count = 0
    while count in list(dico.keys()):
        count += 1
    return count

def camera_tick():
    global player,game
    decalage = 0.1
    game["camera_x"] += (player["x"]-game["camera_x"]-123)*decalage
    game["camera_y"] += (-player["y"]-game["camera_y"]+123)*decalage
    game["camera_x"] = max([game["camera_x"],-(123+16)])
    game["camera_y"] = min([game["camera_y"],(123+16)])
    game["camera_y"] = max([game["camera_y"],((game["chunk_y"]-1)*-256)+123-16])
    game["camera_x"] = min([game["camera_x"],((game["chunk_x"]-1)*256)-123+16])

def player_tick():
    global player
    dx = pyxel.btn(pyxel.KEY_D)-pyxel.btn(pyxel.KEY_Q)
    dy = pyxel.btn(pyxel.KEY_Z)-pyxel.btn(pyxel.KEY_S)
    d = sqrt(dx**2 + dy**2)
    if dx !=0:
        player["x"] += ((dx/d)*player["speed"])
    if dy !=0:
        player["y"] -= (dy/d)*player["speed"]
    
    if player["hpm"]>player["hp"]:
        player["hp"] = min([player["hp"]+player["hps"],player["hpm"]])
    player["x"] = max([game["min_border_x"]-(player["size"]/2),player["x"]])
    player["x"] = min([game["max_border_x"]-(player["size"]/2),player["x"]])
def weapon_use():
    global player
    if player["cw"] == "None":
        pass
    elif player["cw"] == "duplicator":
        duplicator()
    elif player["cw"] == "bit_ray":
        bit_ray()
    elif player["cw"] == "code_trapper":
        code_trapper()
    elif player["cw"] == "pixel_pistol":
        pixel_pistol()
    elif player["cw"] == "laser":
        laser()

def pixel_pistol():
    global weapon,player,bullet
    weapon["reload_max"] = 100
    weapon["reload_speed"] = 0.5
    weapon["refresh_need"] = 5
    
    
    weapon["refresh"] = min([weapon["refresh"]+1,weapon["refresh_need"]])
    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and weapon["reload"]>=10 and weapon["refresh_need"] == weapon["refresh"]:
        mx,my = mouse_coord()
        d = sqrt((mx-player["x"])**2 +(my-player["y"])**2)
        vx = ((mx-player["x"])/d)*5
        vy = ((my-player["y"])/d)*5
        s = {"x":player["x"]+14,"y":player["y"],"damage":10,"size":2,"vx":vx,"vy":vy,"accx":0,"accy":0,"punch":1,"transperce":1}
        weapon["reload"] -= 10
        bullet_spawn(s)
        weapon["refresh"] = 0
    else:
        if weapon["reload"]<weapon["reload_max"]:
            weapon["reload"] += weapon["reload_speed"]
            weapon["reload"] = min([weapon["reload"],weapon["reload_max"]])
    
def laser():
    
    global weapon,player,bullet
    weapon["reload_max"] = 100
    weapon["reload_speed"] = 1
    weapon["refresh_need"] = 10
    
    
    weapon["refresh"] = min([weapon["refresh"]+1,weapon["refresh_need"]])
    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and weapon["reload"]>=100/3 and weapon["refresh_need"] == weapon["refresh"]:
        mx,my = mouse_coord()
        d = sqrt((mx-player["x"])**2 +(my-player["y"])**2)
        vx = ((mx-player["x"])/d)*15
        vy = ((my-player["y"])/d)*15
        
        weapon["reload"] -= 100/3
        for i in range(15):
            s = {"x":(player["x"]+14)+(vx*(i-4)*0.1),"y":(player["y"])+(vy*(i-4)*0.1),"damage":2,"size":1.5,"vx":vx,"vy":vy,"accx":0,"accy":0,"punch":0,"transperce":3}
            bullet_spawn(s)
        weapon["refresh"] = 0
    else:
        if weapon["reload"]<weapon["reload_max"]:
            weapon["reload"] += weapon["reload_speed"]
            weapon["reload"] = min([weapon["reload"],weapon["reload_max"]])
    

def duplicator():
    global weapon,player,bullet
    weapon["reload_max"] = 100
    weapon["reload_speed"] = 2
    weapon["refresh_need"] = 25
    
    
    weapon["refresh"] = min([weapon["refresh"]+1,weapon["refresh_need"]])
    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and weapon["reload"]>=100 and weapon["refresh_need"] == weapon["refresh"]:
        mx,my = mouse_coord()
        d = sqrt((mx-player["x"])**2 +(my-player["y"])**2)
        vx = (mx-player["x"])/d
        vy = (my-player["y"])/d
        if abs(vx)> abs(vy):
            vx = arrondi(vx)*player["speed"]
            vy = 0
        else:
            vx = 0
            vy = arrondi(vy)*player["speed"]

        s = {"x":player["x"],"y":player["y"],"damage":player["damage"],"size":player["size"],"vx":vx,"vy":vy,"accx":0,"accy":0,"punch":1,"transperce":int(player["hpm"]//player["damage"])}
        weapon["reload"] -= 100
        bullet_spawn(s)
        weapon["refresh"] = 0
    else:
        if weapon["reload"]<weapon["reload_max"]:
            weapon["reload"] += weapon["reload_speed"]
            weapon["reload"] = min([weapon["reload"],weapon["reload_max"]])


def code_trapper():
    global weapon,player,bullet
    weapon["reload_max"] = 100
    weapon["reload_speed"] = 1/3
    weapon["refresh_need"] = 50
    
    
    weapon["refresh"] = min([weapon["refresh"]+1,weapon["refresh_need"]])
    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and weapon["reload"]>=50 and weapon["refresh_need"] == weapon["refresh"]:
        mx,my = mouse_coord()
        d = sqrt((mx-player["x"])**2 +(my-player["y"])**2)

        s = {"x":player["x"]+(player["size"]/2),"y":player["y"],"damage":100,"size":player["size"]/2,"tick":900,"accx":0,"accy":0,"punch":0,"transperce":5, "heavy":1}
        bullet_spawn(s)
        
        s = {"damage":0,"size":2,"tick":900,"accx":0,"accy":0,"punch":-1,"transperce":50, "heavy":1} 
        for i in range(int(player["size"]/4)):
            s["x"] =  player["x"]+(player["size"]/2)+ (i*s["size"]*2)
            s["y"] = (player["size"]/2)-(s["size"]/2)+player["y"]
            bullet_spawn(s)
        for i in range(int(player["size"]/4)):
            s["x"] =  player["x"]+(player["size"]/2)+ (i*s["size"]*2)
            s["y"] = -(player["size"]/2)+(s["size"]/2)+player["y"]
            bullet_spawn(s)
        for i in range(1,int(player["size"]/4)-1):
            s["x"] = player["x"]+(player["size"]/2)
            s["y"] = -(player["size"]/2)+(s["size"]/2)+player["y"]+(i*s["size"]*2)
            bullet_spawn(s)
        for i in range(1,int(player["size"]/4)-1):
            s["x"] = player["x"]+(player["size"]/2)+player["size"] -(1*s["size"]*2)
            s["y"] = -(player["size"]/2)+(s["size"]/2)+player["y"]+(i*s["size"]*2)
            bullet_spawn(s)


        weapon["refresh"] = 0
        weapon["reload"] -= 50
    else:
        if weapon["reload"]<weapon["reload_max"]:
            weapon["reload"] += weapon["reload_speed"]
            weapon["reload"] = min([weapon["reload"],weapon["reload_max"]])
    

def bullet_tick():
    global bullet, enemy, bullet
    for name, val in list(bullet.items()):
        val["x"] += val["vx"]
        val["y"] += val["vy"]
        val["vx"] += val["accx"]
        val["vy"] += val["accy"]
        if val['tick'] <= 0:
            del bullet[name]
        else:
            val["tick"] -= 1

            
            for enemy_name in  list(enemy.keys()):
               
                dx=enemy[enemy_name]["x"]-bullet[name]["x"]-bullet[name]['size']
                dy=enemy[enemy_name]["y"]-bullet[name]["y"]
                d =hypot(dx,dy)
                nx = dx/d
                ny = dy/d
                min_d = bullet[name]['size']/2 + enemy[enemy_name]['size']
                if d < min_d and d:              
                    bullet[name]["transperce"] -= 1
                    enemy[enemy_name]["hp"] -= bullet[name]['damage']
                    if bullet[name]["punch"]:
                        offset = ((min_d - d) / 2)*bullet[name]["punch"]
                        bullet[name]['x'] -= nx * offset*(1-bullet[name]['heavy']); bullet[name]['y'] -= ny * offset*(1-bullet[name]['heavy'])
                        enemy[enemy_name]['x'] += nx * offset; enemy[enemy_name]['y'] += ny * offset
                    if enemy[enemy_name]["hp"]<= 0:
                        del enemy[enemy_name]
                
            if bullet[name]["transperce"]<=0:
                del bullet[name]
                    




def enemy_tick():
    global bullet, enemy, bullet, player
    keys = list(enemy)
    for i in range(len(keys)):
        data = enemy[keys[i]]
        if data["hp"] > 0:   
            dx = data["x"]-player["x"]-player["size"]
            dy = data["y"]-player["y"]
            d = hypot(dx,dy)
            nx = dx/d
            ny = dy/d
            action = d<data["detection"]
            if action:
                data["x"] -= nx*data["speed"]
                data["y"] -= ny*data["speed"]
            
                
            

            
                min_d = player['size']/2 + data['size']#colision
                if d < min_d and d:
                    offset = (min_d - d) / 2
                    player['x'] -= nx * offset; player['y'] -= ny * offset
                    data['x'] += nx * offset; data['y'] += ny * offset
                    player["hp"], data["hp"] = player["hp"] - data["damage"], data["hp"] - data["damage"]
            
            
            if data['acc']:# Gestion du mouvement avec accélération
                
                if action and d > 0:
                    # Calcul de la direction normalisée
                    dir_x = dx / d
                    dir_y = dy / d
                    
                    # Application de l'accélération
                    data["vx"] -= nx * data["acc"]
                    data["vy"] -= ny * data["acc"]
                    
                    # Limitation de la vitesse maximale
                    current_speed = hypot(data["vx"], data["vy"])

                    if current_speed > data['max_acc']:
                        scale = data['max_acc'] / current_speed
                        data["vx"] *= scale
                        data["vy"] *= scale
                else:
                    # Frottement progressif quand inactif
                    data["vx"] *= 0.9
                    data["vy"] *= 0.9
                    
                    # Mise à zéro si trop lent
                    if abs(data["vx"]) < 0.1:
                        data["vx"] = 0
                    if abs(data["vy"]) < 0.1:
                        data["vy"] = 0
                
                # Mise à jour de la position
                data["x"] += data["vx"]
                data["y"] += data["vy"]
                

            if not game["tick"]%int(min([len(keys)/100,9])+1):
                
                for j in range(i+1, len(keys)):
                    b = enemy[keys[j]]
                    dx, dy = b['x'] - data['x'], b['y'] - data['y']
                    d = hypot(dx, dy)
                    min_d = data['size'] + data['size']
                    if d < min_d and d:
                        offset = (min_d - d) / 2
                        nx, ny = dx/d, dy/d
                        data['x'] -= nx * offset; data['y'] -= ny * offset
                        b['x'] += nx * offset; b['y'] += ny * offset
        else:
            del enemy[keys[i]]
            
            
            
        
        


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
#==============================================================================
#---------------------------------->tick
#==============================================================================
def update():
    global enemy,bullet,weapon,player,game
    game["tick"] += 1
    
    if game["scene"] == "menu":
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 100 < pyxel.mouse_x < 160 and 100< pyxel.mouse_y < 120:
                enemy = {}
                bullet = {}
                player['hp'] = 100
                game['level'] = 0
                player['inventory'] = ['pixel_pistol']
                game["scene"] = "room"
                game["dialogueBox"] = 2
                
            elif 100 < pyxel.mouse_x < 160 and 145< pyxel.mouse_y < 160:
                pyxel.quit()
    if game["scene"] == "room":
        player_tick()
        camera_tick()
        weapon_use()
        mouse_coord()
        bullet_tick()
        enemy_tick()
        mouse_click()
        
        if len(enemy) == 0:
            game["level"] += 1
            for i in range(10):
                enemy_spawn({"x":0, "y":200,"hp":100, "speed":1, "damage":10, "size":10, "acc":0})
#==============================================================================         
#---------------------------------->draw
#==============================================================================
def draw():
    global enemy,bullet,weapon,player,game
    #mettre un objet sur la camera :
    # x-camx ; y+camy
    
    if game["scene"] == "menu":
        pyxel.blt(0,0,2,0,0,256,256)
    elif game["scene"] == "room":
        for x in range(game["chunk_x"]):
            for y in range(game["chunk_y"]):
                pyxel.blt(((x * 256) - 123)-game["camera_x"],(0 + (y* 256) - 123)+ game["camera_y"],1,0,0,256,256)
    
    for key, val in bullet.items():
        demi = val["size"] / 2
        pyxel.rect(val["x"] + demi - game["camera_x"], val["y"] - demi + game["camera_y"],val["size"], val["size"], 7)
    
    
    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
        pyxel.rect(pyxel.mouse_x-2, pyxel.mouse_y-2, 4, 4, 8)
    else:
        pyxel.rect(pyxel.mouse_x-2, pyxel.mouse_y-2, 4, 4, 10)
    
    for key, val in enemy.items():
        pyxel.circ(val["x"]-game["camera_x"], val["y"]+game["camera_y"], val["size"], 5)
    
    demi = player["size"]/2
    pyxel.rect(player["x"]+demi-game["camera_x"],player["y"]-demi+game["camera_y"], player["size"], player["size"], 7)
    


    bar_width = int((weapon["reload"] / weapon["reload_max"]) * 100)
    if bar_width < 10:
        pyxel.rect(10, 240, bar_width, 5, 0)  
    elif bar_width < 50:
        pyxel.rect(10, 240, bar_width, 5, 3)
    elif bar_width < 100:
        pyxel.rect(10, 240, bar_width, 5, 7)    
    else:
        pyxel.rect(10, 240, bar_width, 5, 13) 
    pyxel.rectb(10, 240, 100, 5, 9)
    
    bar_width = int((weapon["refresh"] / weapon["refresh_need"]) * 100)
    if bar_width < 100:
        pyxel.rect(10, 235, bar_width, 5, 9)  
    else:
        pyxel.rect(10, 235, bar_width, 5, 10)  
    
    pyxel.rectb(10, 235, 100, 5, 9)

    bar_width = int((player["hp"] / player["hpm"]) * 100)
    if bar_width < 10:
        pyxel.rect(10, 245, bar_width, 5, 8)  
    elif bar_width < 100:
        pyxel.rect(10, 245, bar_width, 5, 7)  
    else:
        pyxel.rect(10, 245, bar_width, 5, 2) 
    pyxel.rectb(10, 245, 100, 5, 9)
    



pyxel.init(game["screen_size"][0],game["screen_size"][1])
pyxel.load(r".\resource.pyxres")
pyxel.image(1).load(player["x"] , 0 ,r".\room.png")
pyxel.image(2).load(0 , 0 ,r".\menu.png")
pyxel.run(update, draw)
