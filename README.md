## project_X
le jeu ...

quentin : https://www.pyxelstudio.net/studio/mlxgeu

Inspiration :
- The Légende of Zelda 1
- Sonic Frontièrs

arme :
    - lance pixel = pistolet laser
    - sabre néon

armure : chanps de force

## enemy
des cercle, enemy des carré dans une guerre

## histoire
# La Genèse de la Rivalité

Il y a plusieurs siècles, l'Empire des Cercles et la Nation Carrée étaient deux entités indépendantes, mais leurs formes géométriques distinctes ont toujours représenté une fracture culturelle et idéologique profonde. Les Cercles, symboles de fluidité, d'harmonie et d'équilibre, cherchaient à imposer une société unifiée où chacun trouverait sa place sans contrainte. Les Carrés, au contraire, étaient une nation rigide, méticuleuse et organisée, où chaque individu avait un rôle clairement défini, un cadre précis dans lequel vivre et évoluer.

Les tensions entre les deux nations n'ont cessé d'augmenter au fil des siècles, jusqu'à l'An 50, lorsque l'Empire des Cercles lança une série de campagnes pour soumettre la Nation Carrée, qu'ils considéraient comme un obstacle à leur vision du monde. Bien qu'ils aient été plus avancés technologiquement et plus vastes en nombre, les Carrés ont opposé une résistance farouche. Mais après des décennies de conflits, l'Empire des Cercles a finalement réussi à annexer la Nation Carrée en l'an 90.

# L'Annexion et la Résistance

En 90, après une série de batailles et de négociations forcées, la Nation Carrée a été intégrée à l'Empire des Cercles. Les habitants de la Nation Carrée ont été contraints de se conformer à la culture circulaire et à adopter un mode de vie qui leur était étranger et oppressant. Leur monde rigide et carré a été effacé au profit des idéaux circulaires imposés par l'Empire.

Cependant, dans les ombres de cette occupation, une résistance s'est formée. De petits groupes de rebelles carrés ont commencé à se réunir, prêts à tout pour récupérer leur indépendance et restaurer leur mode de vie. Parmi ces résistants, un jeune homme nommé Zylar Carron, fils d'un ancien général carré, est rapidement devenu une figure centrale de cette lutte.

# Le Héros : Zylar Carron

Zylar Carron naquit dans une petite ville carrée, loin des grandes métropoles de la Nation Carrée. Fils d'un général respecté, Zylar grandit avec un sens aigu de l'honneur et de la rigueur. À l'âge de 18 ans, il fut témoin de la chute de sa ville natale, envahie et détruite par l'armée circulaire lors de l'Annexion. Son père, tué au combat, laissa à Zylar non seulement un héritage familial, mais aussi un désir ardent de venger sa nation et de restaurer l'ordre carré.

Au début, Zylar s'opposa à l'Empire des Cercles en tant que simple soldat de la résistance, mais ses compétences exceptionnelles en stratégie et son charisme naturel le propulsèrent rapidement à la tête des forces rebelles. Il devint une figure légendaire, connue sous le nom de "Le Carré Vivant" pour son insistance à rester fidèle aux idéaux de sa nation, refusant de se laisser "arrondir" par les influences circulaires.

# L'Ère du Jeu : 20 ans Après l'Annexion

Vingt ans après l'annexion de la Nation Carrée, l'Empire des Cercles a presque entièrement assimilé les anciens territoires carrés, mais la résistance ne s'est pas éteinte. Zylar Carron, devenu un leader emblématique et presque mythique parmi les rebelles, continue de mener une guerre secrète contre l'Empire des Cercles. Si la guerre ouverte a pris fin, la résistance a évolué pour devenir un mouvement de guérilla, opérant sous forme de cellules disséminées dans l'Empire.

Les Cercles, bien qu'ayant réussi à maintenir leur pouvoir, se retrouvent confrontés à une insurrection croissante. Des rumeurs de révoltes éclatent dans plusieurs régions, et la figure de Zylar Carron devient un symbole d'espoir pour les opprimés. Le peuple carré, vivant sous le joug des Cercles, nourrit toujours un désir secret de retrouver leur autonomie et de renverser les oppresseurs circulaires.

Zylar, âgé maintenant de 38 ans, est devenu un maître tacticien, connu pour ses incursions audacieuses et sa capacité à échafauder des plans complexes. Cependant, il reste hanté par la perte de sa famille et par le souvenir de la chute de sa ville natale. Son objectif ultime est de redonner à son peuple la liberté et l'indépendance qu'il a perdues, mais les cercles sont partout, dans les rues, dans les esprits et dans les structures de pouvoir. Sa lutte devient plus personnelle chaque jour, au fur et à mesure qu'il doit naviguer dans un monde où la frontière entre le bien et le mal devient de plus en plus floue.

Le joueur incarnera Zylar Carron, en quête de vengeance et de liberté pour son peuple. Il devra rallier les factions rebelles, infiltrer les cités circulaires et déjouer les manœuvres de l'Empire des Cercles tout en affrontant ses propres démons intérieurs. Le jeu se déroulera dans un monde richement détaillé où chaque choix influencera le destin de la résistance et l'avenir de la Nation Carrée.

https://zestedesavoir.com/tutoriels/2835/theorie-des-collisions/collisions-en-2d/

import pyxel
from time import time, sleep
from math import sqrt,sin,cos
from random import random
"""
weapon:

pixel_l -> pixel launcher
pixel_IA -> pixel intelligent
"""

level = 0

class App:
    def __init__(self):
        pyxel.init(512, 512)
        self.enemy = {}  
        self.bullet = {}  
        self.player = {'x': 50, 'y': 50, 'size': 32, "reload": 100, "hp": 100, "weapon": "pixel_l"}
        self.last_direction = [1, 0]  # left direction
        
        self.enemy_spawn(500, 250, 20, 100, 10)
        
        pyxel.run(self.update, self.draw)
        
#________________________enemy maker________________________
    def enemy_spawn(self, x, y, radius, hp, damage):
        """Fait apparaître un ennemi à une position donnée avec un certain rayon et points de vie."""
        self.enemy[f"enemy{time()}"] = {'x': x, 'y': y, 'radius': radius, "hp": hp, "damage": damage}
        
#________________________bullet maker________________________
    def bullet_spawn(self, x, y, radius, direction, damage):
        """Fait apparaître un projectile avec un certain rayon et une direction de mouvement."""
        self.bullet[f"bullet{time()}"] = {'x': x, 'y': y, 'radius': radius, 'direction': direction, "damage": damage}
        
#________________________player direction________________________
    def direction_axe(self, axe):
        """Détermine la direction de mouvement du joueur selon les touches fléchées."""
        if axe == 'x':
            return pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT)
        elif axe == 'y':
            return pyxel.btn(pyxel.KEY_DOWN) - pyxel.btn(pyxel.KEY_UP)
            
            
#________________________weapon________________________
    def shoot_player(self):
        """Tire un projectile dans la dernière direction enregistrée si la touche Espace est pressée."""
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
            level += 1
            #x,y,size,hp,damage
            if level == 1:
                self.enemy_spawn(500, 499, 20, 100, 10)
                sleep(0.01)
                self.enemy_spawn(500, 1, 20, 100, 10)
            if level == 2:
                self.enemy_spawn(500, 250, 40, 400, 40)
                sleep(0.01)
            if level == 3:
                self.enemy_spawn(500, 250, 2, 200, 10)
                sleep(0.01)
            if level == 4:
                for i in range(6):
                    self.enemy_spawn(500,i*100 +1, 20, 100, 10)
                    sleep(0.01)
            if level == 5:
                self.enemy_spawn(1, 1, 32, 100, 10)
                sleep(0.01)
                self.enemy_spawn(1, 500, 32, 100, 10)
                sleep(0.01)
                self.enemy_spawn(500, 500, 32, 100, 10)
                sleep(0.01)
                self.enemy_spawn(500, 1, 32, 100, 10)
            if level == 6:
                self.enemy_spawn(500, 250, 1000, 1000, 100)
            if level == 7:
                for i in range(3):
                    for j in range(3):
                        if j !=1 or i != 1:
                            self.enemy_spawn(250*i, 250*j, 32, 100, 10)
                            sleep(0.01)
            if level == 8:
                self.enemy_spawn(500, 250, 1, 200, 100)
                
            if level == 9:
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
        
#________________________anbandonned funtion ________________________
        self.shoot_player()

#________________________bullet tick________________________
        for bullet_name in list(self.bullet.keys()):
            bullet = self.bullet[bullet_name]
            bullet['x'] += bullet['direction'][0]
            bullet['y'] += bullet['direction'][1]

            # delect bullet outside the screen
            if not (0 <= bullet['x'] <= 512 and 0 <= bullet['y'] <= 512):
                del self.bullet[bullet_name]
                continue  

            
            for enemy_name in list(self.enemy.keys()):
                enemy = self.enemy[enemy_name]
                distance = sqrt((enemy['x'] - bullet['x']) ** 2 + (enemy['y'] - bullet['y']) ** 2)

                if distance < enemy["radius"]+bullet["radius"]:
                   
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
                self.player['x'] += int(round(vec_x / norm)) * 3  # Réaction à la collision
                self.player['y'] += int(round(vec_y / norm)) * 3
                self.player['hp'] -= self.enemy[name]['damage']
            elif norm > 0:
                self.enemy[name]['x'] += int(round(vec_x / norm)) * 2
                self.enemy[name]['y'] += int(round(vec_y / norm)) * 2

    
#________________________draw________________________
    def draw(self):
        """Dessine tous les éléments du jeu à l'écran."""
        pyxel.cls(0) 
        if self.player["hp"]>0:
            
            
    
            #draw player
            pyxel.rect(self.player['x'], self.player['y'], self.player['size'], self.player['size'], 7)
    
            #draw enemy
            for name in self.enemy.keys():
                pyxel.circ(self.enemy[name]['x'], self.enemy[name]['y'], self.enemy[name]['radius'], 8)
    
            #draw bullet
            for name in self.bullet.keys():
                size = self.bullet[name]['radius'] * 2  
                pyxel.rect(self.bullet[name]['x'], 
                           self.bullet[name]['y'], 
                           size, size, 7)
    
            #draw reload barre for reload
            bar_width = int((self.player["reload"] / 100) * 100)  
            if self.player["reload"] < 10:
                pyxel.rect(10, 490, bar_width, 5, 8)  
            elif self.player["reload"] < 100:
                pyxel.rect(10, 490, bar_width, 5, 7)  
            else:
                pyxel.rect(10, 490, bar_width, 5, 11) 
            pyxel.rectb(10, 490, 100, 5, 1)  
    
            #draw reload barre for hp of player
            bar_width = int((self.player["hp"] / 100) * 100)
            if self.player["hp"] < 10:
                pyxel.rect(10, 500, bar_width, 5, 8) 
            elif self.player["hp"] < 100:
                pyxel.rect(10, 500, bar_width, 5, 7)  
            else:
                pyxel.rect(10, 500, bar_width, 5, 11)  
            pyxel.rectb(10, 500, 100, 5, 1)  
        else:
            xs = cos(time()*10)*10
            ys = sin(time()*10)*10
            for i in range(11):
                for j in range(11):
                    pyxel.text(i*50+xs,j*50+ys, 'GAME OVER', 8)

App()
