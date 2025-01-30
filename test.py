    print("Hello World !")import pyxel
from time import time
from math import sqrt

class App:
    def __init__(self):
        pyxel.init(512, 512)
        self.enemy = {}  
        self.bullet = {}  
        self.player = {'x': 50, 'y': 50, 'size': 32, "reload": 100}
        self.last_direction = [1, 0]  # Default direction (moving right)

        self.enemy_spawn(300, 300, 20)
        
        pyxel.run(self.update, self.draw)
        
    def enemy_spawn(self, x, y, radius):
        """Spawn an enemy at a given position with a specific radius."""
        self.enemy[f"enemy{time()}"] = {'x': x, 'y': y, 'radius': radius}
    
    def bullet_spawn(self, x, y, radius, direction):
        """Spawn a bullet at (x, y) with a given radius and movement direction."""
        self.bullet[f"bullet{time()}"] = {'x': x, 'y': y, 'radius': radius, 'direction': direction}

    def direction_axe(self, axe):
        """Get movement direction for player based on arrow keys."""
        if axe == 'x':
            return pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT)
        elif axe == 'y':
            return pyxel.btn(pyxel.KEY_DOWN) - pyxel.btn(pyxel.KEY_UP)

    def shoot_player(self):
        """Shoot a bullet in the last movement direction if space is pressed."""
        if self.player["reload"] >= 10 and pyxel.btnp(pyxel.KEY_SPACE):  # Fire only on key press
            size = sqrt(self.player["reload"])  # Bullet size 
            vx,vy = self.last_direction  #  Use the last arrow key direction

            
            bullet_x = self.player['x'] + self.player['size'] / 2 - size
            bullet_y = self.player['y'] + self.player['size'] / 2 - size

            self.bullet_spawn(bullet_x, bullet_y, size, [vx*5,vy*5])
            self.player["reload"] = 0  # Reset reload timer

    def update(self):
        
        """Game update loop: handles movement, shooting, and collision detection."""
        move_x = self.direction_axe("x")
        move_y = self.direction_axe("y")

        
        self.player['x'] += move_x * 3
        self.player['y'] += move_y * 3

       
        if move_x != 0 or move_y != 0:
            self.last_direction = [move_x, move_y]

        # Keep the player 
        self.player['x'] = max(0, min(self.player['x'], 512 - self.player['size']))
        self.player['y'] = max(0, min(self.player['y'], 512 - self.player['size']))

        # reload 
        if self.player["reload"] < 100:
            self.player["reload"] += 1
        self.shoot_player()

        # Move bullets
        for name in list(self.bullet.keys()):  # Avoid modification errors during iteration
            self.bullet[name]['x'] += self.bullet[name]['direction'][0]
            self.bullet[name]['y'] += self.bullet[name]['direction'][1]

            # Remove bullets 
            if not (0 <= self.bullet[name]['x'] <= 512 and 0 <= self.bullet[name]['y'] <= 512):
                del self.bullet[name]

        # Enemy movement
        for name in self.enemy.keys():
            vec_x = (self.player['x'] + self.player['size'] / 2) - self.enemy[name]['x']
            vec_y = (self.player['y'] + self.player['size'] / 2) - self.enemy[name]['y']
            norm = sqrt(vec_x ** 2 + vec_y ** 2)

            if norm < self.enemy[name]['radius'] + self.player['size'] / 2:
                self.enemy[name]['x'] -= int(round(vec_x / norm)) * 3
                self.enemy[name]['y'] -= int(round(vec_y / norm)) * 3
                self.player['x'] += int(round(vec_x / norm)) * 3  # Player collision reaction
                self.player['y'] += int(round(vec_y / norm)) * 3
            elif norm > 0:
                self.enemy[name]['x'] += int(round(vec_x / norm)) * 2
                self.enemy[name]['y'] += int(round(vec_y / norm)) * 2

    def draw(self):
        """Draw all game elements on the screen."""
        pyxel.cls(0)
        
        #draw player
        pyxel.rect(self.player['x'], self.player['y'], self.player['size'], self.player['size'], 7)
        
        #draw enemy
        for name in self.enemy.keys():
            pyxel.circ(self.enemy[name]['x'], self.enemy[name]['y'], self.enemy[name]['radius'], 8)

        # Draw bullets
        for name in self.bullet.keys():
            size = self.bullet[name]['radius'] * 2  # Square size depends on reload value
            pyxel.rect(self.bullet[name]['x'], 
                       self.bullet[name]['y'], 
                       size, size, 7)

        # Draw reload bar at bottom left
        bar_width = int((self.player["reload"] / 100) * 100)  # Scale to 100 pixels max
        if self.player["reload"]<10:
            pyxel.rect(10, 500, bar_width, 5, 8)# red
        elif self.player["reload"]<100:
            pyxel.rect(10, 500, bar_width, 5, 7)#white
        else:
            pyxel.rect(10, 500, bar_width, 5, 11)#vert
        # Draw reload bar outline
        pyxel.rectb(10, 500, 100, 5, 1)  # Black border

App()
