import asyncio
import pygame as pg
import random, time

pg.init()
clock = pg.time.Clock()
wave = 1

black = (0, 0, 0)
white = (255, 255, 255)

win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Falling Debris')

font = pg.font.Font(None, 30)
speed = 4
score = 0
running = True

player_size = 60
player_pos = [win_width / 2, win_height - player_size]  # 400, 600-40
player_image = pg.image.load('./assets/images/blaze.jpg')
player_image = pg.transform.scale(player_image, (player_size, player_size))  # 40,40

obj_size = 30
obj_data = []     # List to store object positions and their images

bg_image = pg.image.load('./assets/images/fort.jfif')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))


def create_object(obj_data):
    if len(obj_data) < 5 and random.random() < 10:    
        x = random.randint(0, win_width - obj_size)
        y = 0

        if random.random() < 0.9:
            obj = pg.image.load('./assets/images/ice.png')
        else:
            obj = pg.image.load('./assets/images/cod.png')
        obj = pg.transform.scale(obj, (obj_size, obj_size))
        obj_data.append([x, y, obj])
       

def update_objects(obj_data):
    global score, wave

    for object in obj_data:
        x, y, image_data = object
        if y < win_height:
            y += (speed + wave)
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            score += 1
            wave = score//10


def collision_check(obj_data, player_pos):
    global running
    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            time.sleep(1)
            running = False
            break

async def main():
    global running, player_pos
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                x, y = player_pos[0], player_pos[1]
                if event.key == pg.K_LEFT:
                    x -= 20
                elif event.key == pg.K_RIGHT:
                    x += 20
                player_pos = [x, y]

        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Score: {score}'
        text = font.render(text, 10, white)
        screen.blit(text, (win_width - 200, win_height - 40))
        wtext = f'Wave: {wave}'
        wtext = font.render(wtext, 10, white)
        screen.blit(wtext, (win_width - 200, win_height - 60))

        create_object(obj_data)
        update_objects(obj_data)
        collision_check(obj_data, player_pos)

        clock.tick(30)
        pg.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())