from OpenGL.GL import*
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys
import random
import pygame
############################################
#constants
window_width = 900
window_height = 700
level = 1
count = 0
score = 0
heart_score = 2
theta = 0
rocket_up = -280
center_chick_x_l3 = 450
center_chick_y_l3 = 350

#dimensions
heart_width = heart_height = 20
chicken_width = chicken_height = 80
missile_width = 25
missile_height = 40
egg_width = 50
egg_height = 55
rocket_width = rocket_height = 45
player_x = window_width // 2
player_y = 50

#states
game_over = False
show_poster = True
game_started = False
level_end = False
start_level = True
rocket_heart = rocket_egg = missile_chicken1 = missile_chicken2 = False

# lists
chicken = []
chicken2 = []
missiles = []
eggs = []
hearts = []

#speeds
player_speed = 20
egg_speed = 2
missile_speed = 10
chicken_speed = 3
heart_speed = 3.5
##########################################
#graphics_helpers
def init():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    loadTextures()
    glClearColor(.5, 0, 1, .5)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)


texture_names = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGBA,#Transperancy
                 width, height,
                 0,
                 GL_RGBA,#Error like down to string
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)

def loadTextures():
    glEnable(GL_TEXTURE_2D)
    images = []
    images.append(pygame.image.load("rocket.png"))
    images.append(pygame.image.load("chicken1.png"))
    images.append(pygame.image.load("chicken invaders poster.png"))
    images.append(pygame.image.load("button_play.png"))
    images.append(pygame.image.load("fire3.png"))
    images.append(pygame.image.load("background-3.jpg"))
    images.append(pygame.image.load("egg.png"))
    images.append(pygame.image.load("game_over.png"))
    images.append(pygame.image.load("heart.png"))
    images.append(pygame.image.load("winner.png"))
    textures = [pygame.image.tostring(image, "RGBA", True)
                for image in images]
    glGenTextures(len(images), texture_names)
    for i in range(len(images)):
        texture_setup(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())
               #########################################
                             #keyboard#
               #########################################
def keyboard_char(key, x, y):
    global show_poster, game_started, player_x, player_y, missiles

    if key == b"q":
        sys.exit(0)
    elif key == b"p":  # Press 'p' to toggle play/pause
        if not game_started:
            show_poster = False
            game_started = True
        else:
            show_poster = False
    elif game_started: # If the game is started
        if key == b' ':  # Spacebar to shoot
            missiles.append([player_x, player_y + rocket_height])

def keyboard_moving(key, x, y):
    global game_started, player_x, player_y
    if game_started: # If the game is started
        if key == GLUT_KEY_LEFT:# Left arrow key
            player_x -= player_speed
        elif key == GLUT_KEY_RIGHT:  # Right arrow key
            player_x += player_speed
        elif key == GLUT_KEY_UP:  # Up arrow key
            player_y += player_speed
        elif key == GLUT_KEY_DOWN:  # Down arrow key
            player_y -= player_speed

                   #############################################
                                     #drawing#
                   ############################################
def draw_object(x, y, width, height, index):
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[index])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2d(x - width, y - height)
    glTexCoord2f(0, 1)
    glVertex2d(x - width, y + height)
    glTexCoord2f(1, 1)
    glVertex2d(x + width, y + height)
    glTexCoord2f(1, 0)
    glVertex2d(x + width, y - height)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)

def draw_screen(index):
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, texture_names[index])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2d(0, 0)
    glTexCoord2f(0, 1)
    glVertex2d(0, window_height)
    glTexCoord2f(1, 1)
    glVertex2d(window_width, window_height)
    glTexCoord2f(1, 0)
    glVertex2d(window_width, 0)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)


                     #########################################
                                       #Generation
                    #########################################

def generate_hearts():
    global hearts
    hearts = [[random.randint(20, window_width - 20), window_height] for _ in range(1)]
def generate_chickens():
    global chicken, chicken2
    if level == 1:
        chicken = [[random.randint(50, 500), random.randint(250, 550)] for _ in range(10)]
    if level == 2:
        chicken = [[x, x + 300] for x in range(-300, 120, 80)]
        chicken2 = [[x, -x + 1100] for x in range(1100, 680, -80)]
    if level == 3:
        chicken = [[200 * np.cos(x * 3.14 / 180) + center_chick_x_l3, 200 * np.sin(x * 3.14 / 180) + center_chick_y_l3] for x in range(0, 360, 20)]

def generate_eggs():
    global eggs, chicken
    k = random.randint(1, 4)
    for i in range(k):
        if len(chicken) != 0:
            chick = random.choice(chicken)
            eggs.append([chick[0], chick[1]])

              ##############################################
                                  #text#
              ##############################################
def drawText(string, x, y):
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(0.1, 0.1, 1)
    string = string.encode()
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()

            ##########################################################
                               #next level control
            ##########################################################
def next_level():
    global rocket_up, level_end, level, player_x, player_y, start_level

    if level_end and level != 4:
        glClear(GL_COLOR_BUFFER_BIT)
        rocket_up += 10
        #draw rocket_up
        draw_object(400, -100 + rocket_up, 50, 100, 0)
        winner_sound.play()
    if rocket_up >= window_height+100:
        level += 1
        start_level = True
        rocket_up = -280
        level_end = False
#######################################
def check_collision(object1_x, object1_y, width1, height1, object2_x, object2_y, width2, height2, flag):
    global rocket_heart, rocket_egg, missile_chicken1, missile_chicken2, heart_score, player_x, player_y, game_over
    # chicken && player collision
    if (object1_x + width1 >= object2_x - width2
            and object1_x - width1 <= object2_x + width2
            and object1_y + height1 >= object2_y - height2
            and object1_y - height1 <= object2_y + height2):
        # heart_rocket collision
        if flag == 0:
            rocket_heart = True
        # player_rocket and  collision
        if flag == 1:
            player_x -= 100
            player_y -= 100
            heart_score -= 1
            if heart_score <= 0:
                game_over = True

        if flag == 2:
            rocket_egg = True
        if flag == 3:
            missile_chicken1 = True
        if flag == 4:
            missile_chicken2 = True

def draw_game():
    global game_over, show_poster, game_started, level_end, start_level, level, count, eggs, collision
    glClear(GL_COLOR_BUFFER_BIT)
    #draw background
    draw_screen(5)
    if show_poster:
        #draw_poster
        draw_screen(2)
        #draw button
        draw_object(235, 305, 40, 25, 3)
    if not level_end and not show_poster and level != 4:
        if start_level:
            generate_chickens()
            generate_hearts()
            start_level = False
        if count >= 350:
            eggs = []
            generate_eggs()
            count = 0
        count += 1
        #draw player
        draw_object(player_x, player_y, rocket_width, rocket_height, 0)
        for chick in chicken:
            #draw chick
            draw_object(chick[0], chick[1], chicken_width/2, chicken_height/2, 1)
        if level == 2:
            for chick in chicken2:
                # draw chick
                draw_object(chick[0], chick[1], chicken_width/2, chicken_height/2, 1)

        for missile in missiles:
            # draw missile
            draw_object(missile[0], missile[1], missile_width/2, missile_height/2, 4)
        for heart in hearts:
            # draw heart
            draw_object(heart[0], heart[1], heart_width/2, heart_height/2, 8)
        for egg in eggs:
            # draw egg
            draw_object(egg[0], egg[1], egg_width/2, egg_height/2, 6)
                        #############text####################
        drawText("Score: " + str(score), 10, window_height - 30)
        drawText("Level: " + str(level), window_width - 150, window_height - 30)
        drawText("Score heart: " + str(heart_score), 10, window_height - 50)

    if len(chicken) == 0 and len(chicken2) == 0 and not show_poster:
        level_end = True
        next_level()
    if game_over:
        glClear(GL_COLOR_BUFFER_BIT)
        # draw gameover
        draw_screen(7)
    if level == 4:
        glClear(GL_COLOR_BUFFER_BIT)
        #draw winner
        draw_screen(9)
    glutSwapBuffers()

                ##################################################
                                #update
                ##################################################
def update(value):
    global player_x, chicken, missiles, eggs, score, level, game_over, chicken_speed, level_end, chicken2, show_poster, heart_score, hearts, heart_speed,\
        theta, player_y, rocket_heart, rocket_egg, missile_chicken1, missile_chicken2
    # Move hearts
    for heart in hearts:
        heart[1] -= heart_speed

    # Check for heart collection
    for heart in hearts:
        # for flag = 0
        check_collision(player_x, player_y, rocket_width, rocket_height, heart[0],
                        heart[1], heart_width/2, heart_height/2, 0)
        if rocket_heart:
            hearts.remove(heart)
            heart_score += 1

    # Move chickens
    if level == 1:
        for chick in chicken:
            chick[0] += chicken_speed
            # chick and wall
            if chick[0] >= window_width - chicken_width / 2 or chick[0] <= chicken_width / 2:
                chicken_speed = -(.5)*chicken_speed
            # chick && player collision
            #for flag = 1
            check_collision(player_x, player_y, rocket_width, rocket_height, chick[0], chick[1], chicken_width/2, chicken_height/2, 1)


    if level == 2:
        for chick in chicken:
            if chicken[0][0] >= 200:
                chicken_speed = 0
            else:
                chicken_speed = 5
            if chick[1] <= 500:
                chick[0] += chicken_speed
                chick[1] += chicken_speed
            else:
                chick[0] += chicken_speed
            # chick && player collision
            # for flag = 1
            check_collision(player_x, player_y, rocket_width, rocket_height, chick[0], chick[1], chicken_width/2, chicken_height/2, 1)


        for chick in chicken2:
            if chicken2[0][0] <= 540:
                chicken_speed = 0
            else:
                chicken_speed = 5
            if chick[1] <= 400:
                chick[0] -= chicken_speed
                chick[1] += chicken_speed
            else:
                chick[0] -= chicken_speed
            # chick && player collision
            # for flag = 1
            check_collision(player_x, player_y, rocket_width, rocket_height, chick[0],
                            chick[1], chicken_width/2, chicken_height/2, 1)

    if level == 3:
        # moving
        for chick in chicken:
            if (chick[0] - center_chick_x_l3) > 0 and (chick[1] - center_chick_y_l3) > 0:
                theta = np.arctan((chick[1] - center_chick_y_l3) / (chick[0] - center_chick_x_l3)) * (180 / 3.14)
                print(1)
            elif (chick[0] - center_chick_x_l3) < 0 and (chick[1] - center_chick_y_l3) > 0:
                theta = 180 - (np.arctan((chick[1] - center_chick_y_l3) / -(chick[0] - center_chick_x_l3)) * (180 / 3.14))
                print(2)
            elif (chick[0] - center_chick_x_l3) < 0 and (chick[1] - center_chick_y_l3) < 0:
                theta = 180 + (np.arctan(-(chick[1] - center_chick_y_l3) / -(chick[0] - center_chick_x_l3)) * (180 / 3.14))
                print(3)
            elif (chick[0] - center_chick_x_l3) > 0 and (chick[1] - center_chick_y_l3) < 0:
                theta = 360 - (np.arctan(-(chick[1] - center_chick_y_l3) / (chick[0] - center_chick_x_l3)) * (180 / 3.14))
                print(4)
            theta += 1
            chick[0] = 200 * np.cos(theta * (3.14 / 180)) + center_chick_x_l3
            chick[1] = 200 * np.sin(theta * (3.14 / 180)) + center_chick_y_l3
            # chick && player collision
            # for flag = 1
            check_collision(player_x, player_y, rocket_width, rocket_height, chick[0], chick[1], chicken_width/2, chicken_height/2, 1)


    # Move missiles
    for missile in missiles:
        missile[1] += missile_speed

    # Move eggs
    for egg in eggs:
        egg[1] -= egg_speed
        # collision egg &&player
        #flag = 2
        check_collision(player_x, player_y, rocket_width, rocket_height, egg[0], egg[1], egg_width/2, egg_height/2, 2)
        if rocket_egg:
            rocket_egg = False
            eggs.remove(egg)
            heart_score -= 1
            if heart_score <= 0:
                game_over = True

    # Check for missile-chick collisions
    for missile in missiles:
        for chick in chicken:  # edit
            # chick && missile collision
            # for flag = 3
            check_collision(missile[0], missile[1], missile_width/2, missile_height/2, chick[0], chick[1], chicken_width/2, chicken_height/2, 3)
            if missile_chicken1:
                missile_chicken1 = False
                chicken.remove(chick)
                if missile in missiles:
                    missiles.remove(missile)
                score += 10
        for chick in chicken2:
            # chick && missile collision
            # for flag = 4
            check_collision(missile[0], missile[1], missile_width / 2, missile_height / 2, chick[0], chick[1], chicken_width / 2, chicken_height / 2, 4)
            if missile_chicken2:
                missile_chicken2 = False
                chicken2.remove(chick)
                if missile in missiles:
                    missiles.remove(missile)
                score += 10

    if game_over:
        game_over_sound.play()

    glutPostRedisplay()
    glutTimerFunc(20, update, 0)


               ######################################
                               #sound
               ######################################
def sound():
    global chicken, eggs, background_sound,  winner_sound, game_over_sound, game_over
    import pygame.mixer

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load sound files
    background_sound = pygame.mixer.Sound("Backgroundsound.mp3")
    winner_sound = pygame.mixer.Sound("Chicken Invaders 4 OST Mission Complete.mp3")
    game_over_sound = pygame.mixer.Sound("Chicken Invaders 4 OST Game Over.mp3")

    # Set volume for each sound
    background_sound.set_volume(0.1)
    winner_sound.set_volume(0.6)
    game_over_sound.set_volume(1)
    # In your main function, start playing the background sound
    background_sound.play(-1)  # -1 plays the sound indefinitely

def main():
    sound()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Chicken Invaders")
    glutDisplayFunc(draw_game)
    glutTimerFunc(1, update, 0)
    glutKeyboardFunc(keyboard_char)
    glutSpecialFunc(keyboard_moving)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()