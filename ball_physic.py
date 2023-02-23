import pygame, math, random

class ball:
    def __init__(self, px, py, vx, vy, ax, ay, radius, mass, id, partition):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.radius = radius
        self.mass = mass
        self.id = id
        self.is_move = False
        self.partition = partition
        self.partitions = [self.partition]

WIDTH = 800
HEIGHT = 600

class Grid:
    def __init__(self, gridsize):
        self.gridsize = gridsize
        self.row = HEIGHT/gridsize
        self.col = WIDTH/gridsize
        self.ball_list = list()

    def addBall(self, x, y, r):
        newBall = ball(x,y,0,0,0,0,r,r*10,len(self.ball_list), [x/self.gridsize, y/self.gridsize])
        self.ball_list.append(newBall)



pygame.init()
font = pygame.font.Font(None, 14)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Game:
    def __init__(self, screen):
        self.ball_list = list()
        self.selectball = None
        self.clicked = False
        self.screen = screen
        self.force = 10.0
        self.stop_threshold = 3.0
        self.selectball_pos = list()
        self.is_draw_line = False
        self.gridsize = 20
        for _ in range(100):
            self.addball(random.randint(0,800), random.randint(0,600), 10)

    def addball(self, x, y, r):
        newball = ball(x,y,0,0,0,0,r,r*10,len(self.ball_list), [x//self.gridsize, y//self.gridsize])
        self.ball_list.append(newball)

    def update(self, elapse_time):
        DoballsOverlap = lambda x1, y1, r1, x2, y2, r2: abs((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)) <= (r1 + r2)*(r1 + r2)
        is_point_in_ball = lambda x1, y1, r1, px, py: ((x1 - px)**2 + (y1 - py)**2) < r1**2
        
        mouse_event = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_event[0] and not self.clicked:
            for ball in self.ball_list:
                if (is_point_in_ball(ball.px, ball.py, ball.radius, mouse_pos[0], mouse_pos[1])):
                    if ball.vx == 0 and ball.vy == 0:
                        self.selectball = ball
                        self.selectball_pos = [self.selectball.px, self.selectball.py]
                        self.is_draw_line = True
                        self.clicked = True
                        break

        if mouse_event[2] and not self.clicked:
            self.selectball_pos = None
            for ball in self.ball_list:
                if (is_point_in_ball(ball.px, ball.py, ball.radius, mouse_pos[0], mouse_pos[1])):
                    ball.vx = 0
                    ball.vy = 0
                    self.selectball = ball
                    self.clicked = True
                    break

        if mouse_event[0]:
            if self.is_draw_line:
                pygame.draw.line(self.screen, (0,0,255), (self.selectball_pos[0], self.selectball_pos[1]), (mouse_pos[0], mouse_pos[1]), 2)
                pygame.draw.line(self.screen, (255,0,0), (self.selectball_pos[0], self.selectball_pos[1]), (self.selectball_pos[0]+(self.selectball_pos[0]-mouse_pos[0])*100, self.selectball_pos[1]+(self.selectball_pos[1]-mouse_pos[1])*100), 2)

        if mouse_event[2]:
            if self.selectball != None:
                self.selectball.px = mouse_pos[0]
                self.selectball.py = mouse_pos[1]

        # Apply force
        if not mouse_event[0] and self.clicked:
            try:
                if self.selectball != None:
                    self.selectball.is_move = True
                    self.selectball.vx = self.force * (self.selectball_pos[0] - mouse_pos[0])
                    self.selectball.vy = self.force * (self.selectball_pos[1] - mouse_pos[1])
                self.selectball = None
                self.clicked = False
                self.is_draw_line = False
            except:
                pass

        if not mouse_event[2] and not mouse_event[0] and self.clicked:
            self.selectball = None
            self.clicked = False

        vecCollidingPairs = list()

        for ball in self.ball_list:
            if not ball.is_move:
                continue
            ball.ax = -ball.vx * 0.8
            ball.ay = -ball.vy * 0.8

            ball.vx += ball.ax * elapse_time
            ball.vy += ball.ay * elapse_time
            ball.px += ball.vx * elapse_time
            ball.py += ball.vy * elapse_time

            ball.partition[0] = ball.px//self.gridsize
            ball.partition[1] = ball.py//self.gridsize
            for x in range(-1,2):
                for y in range(-1,2):
                    ball.partitions.append([ball.partition[0]+x, ball.partition[1]+y])

            if ball.px < 0:
                ball.px += WIDTH
            if ball.px >= WIDTH:
                ball.px -= WIDTH
            if ball.py < 0:
                ball.py += HEIGHT
            if ball.py >= HEIGHT:
                ball.py -= HEIGHT

            if math.fabs(math.pow(ball.vx,2)+math.pow(ball.vy,2) < self.stop_threshold):
                ball.vx = 0
                ball.vy = 0
                ball.is_move = False
            
        for ball in self.ball_list:
            if not ball.is_move:
                continue
            for target in self.ball_list:
                if target.partition not in ball.partitions:
                    continue
                if ball.id != target.id:
                    if DoballsOverlap(ball.px,ball.py,ball.radius,target.px,target.py,target.radius):
                        target.is_move = True
                        vecCollidingPairs.append([ball, target])
                        distance = math.sqrt(math.pow(ball.px-target.px,2)+math.pow(ball.py-target.py,2))
                        overlap = 0.5 * (distance - ball.radius - target.radius)
                        ball.px -= overlap * (ball.px - target.px) / distance
                        ball.py -= overlap * (ball.py - target.py) / distance
                        target.px += overlap * (ball.px - target.px) / distance
                        target.py += overlap * (ball.py - target.py) / distance
                        ball.partition[0] = ball.px//self.gridsize
                        ball.partition[1] = ball.py//self.gridsize
                        target.partition[0] = ball.px//self.gridsize
                        target.partition[1] = ball.py//self.gridsize
                        for x in range(-1,2):
                            for y in range(-1,2):
                                ball.partitions.append([ball.partition[0]+x, ball.partition[1]+y])

        for c in vecCollidingPairs:
            ball_1 = c[0]
            ball_2 = c[1]
            distance = math.sqrt(math.pow(ball_1.px-ball_2.px,2)+math.pow(ball_1.py-ball_2.py,2))
            nx = (ball_2.px - ball_1.px) / distance
            ny = (ball_2.py - ball_1.py) / distance
            tx = -ny
            ty = nx
            dpTan1 = ball_1.vx * tx + ball_1.vy * ty
            dpTan2 = ball_2.vx * tx + ball_2.vy * ty
            dpNorm1 = ball_1.vx * nx + ball_1.vy * ny
            dpNorm2 = ball_2.vx * nx + ball_2.vy * ny
            m1 = (dpNorm1 * (ball_1.mass - ball_2.mass) + 2.0 * ball_2.mass * dpNorm2) / (ball_1.mass + ball_2.mass)
            m2 = (dpNorm2 * (ball_2.mass - ball_1.mass) + 2.0 * ball_1.mass * dpNorm1) / (ball_1.mass + ball_2.mass)
            ball_1.vx = tx * dpTan1 + nx * m1
            ball_1.vy = ty * dpTan1 + ny * m1
            ball_2.vx = tx * dpTan2 + nx * m2
            ball_2.vy = ty * dpTan2 + ny * m2

        for ball in self.ball_list:
            if ball.id == 0:
                pygame.draw.circle(self.screen, (255,255,255), (ball.px, ball.py), ball.radius)
                pygame.draw.circle(self.screen, (255,0,0), (ball.px, ball.py), 1.5)
            else:
                pygame.draw.circle(self.screen, (255,0,0), (ball.px, ball.py), ball.radius)
            pygame.draw.circle(self.screen, (0,0,0), (ball.px, ball.py), ball.radius, 1)
            # for rect in ball.partitions:
            #     pygame.draw.rect(self.screen, (0,0,255),(rect[0]*self.gridsize, rect[1]*self.gridsize, self.gridsize, self.gridsize), 1)
            ball.partitions.clear()
            
            

game = Game(screen)

running = True

clock = pygame.time.Clock()
FPS = 120

while running:
    clock.tick(FPS)
    dt = clock.tick_busy_loop(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((57,130,49))
    game.update(dt)
    pygame.display.update()
pygame.quit()