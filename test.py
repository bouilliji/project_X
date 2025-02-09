import pyxel
from time import time, sleep
from math import sqrt, sin, cos
from random import random

"""
weapon:

pixel_l -> pixel launcher
pixel_IA -> pixel intelligent
"""



class App:
    def __init__(self):
        pyxel.init(512, 512)
        self.enemy = {}  
        self.bullet = {}  
        self.player = {'x': 50, 'y': 50, 'size': 32, "reload": 100, "hp": 100, "weapon": "pixel_l", "level":0}
        self.last_direction = [1, 0]  # left direction
        
        self.enemy_spawn(500, 250, 20, 100, 10)
        
        pyxel.run(self.update, self.draw)
        
#________________________enemy maker________________________
    def enemy_spawn(self, x, y, radius, hp, damage):
        """Spawns an enemy at a given position with certain radius and health points."""
        self.enemy[f"enemy{time()}"] = {'x': x, 'y': y, 'radius': radius, "hp": hp, "damage": damage}
        
#________________________bullet maker________________________
    def bullet_spawn(self, x, y, radius, direction, damage):
        """Spawns a projectile with a certain radius and direction."""
        self.bullet[f"bullet{time()}"] = {'x': x, 'y': y, 'radius': radius, 'direction': direction, "damage": damage}
        
#________________________player direction________________________
    def direction_axe(self, axe):
        """Determines the movement direction of the player based on the QZSD keys."""
        if axe == 'x':
            return pyxel.btn(pyxel.KEY_D) - pyxel.btn(pyxel.KEY_Q)
        elif axe == 'y':
            return pyxel.btn(pyxel.KEY_S) - pyxel.btn(pyxel.KEY_Z)
            
#________________________weapon________________________
    def shoot_player(self):
        """Shoots a projectile in the last recorded direction if the space bar is pressed."""
        if self.player["reload"] >= 10 and pyxel.btnp(pyxel.KEY_SPACE):  # reload time
            size = sqrt(self.player["reload"])  # bullet size
            vx, vy = self.last_direction  # use the last direction of the player

            bullet_x = self.player['x'] + self.player['size'] / 2 - size
            bullet_y = self.player['y'] + self.player['size'] / 2 - size
            
            self.bullet_spawn(bullet_x, bullet_y, size, [vx * 5, vy * 5], self.player["reload"])
            self.player["reload"] = 0  # reset reload
            
#_____________________________tick_______________________________________
    def update(self):
        global level
        if len(list(self.enemy.keys())) == 0:
            self.player['level'] += 1
            #x,y,size,hp,damage
            if self.player['level'] == 1:
                self.enemy_spawn(500, 499, 20, 100, 10)
                sleep(0.01)
                self.enemy_spawn(500, 1, 20, 100, 10)
            if self.player['level'] == 2:
                self.enemy_spawn(500, 250, 40, 400, 40)
                sleep(0.01)
            if self.player['level'] == 3:
                self.enemy_spawn(500, 250, 2, 200, 10)
                sleep(0.01)
            if self.player['level'] == 4:
                for i in range(6):
                    self.enemy_spawn(500,i*100 +1, 20, 100, 10)
                    sleep(0.01)
            if self.player['level'] == 5:
                self.enemy_spawn(1, 1, 32, 100, 10)
                sleep(0.01)
                self.enemy_spawn(1, 500, 32, 100, 10)
                sleep(0.01)
                self.enemy_spawn(500, 500, 32, 100, 10)
                sleep(0.01)
                self.enemy_spawn(500, 1, 32, 100, 10)
            if self.player['level'] == 6:
                self.enemy_spawn(500, 250, 1000, 1000, 100)
            if self.player['level'] == 7:
                for i in range(3):
                    for j in range(3):
                        if j !=1 or i != 1:
                            self.enemy_spawn(250*i, 250*j, 32, 100, 10)
                            sleep(0.01)
            if self.player['level'] == 8:
                self.enemy_spawn(500, 250, 1, 200, 100)
                
            if self.player['level'] == 9:
                self.enemy_spawn(600, 250, 2000, 10000, 999)
                
        
#________________________player direction ________________________
        move_x = self.direction_axe("x")
        move_y = self.direction_axe("y")
        
#________________________player  move________________________
        self.player['x'] += move_x * 3
        self.player['y'] += move_y * 3

        if move_x != 0 or move_y != 0:
            self.last_direction = [move_x, move_y]

        # 
        self.player['x'] = max(0, min(self.player['x'], 512 - self.player['size']))
        self.player['y'] = max(0, min(self.player['y'], 512 - self.player['size']))

#________________________reload +________________________
        if self.player["reload"] < 100:
            self.player["reload"] += 1
#________________________hp + ________________________
        if 0 <self.player["hp"] < 100:
            self.player["hp"] += 0.1
        
#________________________abandoned function ________________________
        self.shoot_player()

#________________________bullet tick________________________
        for bullet_name in list(self.bullet.keys()):
            bullet = self.bullet[bullet_name]
            bullet['x'] += bullet['direction'][0]
            bullet['y'] += bullet['direction'][1]

            # delete bullet outside the screen
            if not (0 <= bullet['x'] <= 512 and 0 <= bullet['y'] <= 512):
                del self.bullet[bullet_name]
                continue  

            
            for enemy_name in list(self.enemy.keys()):
                enemy = self.enemy[enemy_name]
                distance = sqrt((enemy['x'] - bullet['x']) ** 2 + (enemy['y'] - bullet['y']) ** 2)

                if distance < enemy["radius"] + bullet["radius"]:
                    enemy["hp"] -= bullet["damage"]

                    del self.bullet[bullet_name]

                    if enemy["hp"] <= 0:
                        del self.enemy[enemy_name]

                    break  

#________________________enemy tick________________________
        for name in self.enemy.keys():
            vec_x = (self.player['x'] + self.player['size'] / 2) - self.enemy[name]['x']
            vec_y = (self.player['y'] + self.player['size'] / 2) - self.enemy[name]['y']
            norm = sqrt(vec_x ** 2 + vec_y ** 2)

            if norm < self.enemy[name]['radius'] + self.player['size'] / 2:
                self.enemy[name]['x'] -= int(round(vec_x / norm)) * 3
                self.enemy[name]['y'] -= int(round(vec_y / norm)) * 3
                self.player['x'] += int(round(vec_x / norm)) * 3  # Collision reaction
                self.player['y'] += int(round(vec_y / norm)) * 3
                self.player['hp'] -= self.enemy[name]['damage']
            elif norm > 0:
                self.enemy[name]['x'] += int(round(vec_x / norm)) * 2
                self.enemy[name]['y'] += int(round(vec_y / norm)) * 2

    
#________________________draw________________________
    def draw(self):
        """Draws all game elements on the screen."""
        pyxel.cls(0) 
        if self.player["hp"] > 0:
            # Draw player
            pyxel.rect(self.player['x'], self.player['y'], self.player['size'], self.player['size'], 7)
    
            # Draw enemy
            for name in self.enemy.keys():
                pyxel.circ(self.enemy[name]['x'], self.enemy[name]['y'], self.enemy[name]['radius'], 8)
    
            # Draw bullet
            for name in self.bullet.keys():
                size = self.bullet[name]['radius'] * 2  
                pyxel.rect(self.bullet[name]['x'], 
                           self.bullet[name]['y'], 
                           size, size, 7)
    
            # Draw reload bar for reload
            bar_width = int((self.player["reload"] / 100) * 100)  
            if self.player["reload"] < 10:
                pyxel.rect(10, 490, bar_width, 5, 8)  
            elif self.player["reload"] < 100:
                pyxel.rect(10, 490, bar_width, 5, 7)  
            else:
                pyxel.rect(10, 490, bar_width, 5, 11) 
            pyxel.rectb(10, 490, 100, 5, 1)  
    
            # Draw reload bar for player's HP
            bar_width = int((self.player["hp"] / 100) * 100)
            if self.player["hp"] < 10:
                pyxel.rect(10, 500, bar_width, 5, 8) 
            elif self.player["hp"] < 100:
                pyxel.rect(10, 500, bar_width, 5, 7)  
            else:
                pyxel.rect(10, 500, bar_width, 5, 11)  
            pyxel.rectb(10, 500, 100, 5, 1)  
        else:
            xs = cos(time() * 10) * 10
            ys = sin(time() * 10) * 10
            for i in range(11):
                for j in range(11):
                    pyxel.text(i * 50 + xs, j * 50 + ys, 'GAME OVER', 8)

App()
