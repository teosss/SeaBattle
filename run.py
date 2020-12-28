from add.login import *
from PIL import ImageTk, Image as PILimage
from tkinter import messagebox
import random

# class Сoordinate():
#   def __init__(self, x = 0, y = 0):
#        self.x = x
#        self.y = y
   
class Player():
    def __init__(self, name_1, name_2):
        self.name_1 = name_1
        self.name_2 = name_2

GAME = Tk()

game_window = Сoordinate(400, 400)          # розмір вікна
field_size = Сoordinate(zone, zone)         # розмір поля для гри
step = Сoordinate()                         # крок для поля
menu = Сoordinate()                         # розмір і параметри меню
player_zone = Сoordinate()                  # зона для взаємодії в межах сітки  
players = Player(login_name_1, login_name_2)# зараємо імена гравців

game_running = True
move_player = False

step.x = game_window.x // field_size.x  # задаємо крок по горизонталі
step.y = game_window.y // field_size.y  # задаємо крок по вертикалі

game_window.x = step.x * field_size.x   # вирівнюємо розмір вікна відповідно до розміру поля
game_window.y = step.y * field_size.y   # 

delta_menu_x = field_size.x            # ширина у кроках відділу де меню

water_color = "#7FC9FF"                # Кольори
grey_color = "#AAAAAA"                 #
win_color = "#FFD800"                  #
black_color = "black"                  #
red_color = "red"                      #

player_1_boom = 0                       # ініціалізуємо кількість попадань 1 гравця
player_2_boom = 0                       # ініціалізуємо кількість попадань 2 гравця
next_step = 1                           # лічильник ходу гри
ship_total = 0                          # кількість клітинок кораблів

menu.x = step.x * delta_menu_x          # розмір меню по ширині
menu.y = 40                             # розмір меню по висоті 
offset_x = game_window.x + menu.x

ships = field_size.x // 2               # Визначаємо максимальну кількість кораблів:
ship_len1 = 1           # довжина першого типу корабля
ship_len2 = 2           # довжина другого типу корабля
ship_len3 = 3           # довжина третього типу корабля

img = PILimage.open(r"images\fire.gif")
img = img.resize((step.x,step.y), PILimage.ANTIALIAS)
fire_img =  ImageTk.PhotoImage(img)


enemy_ships1 = [[0 for i in range(field_size.x + 1)] for i in range(field_size.y + 1)]

enemy_ships2 = [[0 for i in range(field_size.x + 1)] for i in range(field_size.y + 1)]

list_objects = []       # список об'єктів canvas
list_objects_show = []  # список згенерованих кораблів які можна підглянути

points1 = [[-1 for i in range(field_size.x)] for i in range(field_size.y)] # points1 - Визначає куди натиснули мишкою  в поле 1

points2 = [[-1 for i in range(field_size.x)] for i in range(field_size.y)] # points2 - Визначає куди натиснули мишкою в поле 2


ships_list = []      # ships_list - список кораблів першого і другого гравця

def game_close():
    """
    Функція для виходу з гри через Х
    """                   
    global game_running
    if messagebox.askokcancel("Sea Battle | EXIT", "Бажаєте вийти з гри?"):
        game_running = False
        GAME.destroy()

GAME.iconbitmap(icon_location) 
GAME.protocol("WM_DELETE_WINDOW", game_close)     # функція на вихід з гри
GAME.title("Sea Battle | Game")                   # назва гри
GAME.resizable(0, 0)                              # параметер на зміну розміру вікна
GAME.wm_attributes("-topmost", 1)                 # параметер по видимсть поверх інших вікон
canvas = Canvas(GAME, width=game_window.x + menu.x + game_window.x, height=game_window.y + menu.y, bd=0, highlightthickness=0) 
# задаємо основу для ігрового вікна
zone1 = canvas.create_rectangle(0, 0, game_window.x, game_window.y, fill=water_color)  # Поле гравця 1                           
zone2 = canvas.create_rectangle(game_window.x + menu.x, 0, game_window.x + menu.x + game_window.x, game_window.y,fill=water_color)                                      # Поле гравця 2
canvas.pack()
GAME.update()


def draw_table(offset_x=0):                        # функція створює лінії вертикальні й горизонтальні
    """
    Функція для рисування ліній полів
    """  
    for i in range(0, field_size.x + 1):
        canvas.create_line(offset_x + step.x * i, 0, offset_x + step.x * i, game_window.y)
    for i in range(0, field_size.y + 1):
        canvas.create_line(offset_x, step.y * i, offset_x + game_window.x, step.y * i)

draw_table()                            # малюємо лінії для першого поля      
draw_table(game_window.x + menu.x)      # малюємо лінії для другого поля




def turn_player(igrok_mark_1):
    """
    Функція для графічного розроділення ходів активного і пасивного гравця
    """  
    if  igrok_mark_1:
        t0.configure(fg=red_color)
        t1.configure(fg=grey_color)
        canvas.itemconfig(zone2,fill=grey_color)
        canvas.itemconfig(zone1,fill=water_color)                                                      
    else:
        t1.configure(fg=red_color)
        t0.configure(fg=grey_color)
        canvas.itemconfig(zone2,fill=water_color)
        canvas.itemconfig(zone1,fill=grey_color)                              

def button_show_enemy():               # функція для дебагу (відобразити кораблі 1 гравця)
    """
    Функція для відображення розташування кораблів гравця 1
    """  
    b1.configure(state=NORMAL)
    b0.configure(state=DISABLED)
    for i in range(0, field_size.x):   
        for j in range(0, field_size.y):
            if enemy_ships1[j][i] > 0:
                color = red_color
                if points1[j][i] != -1:
                    color = black_color
                _id = canvas.create_rectangle(i * step.x, j * step.y, i * step.x + step.x, j * step.y + step.y, fill=color)
                list_objects_show.append(_id)
            if enemy_ships2[j][i] > 0:
                color = red_color
                if points2[j][i] != -1:
                    color = black_color
                _id = canvas.create_rectangle(game_window.x + menu.x + i * step.x, j * step.y,
                                              game_window.x + menu.x + i * step.x + step.x, j * step.y + step.y,
                                              fill=color)
                list_objects_show.append(_id)


def button_del_show_enemy():            # функція для дебагу (відобразити кораблі 2 гравця)
    """
    Функція для відображення розташування кораблів гравця 2
    """ 
    b0.configure(state=NORMAL)
    b1.configure(state=DISABLED) 
    for element in list_objects_show:
        try:
            canvas.delete(element)
        except:
            element.destroy()


def button_begin_again():           # функція для перезапуску гри
    """
    Функція для очитки полів від елементів при початку нової гри
    """  
    global list_objects
    global points1, points2
    global next_step
    global enemy_ships1, enemy_ships2
    
    b0.configure(state=NORMAL)
    b1.configure(state=DISABLED)
    
    next_step = 1                         
    Player_turn.configure(text=f"Зараз {next_step} хід")
    
    for element in list_objects:
        try:
            canvas.delete(element)
        except:
            element.destroy()
    for element in list_objects_show:
        try:
            canvas.delete(element)
        except:
            element.destroy()
    list_objects = []
    generate_ships_list()
    enemy_ships1 = generate_enemy_ships()
    enemy_ships2 = generate_enemy_ships()
    points1 = [[-1 for i in range(field_size.x)] for i in range(field_size.y)]
    points2 = [[-1 for i in range(field_size.x)] for i in range(field_size.y)]


b0 = Button(GAME, text=f"Відобразити кораблі гравців", command=button_show_enemy)
b0.place(x=game_window.x + menu.x / 4 + 10, y=30)

b1 = Button(GAME, text=f"Приховати кораблі гравців", state=DISABLED, command=button_del_show_enemy)
b1.place(x=game_window.x + menu.x / 4 + 15, y=70)

b2 = Button(GAME, text="Почати заново", command=button_begin_again)
b2.place(x=game_window.x + menu.x / 4 + 50, y=110)

Player_turn = Label(GAME, text=f"Зараз {next_step} хід", font=("Helvetica", 12))
Player_turn.place(x=game_window.x + menu.x / 4 + 50, y=150)

Generate_ship = Label(GAME, font=("Helvetica", 11))
Generate_ship.place(x=game_window.x + menu.x // 3 + 20 , y=175)

Player_hits_1 = Label(GAME, font=("Helvetica", 10))
Player_hits_1.place(x=game_window.x + 20 , y=200)

Player_hits_2 = Label(GAME, font=("Helvetica", 10))
Player_hits_2.place(x=game_window.x + 20 , y=220)

t0 = Label(GAME, text=players.name_1, font=("Helvetica", 16))
t0.place(x=game_window.x // 2 - t0.winfo_reqwidth() // 2, y=game_window.y + 3)
t1 = Label(GAME, text=players.name_2, font=("Helvetica", 16))
t1.place(x=game_window.x + menu.x + game_window.x // 2 - t1.winfo_reqwidth() // 2, y=game_window.y + 3)

def draw_point(x, y, enemy_ships, offset_x = 0 ):   
    """
    Функція рисує на вибрій клітинці об'єкт для другого гравця
    """ 
    if enemy_ships[y][x] == 0:
        color = "white"
        id1 = canvas.create_rectangle(offset_x + x * step.x, y * step.y, offset_x + x * step.x + step.x, y * step.y + step.y, fill=color)
        list_objects.append(id1)
        return False

    if enemy_ships[y][x] > 0:
        color = red_color
        id1 = canvas.create_rectangle(offset_x + x * step.x, y * step.y, offset_x + x * step.x + step.x, y * step.y + step.y, fill=color)
        id2 = canvas.create_image(offset_x + x * step.x, y * step.y, image=fire_img, anchor=NW)        
        list_objects.append(id1)
        list_objects.append(id2)
        return True

def check_winner(enemy_ships, points):
    """
    Функція перевіряє чи гравець 1 задовільнив умови перемоги
    """  
    win = True
    for i in range(0, field_size.x):
        for j in range(0, field_size.y):
            if enemy_ships[j][i] > 0:
                if points[j][i] == -1:
                    win = False
    return win

def add_to_all(event):
    """
    Функція певіряє, що нажав користувач і реагує на його дії відповідно до правил гри
    """
    global points1, points2, move_player, next_step, offset_x, player_1_boom, player_2_boom
    
    shot = False
    
    _type = 0  # ЛКМ
    
    if event.num == 3:
        _type = 1  # ПКМ
    
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
 
    player_zone.x = mouse_x // step.x
    player_zone.y = mouse_y // step.y

    # перше ігрове поле
    if player_zone.x < field_size.x and player_zone.y < field_size.y and move_player:
        if points1[player_zone.y][player_zone.x] == -1:
            points1[player_zone.y][player_zone.x] = _type
            
            move_player = False
            
            next_step += 1                          # підрахунок ходу гравців
            Player_turn.configure(text=f"Зараз {next_step} хід")
            
            shot = draw_point(player_zone.x, player_zone.y, enemy_ships1)
            if shot == True:
                player_1_boom -= 1
                Player_hits_1.configure(text=f"{players.name_1} -- залишилось {player_1_boom}")
            if check_winner(enemy_ships1, points1):
                move_player = True                
                win_back = canvas.create_rectangle(game_window.x + menu.x, 0, game_window.x + menu.x + game_window.x, game_window.y, fill=water_color)
                win = Label(GAME, text="WIN!",fg=win_color, font=("Helvetica", 60))
                win.configure(bg=water_color)
                win.place(x=game_window.x + menu.x + game_window.x // 3, y=game_window.y // 2.5)
            
                list_objects.append(win_back)
                list_objects.append(win)
                print("Перемога гравця №2")
                points1 = [[10 for i in range(field_size.x)] for i in range(field_size.y)]
                points2 = [[10 for i in range(field_size.x)] for i in range(field_size.y)]

    # друге ігрове поле
    if player_zone.x >= field_size.x + delta_menu_x and player_zone.x <= field_size.x + field_size.x + delta_menu_x and player_zone.y < field_size.y and not move_player:
        if points2[player_zone.y][player_zone.x - field_size.x - delta_menu_x] == -1:
            points2[player_zone.y][player_zone.x - field_size.x - delta_menu_x] = _type
            move_player = True
            
            shot = draw_point(player_zone.x - field_size.x - delta_menu_x, player_zone.y, enemy_ships2, offset_x)
            if shot == True:
                player_2_boom -= 1
                Player_hits_2.configure(text=f"{players.name_2} -- залишилось {player_2_boom}")
            
            # if check_winner(player_zone.x, player_zone.y):
            
            if check_winner(enemy_ships2, points2):
                move_player = False
                win_back = canvas.create_rectangle(0, 0, game_window.x, game_window.y, fill=water_color)
                win = Label(GAME, text="WIN!",fg=win_color, font=("Helvetica", 60))
                win.configure(bg=water_color)
                win.place(x=game_window.x // 3, y=game_window.y // 2.5)
                
                list_objects.append(win_back)
                list_objects.append(win)
                print("Перемога гравця №1")
                points1 = [[10 for i in range(field_size.x)] for i in range(field_size.y)]
                points2 = [[10 for i in range(field_size.x)] for i in range(field_size.y)]

    turn_player(move_player)
    

def generate_ships_list(): # функція генерує кораблів
    """
    Функція генерує список які кораблі використовувати
    """
    global ships_list
    ships_list = []
    for i in range(0, ships):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3]))


def generate_enemy_ships(): 
    """
    Функція генерує кількість і розмішення кораблів
    """
    global ships_list, ship_total, player_1_boom, player_2_boom
    enemy_ships = []

    # підрахунок загальної довжини кораблів
    sum_1_all_ships = sum(ships_list)
    sum_ships = 0


    while sum_ships != sum_1_all_ships:
        # онуляємо масив кораблів 
        enemy_ships = [[0 for i in range(field_size.x)] for i in
                       range(field_size.y)]  

        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)  # 1- горизонтальний 2 - вертикальниї

            primerno_x = random.randrange(0, field_size.x)
            if primerno_x + len > field_size.x:
                primerno_x = primerno_x - len

            primerno_y = random.randrange(0, field_size.y)
            if primerno_y + len > field_size.y:
                primerno_y = primerno_y - len

            # print(horizont_vertikal, primerno_x,primerno_y)
            if horizont_vertikal == 1:
                if primerno_x + len <= field_size.x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записуємо якщо поруч нічого не має
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записуємо номер корабля
                        except Exception:
                            pass
            if horizont_vertikal == 2:
                if primerno_y + len <= field_size.y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записуємо якщо поруч нічого не має
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записуємо номер корабля
                        except Exception:
                            pass

        # підраховуємо кількість
        sum_ships = 0
        for i in range(0, field_size.x):
            for j in range(0, field_size.y):
                if enemy_ships[j][i] > 0:
                    sum_ships = sum_ships + 1
    
    ship_total = sum_ships
    player_1_boom = sum_ships
    player_2_boom = sum_ships
    Player_hits_1.configure(text=f"{players.name_1} -- залишилось {ship_total}")
    Player_hits_2.configure(text=f"{players.name_2} -- залишилось {ship_total}")
    Generate_ship.configure(text=f"Створено {ship_total}")
    return enemy_ships

generate_ships_list()

enemy_ships1 = generate_enemy_ships()
enemy_ships2 = generate_enemy_ships()


canvas.bind_all("<Button-1>", add_to_all)  # ЛКМ
canvas.bind_all("<Button-3>", add_to_all)  # ПКМ

turn_player(move_player)

while game_running:
    if game_running:
        GAME.update_idletasks()
        GAME.update()
    time.sleep(0.005)