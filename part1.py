# pyglet event handler demo
import sys
sys.dont_write_bytecode = True
import imp
import pyglet
from pyglet.gl import glEnable, glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_BLEND
from pyglet.window import mouse, key



# Our World
class Scene:

    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?"):

        self.hero = Hero()
        self.weapon = Weapon()

        levelname = sys.argv[-1]
        self.level = imp.load_source('happy',levelname+'.py')

        print(str(['rows=',self.level.rows,'cols=',self.level.cols]))


        self.keyDict = {'RIGHT': False, 'LEFT': False, 'RUN': False, 'SHOOT': False, 'JUMP': False, 'ATTACK': False}

        # Build the OpenGL / Pyglet Window
        self.window = pyglet.window.Window(width=width, height=height, caption=caption)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


        # Create the Background
        self.background = pyglet.resource.image(self.level.background)
        self.background_x = 0
        #music = pyglet.media.load(level.music)
        #music.play()

        pyglet.clock.schedule_interval(self.step, 0.02)


        # Great for debugging
        self.window.push_handlers(pyglet.window.event.WindowEventLogger())

        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():
            #while(self.running):
                self.window.clear()
                self.background.blit(self.background_x,0,height=height)
                #self.levelDef = self.level.board2grid(self.level.levelDefinition)
                self.level.drawBoard(self.level.level)
                self.level.drawBoard(self.level.goals)
                if self.keyDict['RIGHT'] == False and self.keyDict['LEFT'] == False:
                    self.hero.switch('Idle', self.hero.dir, False)
                self.hero.currentSprite.draw()

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.LEFT:
                 self.keyDict['LEFT'] = True
                 self.hero.switch('Run', 'LEFT', True)
            elif symbol == key.RIGHT:
                self.keyDict['RIGHT'] = True
                self.hero.switch('Run', 'RIGHT', False)
            elif symbol == key.LSHIFT or symbol == key.RSHIFT: self.keyDict['RUN'] = True
            elif symbol == key.LCTRL or symbol == key.RCTRL: self.keyDict['SHOOT'] = True
            elif symbol == key.SPACE: self.keyDict['JUMP'] = True
            elif symbol == key.LALT or symbol == key.RALT: self.keyDict['ATTACK'] = True

        @self.window.event
        def on_key_release(symbol, modifiers):
            if symbol == key.LEFT: self.keyDict['LEFT'] = False
            elif symbol == key.RIGHT: self.keyDict['RIGHT'] = False
            elif symbol == key.LSHIFT or symbol == key.RSHIFT: self.keyDict['RUN'] = False
            elif symbol == key.LCTRL or symbol == key.RCTRL: self.keyDict['SHOOT'] = False
            elif symbol == key.SPACE: self.keyDict['JUMP'] = False
            elif symbol == key.LALT or symbol == key.RALT: self.keyDict['ATTACK'] = False

    def step(self, dist):
        self.hero.move(self.keyDict)

class Player(object):
        def load_images(self, action, flip):
            pass

#scale = 0.15, animation speed = 0.05
class Hero(Player):
    def __init__(self):
        Player.__init__(self)
        self.x = 100
        self.y = 100
        self.steps = 0
        self.action = 'Idle'
        self.dir = 'Right'
        self.falling = False
        self.speed = 0.05
        self.scale = 0.15
        self.dist = 0
        self.currentSprite = self.switch(self.action, self.dir, False)

        #Load animation sequences
        #self.idle = pyglet.image.Animation.from_image_sequence(self.load_images('Idle', False), 0.15, True)
        #self.idleSprite = pyglet.sprite.Sprite(self.idle, self.x, self.y)
        #self.move_right = pyglet.image.Animation.from_image_sequence(self.load_images('Run', False), 0.15, True)
        #self.move_right_Sprite = pyglet.sprite.Sprite(self.move_right, self.x, self.y)
        #self.move_left = pyglet.image.Animation.from_image_sequence(self.load_images('Run', True), 0.15, True)
        #self.move_left_Sprite = pyglet.sprite.Sprite(self.move_left, self.x, self.y)

    def load_images(self, action, flip):
        spriteArray = []
        spriteFile = action
        for x in range(1, 11):
            img = pyglet.resource.image('sprites/hero/' + action + " (" + str(x) + ").png", flip_x=flip)
            spriteArray.append(img)
        return spriteArray
    def switch(self, action, direction, flip):
        self.action = action
        self.dir = direction
        actionSeq = self.load_images(action, flip)
        playerAnimation = pyglet.image.Animation.from_image_sequence(actionSeq, self.speed, True)
        self.currentSprite = pyglet.sprite.Sprite(playerAnimation, self.x, self.y)
        self.currentSprite.scale = self.scale
        return self.currentSprite
    def move(self, keyDict):
        if keyDict['RUN']:
            self.dist = 9
        else:
            self.dist = 3

        if keyDict['LEFT'] or keyDict['RIGHT']:
            self.steps = 10

        if self.steps > 0:
            if keyDict['RIGHT']:
                self.currentSprite.x = self.currentSprite.x + self.dist
                self.x = self.x + self.dist
            if keyDict['LEFT']:
                self.currentSprite.x = self.currentSprite.x - self.dist
                self.x = self.x - self.dist
            self.steps = self.steps - 1
    #def drawMove(self, currentImgSeq):
    #    self.currentSprite = pyglet.sprite.Sprite(currentImgSeq, self.x, self.y)
    #    self.currentSprite.scale = .15
    #    return self.currentSprite

class Weapon(Player):
    def __init__(self):
        Player.__init__(self)

        self.x = 100
        self.y = 100

        self.wep = pyglet.image.Animation.from_image_sequence(self.load_images('Kunai', False), 0.15, True)
        #self.weaponSprite = pyglet.sprite.Sprite(self.wep, self.x, self.y)
        #self.weaponSprite.scale = .15

    def load_images(self, action, flip):
        spriteArray = []

        for i in range(1, 11):
            img = pyglet.resource.image('sprites/weapon/' + action + " (" + str(i) + ").png", flip_x=flip)
            spriteArray.append(img)
        return spriteArray






if __name__ == '__main__':
    myGame = Scene()
    pyglet.app.run()
