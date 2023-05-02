from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import uniform
from perlin_noise import PerlinNoise

app = Ursina()

texture1 = load_texture('assets/grass_block.png')
texture2 = load_texture('assets/stone_block.png')
texture3 = load_texture('assets/brick_block.png')
texture4 = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
sans = load_texture('assets/Sans.png')
block_pick = 1

def input(key):
    if key == 'escape':
        quit()

def update():
    global block_pick
    if held_keys['1']: 
        block_pick = 1
    if held_keys['2']: 
        block_pick = 2
    if held_keys['3']: 
        block_pick = 3
    if held_keys['4']: 
        block_pick = 4
    if held_keys['5']: 
        block_pick = 5
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else: 
        hand.passive()

class Block(Button):
    def __init__(self,position=(0,0,0),texture = texture1):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            scale = 0.5
        )

    def input(self,key):
        if self.hovered:
            if key == 'left mouse down':
                if block_pick == 1: 
                    block = Block(position = self.position + mouse.normal,texture = texture1)
                if block_pick == 2: 
                    block = Block(position = self.position + mouse.normal,texture = texture2)
                if block_pick == 3: 
                    block = Block(position = self.position + mouse.normal,texture = texture3)
                if block_pick == 4: 
                    block = Block(position = self.position + mouse.normal,texture = texture4)
                if block_pick == 5: 
                    block = Block(position = self.position + mouse.normal,texture =  sans)
            
            if key == 'right mouse down':
                destroy(self)

class SKy(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 150,
            double_sided = True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150,-10,0),
            position = Vec2(0.4,-0.6)
        )

    def active(self):
        self.position = Vec2(0.3,-0.5)

    def passive(self):
        self.position = Vec2(0.4,-0.6)

noise = PerlinNoise(octaves = 3, seed = 2023)
scale = 24

for z in range(50):
    for x in range(50):
        block = Block(position = (x,0,z))
        block.y = floor(noise([x/scale,z/scale])*8)

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()