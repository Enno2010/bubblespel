from tkinter import *
from random import randint
from time import sleep, time
from math import sqrt

HEIGHT = 500
WIDTH = 800

SHIP_R = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
SHIP_SPD = 10
score = 0
#nuttige dingen
BUB_CHANCE = 10
TIME_LIMIT = 30
running = True
BONUS_SCORE = 1000
score = 0
bonus = 0
levens = 10
end = time() + TIME_LIMIT
bub_id = list()
bullet_id = list()
bub_r = list()
bub_speed = list()
MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPD = 10
GAP = 100

def show_levens(levens):
    c.itemconfig(levens_text, text=str(levens))

def show_score(score):
    c.itemconfig(score_text, text=str(score))

def show_time(time_left):
    c.itemconfig(time_text, text=str(time_left))

def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id, 0, -SHIP_SPD)
        c.move(ship_id2, 0, -SHIP_SPD)
    elif event.keysym == 'Down':
        c.move(ship_id, 0, SHIP_SPD)
        c.move(ship_id2, 0, SHIP_SPD)
    elif event.keysym == 'Left':
        c.move(ship_id, -SHIP_SPD, 0)
        c.move(ship_id2, -SHIP_SPD, 0)
    elif event.keysym == 'Right':
        c.move(ship_id, SHIP_SPD, 0)
        c.move(ship_id2, SHIP_SPD, 0)

def shoot(event):
    if event.keysym == 'space':
        create_bullet()
        print("Spatie")

def handle_keys(event):
    move_ship(event)
    shoot(event)

def create_bullet():
    x, y = get_coords(ship_id)
    id1 = c.create_rectangle(x + 20, y - 1, x + 30, y + 1, outline='black', fill='black')
    bullet_id.append(id1)


#maakt bubbels
def create_bubble():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)
    color = 'white'
    colorValue = randint(0,10)
    if colorValue == 9:
        color = 'red'
    if colorValue == 8:
        color = 'yellow'
    #if colorValue == 7:
        #color = 'Green'
    if colorValue == 6:
        color = 'Orange'
    if colorValue == 5:
        color = 'Blue'
    if colorValue == 4:
        color = 'Violet'
    #if colorValue == 3:
        #color = 'Pink'
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline=color) #fill='yellow')
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPD))

def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)

def move_bullets():
    for i in range(len(bullet_id)):
        c.move(bullet_id[i], 10, 0)

def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x, y

def del_bubble(i):
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i])
    del bub_id[i]

def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x, y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)

def del_bullet(i):
    c.delete(bullet_id[i])
    del bullet_id[i]

def clean_up_bullets():
    for i in range(len(bullet_id)-1, -1, -1):
        x, y = get_coords(bullet_id[i])
        if x > WIDTH + GAP:
            del_bullet(i)

def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def collision():
    levens = 0  
    for bub in range(len(bub_id)-1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]):
            levens = -1
            del_bubble(bub)
    return levens

def hit():
    points = 0  
    for bub in range(len(bub_id)-1, -1, -1):
        for i in range(len(bullet_id)-1,-1,-1):
            if distance(bullet_id[i], bub_id[bub]) < (bub_r[bub]):
                points += (bub_r[bub]  + bub_speed[bub])
                del_bubble(bub)
                del_bullet(i)
    return points

def sluitaf():
    global running
    running = False

#Initialisatie
print("Begin van het spel")
window = Tk()
window.protocol("WM_DELETE_WINDOW", sluitaf)
window.title('Bellenschieter')
c = Canvas(window, width=WIDTH, height=HEIGHT, bg='DarkBlue')
c.pack()
c.bind_all('<Key>', handle_keys)
c.bind_all('<KeyPress>', handle_keys)

ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
ship_id2 = c.create_oval(0, 0, 30, 30, outline='red')
#maakt de time en de score
c.create_text(50, 30, text='TIJD', fill='white' )
c.create_text(150, 30, text='SCORE', fill='White' )
c.create_text(150, 30, text='LEVENS', fill='White' )
time_text = c.create_text(50, 50, fill='white' )
score_text = c.create_text(150, 50, fill='white' )
levens_text = c.create_text(250, 50, fill='white' )
#MAIN GAME LOOP
while levens > 0 and running:
    if randint(1, BUB_CHANCE) == 1:
        create_bubble()
    move_bubbles()
    move_bullets()
    clean_up_bubs()
    clean_up_bullets()
    score += hit()
    levens += collision()
    if (int(score / BONUS_SCORE)) > bonus:
        bonus += 1
        end += TIME_LIMIT
    show_levens(levens)
    show_score(score)
    show_time(int(end - time()))
    window.update()
    sleep(0.01)
#maakt einde van spel
end = time() + TIME_LIMIT
c.create_text(MID_X, MID_Y, \
    text='GAME OVER' , fill='white' , font=('Helvetica' ,30))
c.create_text(MID_X, MID_Y + 30, \
    text='Score: '+ str(score),fill='white')
c.create_text(MID_X, MID_Y + 45, \
    text='Bonus time: '+ str(bonus*TIME_LIMIT), fill='white')
c.create_text(MID_X, MID_Y + 60, \
    text='Levens: '+ str(levens),fill='white')
#sleep(3)
