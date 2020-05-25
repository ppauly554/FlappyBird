import pygame
import random

#setup
pygame.init()
window = pygame.display.set_mode((1000,1000))

#variables
clock = pygame.time.Clock()
run = True

die = pygame.mixer.Sound("assets/audio/sfx_die.wav")
hit = pygame.mixer.Sound("assets/audio/sfx_hit.wav")
point = pygame.mixer.Sound("assets/audio/sfx_point.wav")
swoosh = pygame.mixer.Sound("assets/audio/sfx_swooshing.wav")

paused = True

background_image = pygame.image.load("assets/background/background.png")

pipe_image = pygame.image.load("assets/sprites/pipe/pipe.png")

bird_sprites = [pygame.image.load("assets/sprites/bird/flap.png"), pygame.image.load("assets/sprites/bird/not flap.png")]
angle = 0
flapping = False
angle_cnt = 0
flapped = False
flapped_cnt = 0
wing_bool = False
dead = False
wait = 0
ascending = True

font = pygame.font.Font("assets/flappybird.TTF",72)

points = 0

#class and functions
with open("HighScore.txt", "r") as f: high_score = int(f.read()); f.close()

def pause():
    mask = pygame.Surface((1000,1000), pygame.SRCALPHA)
    mask.fill((128,128,128,128))
    window.blit(mask, (0,0))

backgrounds = [0]
def background_move():
    global backgrounds
    remove = False
    for item in range(len(backgrounds)):
        if not dead and not paused:
            backgrounds[item] -= 10
            if backgrounds[item] == -10: backgrounds.append(980)
            if backgrounds[item] == -1000: remove = True
        window.blit(background_image, (backgrounds[item],0))
    if remove: del backgrounds[0]

pipes = [[1000,random.randint(150,650),100,800]]
def pipe_move():
    global pipes
    remove = False
    for item in range(len(pipes)):
        selected = pipes[item]
        if not dead and not paused:
            selected[0] -= 10
            if selected[0] == 500: pipes.append([1000,random.randint(150,650),100,800])
            if selected[0] == -100: remove = True
        window.blit(pipe_image, (selected[0], selected[1] - 800)); window.blit(pygame.transform.flip(pipe_image, False, True), (selected[0], selected[1] + 200))
    if remove: del pipes[0]

class bird:
    def __init__(self, y):
        self.y = y
    def load(self):
        global flapped, flapped_cnt, wing_bool
        bird_selected = bird_sprites[0]
        if wing_bool: bird_selected = bird_sprites[1]
        if not flapped: wing_bool = not wing_bool
        if flapped_cnt == 15: flapped = not flapped; flapped_cnt = 0
        flapped_cnt += 1
        window.blit(pygame.transform.rotate(bird_selected, angle), (50, self.y))
    def check(self):
        global dead, points, wait
        body = pygame.Rect(50, self.y, 50, 50)
        if not dead:
            for HB in pipes:
                if body.colliderect((HB[0], HB[1] + 200,HB[2],HB[3])) or body.colliderect((HB[0], HB[1] - 800,HB[2],HB[3])): dead = True; hit.play()
                if body.colliderect((HB[0] + 150, HB[1], 1, 200)):
                    wait += 1
                    if wait == 4:
                        points += 1
                        wait = 0
                        point.play()

    '''
    I'm brain dead when it comes to
    velocity and jump calculations
    so enjoy my janky code
    '''
    def fall(self):
        global run, angle
        if dead: self.y += 50
        else: self.y += 10
        if self.y >= 1000: run = False
        angle = -45
    def flap(self):
        if self.y >= -25: self.y -= 70

def score_board():
    scoreboard = font.render(f"""Score: {points} HighScore: {high_score}""", True, (255,255,0))
    scoreboard_rect = scoreboard.get_rect(center=(500, 50))
    window.blit(scoreboard, scoreboard_rect)

bird = bird(450)

#main loop
while run:
    clock.tick(60)
    pygame.display.flip()
    window.fill((255,255,255))

    background_move()
    pipe_move()
    bird.check()
    bird.load()
    score_board()

    if points > high_score:
        high_score = points

    if not paused:
        bird.fall()
        if flapping:
            angle_cnt += 1
            angle = 45
            if angle_cnt == 5: angle_cnt = 0; flapping = False
        if dead:
            if ascending: ascending = not ascending; bird.flap();die.play()
    else:
        pause()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: paused = not paused
            elif event.key == pygame.K_F11:
                with open("HighScore.txt", "w") as f: f.write("0"); f.flush(); f.close()
            elif event.key == pygame.K_SPACE:
                if not dead:
                    if not paused: bird.flap(); flapping = True; swoosh.play()
                    else: paused = not paused
if points >= high_score:
    with open("HighScore.txt","w") as f: f.write(str(points)); f.flush(); f.close()
pygame.quit()