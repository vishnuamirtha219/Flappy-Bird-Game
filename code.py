import pygame
from random import randint
gw, gh = 551, 720
bx, by = 30, 300
bird_timer = 0
bird_index = 0
pipes = []
pipe_timer = 0
delay = 180
intro = True
ground_x = 0
pipe_x , top_pipe_y, bot_pipe_y, gap = 0, 0, 0, 130
gravity = 0.2
velocity = 0
score = 0 
game_over = False

screen = pygame.display.set_mode((gw, gh))
pygame.display.set_caption("flappybird")

bg = pygame.image.load("background.png")
gnd = pygame.image.load("ground.png")
top_pipe = pygame.image.load("pipe_top.png")
bot_pipe = pygame.image.load("pipe_bottom.png")
b1 = pygame.image.load("bird_up.png")
b2 = pygame.image.load("bird_mid.png")
b3 = pygame.image.load("bird_down.png")
start = pygame.image.load("start.png")
end = pygame.image.load("game_over.png")

bird_list = [b1, b2, b3]

def ground():
    global ground_x
    screen.blit(gnd, (ground_x, 500))
    screen.blit(gnd, (ground_x + 551, 500)) 
    if ground_x <= -551:
        ground_x = 0
    ground_x -= 1
def bird_flap():
    global bird_timer, bird_index, bx, by
    bird_timer+= .5
    if bird_timer >= 5:
        bird_index+=1  # default bird_index = 0  0 = 0
        bird_timer = 0
        if bird_index == 3:
            bird_index = 0
    screen.blit(bird_list[bird_index], (bx, by))

def pipes_create():
    global pipes, pipe_timer, score
    pipe_rects = []
    if pipe_timer <=0:
        top_pipe_y = randint(-600, -480)
        bot_pipe_y = 800 + top_pipe_y + gap
        pipes.append([gw, top_pipe_y, "top", False])
        pipes.append([gw, bot_pipe_y, "bot", False])
        pipe_timer = delay
    pipe_timer -= 1
    new_pipes = []
    for p in pipes:
        x, y, t, passed = p
        if t == "top":
            rect = top_pipe.get_rect(topleft=(x, y))
            screen.blit(top_pipe, (x, y))
        else:
            rect = bot_pipe.get_rect(topleft=(x, y))
            screen.blit(bot_pipe, (x, y))
            if x + bot_pipe.get_width() <= bx and not passed and not game_over:  
                score += 1
                passed = True        
        pipe_rects.append(rect)
        new_pipes.append([x-1, y, t, passed])
    pipes = new_pipes 
    return pipe_rects

while True:
    keys = pygame.key.get_pressed()   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.blit(bg, (0, 0))
    if intro:
        ground()
        bird_flap()
        screen.blit(start, (184, 150))
        if keys[pygame.K_SPACE]:
            intro = False
    else:
        pipe_rects = pipes_create()
        ground()
        if keys[pygame.K_SPACE]:
            velocity = -2.5
        velocity += gravity
        by += velocity
        bird_flap()
        bird_rect = bird_list[bird_index].get_rect(topleft=(bx, by))
        for rect in pipe_rects:
            if bird_rect.colliderect(rect):
                game_over = True
        if by >= 500: # ground level 
            game_over = True
    if game_over:
        by += 10
        if keys[pygame.K_r]:
            bx, by = 30, 300
            bird_timer = 0
            bird_index = 0
            pipes = []
            pipe_timer = 0
            intro = True
            ground_x = 0
            pipe_x , top_pipe_y, bot_pipe_y, gap = 0, 0, 0, 130
            velocity = 0
            score = 0 
            game_over = False
        screen.blit(end, (184, 150))        
    pygame.display.flip()