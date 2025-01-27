import pyxel
from time import time
from math import sqrt

class App:
    def __init__(self):
        pyxel.init(512, 512)
        self.x = 0
        self.enemy = {}
        self.player = {'x':50 , 'y':50 , 'size':32}
        self.enemy_spawn(300,300,20)
        pyxel.run(self.update, self.draw)
        
    def enemy_spawn(self,x,y,radius):
        self.enemy[f"enemy{time()}"] = {'x':x , 'y':y , 'radius':radius}

    def dirrection_axe(self,axe):
        if axe == 'x':
            return pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT)
        elif axe == 'y':
            return pyxel.btn(pyxel.KEY_DOWN) - pyxel.btn(pyxel.KEY_UP)

    def update(self):
        self.player['x'] += self.dirrection_axe("x") * 3
        self.player['y'] += self.dirrection_axe("y") * 3
        if not 0 < self.player['x'] < 512 - self.player['size']:
            self.player['x'] -= self.dirrection_axe("x") * 3
        if not 0 < self.player['y'] < 512 - self.player['size']:
            self.player['y'] -= self.dirrection_axe("y") * 3

        for name in self.enemy.keys():
            vecteur = ((self.player['x'] + self.player['size']/2) - self.enemy[name]['x'], (self.player['y'] + self.player['size']/2) - self.enemy[name]['y'])
            norme = sqrt(vecteur[0]**2 + vecteur[1]**2)
            if norme < self.enemy[name]['radius'] + self.player['size'] / 2:
                self.enemy[name]['x'] -= int(round(vecteur[0] / norme)) * 3
                self.enemy[name]['y'] -= int(round(vecteur[1] / norme)) * 3
            elif norme > 0:
                self.enemy[name]['x'] += int(round(vecteur[0] / norme)) * 2
                self.enemy[name]['y'] += int(round(vecteur[1] / norme)) * 2
            elif norme == 0:
                continue



    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.player['x'], self.player['y'], self.player['size'], self.player['size'], 9)
        for name in self.enemy.keys():
            pyxel.circ(self.enemy[name]['x'], self.enemy[name]['y'], self.enemy[name]['radius'], 8)

App()