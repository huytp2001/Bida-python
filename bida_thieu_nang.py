import pygame, math

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

WIDTH = 930
HEIGHT = 504

pygame.init()
font = pygame.font.Font(None, 14)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Game:
    def __init__(self, screen):
        self.ball_list = list()
        self.selectball = None
        self.clicked = False
        self.screen = screen
        self.force = 15.0
        self.friction = 1.1
        self.stop_threshold = 3.0
        self.selectball_pos = list()
        self.is_draw_line = False
        self.ball_radius = 9
        self.gridsize = self.ball_radius * 2
        self.balls_color = [(255,255,255), (227,210,34), (44,50,212), (255,0,0),(202,70,212),(125,38,212),(38,191,92), (196,108,57), (0,0,0), (227,210,34),(44,50,212),(255,0,0),(202,70,212),(125,38,212),(38,191,92),(196,108,57)]
        self.hole = [[ self.ball_radius/2+4, self.ball_radius/2+4],
                     [ self.ball_radius/2+4, HEIGHT-self.ball_radius/2-4], 
                     [ WIDTH/2-self.ball_radius/2, self.ball_radius/2+2],
                     [ WIDTH/2-self.ball_radius/2, HEIGHT-self.ball_radius/2-2], 
                     [ WIDTH-self.ball_radius/2-4, self.ball_radius/2+4], 
                     [ WIDTH-self.ball_radius/2-4, HEIGHT-self.ball_radius/2-4]]
        
        self.clearTable()
        
    def clearTable(self):
        self.ball_list.clear()
        self.addball(728,242,self.ball_radius,len(self.ball_list))
        self.addball(297,242,self.ball_radius,len(self.ball_list))
        self.addball(282,232,self.ball_radius,len(self.ball_list))
        self.addball(282,251,self.ball_radius,len(self.ball_list))
        self.addball(266,225,self.ball_radius,len(self.ball_list))
        self.addball(267,242,self.ball_radius,len(self.ball_list))
        self.addball(266,260,self.ball_radius,len(self.ball_list))
        self.addball(252,217,self.ball_radius,len(self.ball_list))
        self.addball(252,234,self.ball_radius,len(self.ball_list))
        self.addball(252,251,self.ball_radius,len(self.ball_list))
        self.addball(252,268,self.ball_radius,len(self.ball_list))
        self.addball(237,207,self.ball_radius,len(self.ball_list))
        self.addball(236,226,self.ball_radius,len(self.ball_list))
        self.addball(236,244,self.ball_radius,len(self.ball_list))
        self.addball(236,261,self.ball_radius,len(self.ball_list))
        self.addball(238,280,self.ball_radius,len(self.ball_list))

    def addball(self, x, y, r, id):
        newball = ball(x,y,0,0,0,0,r,r*10,id, [x//self.gridsize, y//self.gridsize])
        self.ball_list.append(newball)

    def update(self, elapse_time):
        DoballsOverlap = lambda x1, y1, r1, x2, y2, r2: abs((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)) <= (r1 + r2)*(r1 + r2)
        is_point_in_ball = lambda x1, y1, r1, px, py: ((x1 - px)**2 + (y1 - py)**2) < r1**2
        
        mouse_event = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_event[0] and not self.clicked:
            for ball in self.ball_list:
                if (is_point_in_ball(ball.px, ball.py, ball.radius, mouse_pos[0], mouse_pos[1])):
                    if ball == self.ball_list[0]:
                        if ball.vx == 0 and ball.vy == 0:
                            self.selectball = ball
                            self.selectball_pos = [self.selectball.px, self.selectball.py]
                            self.is_draw_line = True
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

        vecCollidingPairs = list()

        for ball in self.ball_list:
            if not ball.is_move:
                continue
            ball.ax = -ball.vx * self.friction
            ball.ay = -ball.vy * self.friction

            ball.vx += ball.ax * elapse_time
            ball.vy += ball.ay * elapse_time
            ball.px += ball.vx * elapse_time
            ball.py += ball.vy * elapse_time

            ball.partition[0] = ball.px//self.gridsize
            ball.partition[1] = ball.py//self.gridsize
            for x in range(-1,2):
                for y in range(-1,2):
                    ball.partitions.append([ball.partition[0]+x, ball.partition[1]+y])

            if ball.px < self.ball_radius or ball.px > WIDTH-self.ball_radius:
                ball.vx = -ball.vx
            if ball.py < self.ball_radius or ball.py > HEIGHT-self.ball_radius:
                ball.vy = -ball.vy

            if math.fabs(math.pow(ball.vx,2)+math.pow(ball.vy,2) < self.stop_threshold):
                ball.vx = 0
                ball.vy = 0
                ball.is_move = False

            for hole in self.hole:
                distance = math.sqrt(math.pow(ball.px-hole[0],2)+math.pow(ball.py-hole[1],2))
                if distance <= self.ball_radius * 1.2:
                    if ball == self.ball_list[0]:
                        continue
                    self.ball_list.remove(ball)

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

        for hole in self.hole:
            pygame.draw.circle(self.screen, (39,39,39), (hole[0],hole[1]), self.ball_radius+3)

        for ball in self.ball_list:
            if ball.id == 0:
                pygame.draw.circle(self.screen, self.balls_color[ball.id], (ball.px, ball.py), ball.radius)
                pygame.draw.circle(self.screen, (255,0,0), (ball.px, ball.py), 1.5)
            else:
                text_surface = font.render(f'{ball.id}', True, (255, 255, 255)).convert_alpha()
                text_rect = text_surface.get_rect()
                text_rect.center = (ball.px, ball.py)
                pygame.draw.circle(self.screen, self.balls_color[ball.id], (ball.px, ball.py), ball.radius)
                self.screen.blit(text_surface, text_rect)
            pygame.draw.circle(self.screen, (0,0,0), (ball.px, ball.py), ball.radius, 1)
            ball.partitions.clear()

game = Game(screen)

running = True

clock = pygame.time.Clock()
FPS = 240

while running:
    clock.tick(FPS)
    dt = clock.tick_busy_loop(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.clearTable()

    screen.fill((57,130,49))
    game.update(dt)
    pygame.display.update()
pygame.quit()