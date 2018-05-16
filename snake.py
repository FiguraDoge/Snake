import sys
import pygame
import random

########################### Global Constants ##############################
AUTHOT = 'Chengjia Wu'
block_size = 20
width = 1600
height = 900
initial_snake_length = 10
number_columns = width / block_size
number_rows = height / block_size
FPS = 15
DRAW_GRID = False
###########################################################################


def get_initial_snake_player1(snake_length , number_columns , number_rows , two_player):
        snake_list_player1 = []
        if two_player :
                head_x = number_columns // 2
                head_y = number_rows // 3
        else:
                head_x = number_columns // 2
                head_y = number_rows // 2
                
        for i in range (snake_length):
                snake_body = (head_x - i, head_y)
                snake_list_player1.append(snake_body)
        snake_list_player1.reverse()
        return(snake_list_player1)

def get_initial_snake_player2(snake_length , number_columns , number_rows):
        snake_list_player2 = []
        head_x = number_columns // 2
        head_y = number_rows // 1.25
        for i in range (snake_length):
                snake_body = (head_x + i, head_y)
                snake_list_player2.append(snake_body)
        snake_list_player2.reverse()
        return(snake_list_player2)

def pick_random_apple_position_one(snake_list , number_columns , number_rows):
                while True:
                        apple_x = random.randint(0 , number_columns - 1)
                        apple_y = random.randint(0 , number_rows - 1)
                        if ((apple_x,apple_y) not in snake_list):
                                return[apple_x , apple_y]

def pick_random_apple_position_two(snake_list_player1 , snake_list_player2 , buff_position , number_columns , number_rows):
        while True:
                        apple_x = random.randint(0 , number_columns - 1)
                        apple_y = random.randint(0 , number_rows - 1)
                        if ((apple_x,apple_y) not in snake_list_player1) and ((apple_x,apple_y) not in snake_list_player2)and ([apple_x , apple_y] != buff_position):
                                return[apple_x , apple_y]
        
def update_direction (current_direction , new_direction):
        if (current_direction[0] != new_direction[0] * -1) and (current_direction[1] != new_direction[1] * -1) :
                current_direction = new_direction
        return(current_direction)

def update_snake(snake_list , current_direction, apple_position):
        snake_head = list(snake_list[-1])
        snake_head[0] += current_direction[0]
        snake_head[1] += current_direction[1]
        
        if (snake_head == apple_position) :
                snake_list.append(tuple(apple_position))
                apple_eaten = True
        else:
                snake_list.append(tuple(snake_head))
                del(snake_list[0])
                apple_eaten = False
        return (snake_list , apple_eaten)

def update_buff(snake_list_player , buff_position):
        snake_head = snake_list_player[-1]
        if snake_head == tuple(buff_position):
                return(True)
        else:
                return(False)
        
def not_snake_inside_window(snake_list , number_columns , number_rows):
        snake_head_x = snake_list[-1][0]
        snake_head_y = snake_list[-1][1]
        if (snake_head_x >= number_columns) or (snake_head_x < 0) or (snake_head_y >= number_rows) or (snake_head_y < 0) :
                return(True)
        return(False)

def snake_go_through_window(snake_list , number_columns , number_rows):
        snake_head_x = snake_list[-1][0]
        snake_head_y = snake_list[-1][1]
        if snake_head_x >= number_columns:
                snake_head_x = 0
        if snake_head_x < 0:
                snake_head_x = number_columns -1
        if snake_head_y >= number_rows:
                snake_head_y = 0
        if snake_head_y < 0:
                snake_head_y = number_rows - 1
        snake_list[-1] = (snake_head_x , snake_head_y)
        return(snake_list)

def snake_hit_itself(snake_list):
        snake_head = snake_list[-1]
        for element in snake_list[0:-1]:
                if snake_head == element:
                        return(True)
        return(False)

def snake_hit_each_other(snake_list_player1 , snake_list_player2):
        snake_head_player1 = snake_list_player1[-1]
        snake_head_player2 = snake_list_player2[-1]

        if snake_head_player1 == snake_head_player2:
                return(True , 3)
        for element in snake_list_player2[0:-1]:
                if snake_head_player1 == element:
                        return(True , 1)
        for element in snake_list_player1[0:-1]:
                if snake_head_player2 == element:
                        return(True , 2)
        return(False , 0)
                
def draw_grid(width , height , block_size , window):
        for i in range (0, width , int(block_size)):
                pygame.draw.line(window, (255,255,255) , (i,0) , (i,height))
        for j in range (0, height , int(block_size)):
                pygame.draw.line(window, (255,255,255) , (0,j) , (width,j))
                
def write_words(font , words , x , y , color , window):
        text = font.render(str(words) , 1 , color)
        window.blit(text, (x , y))

def draw_snake(snake_list , block_size , window , color):
        for element in snake_list:
                body_x = element[0] * block_size
                body_y = element[1] * block_size
                body_red = random.randint(0,255)
                body_green = random.randint(0,255)
                body_blue = random.randint(0,255)
                if color == 'red':
                        pygame.draw.rect(window, (255 , 0 , 0) , (body_x , body_y , block_size , block_size))
                else:
                        if color == 'blue':
                                pygame.draw.rect(window, (0 , 0 , 255) , (body_x , body_y , block_size , block_size))
                        else:
                                pygame.draw.rect(window, (body_red , body_blue, body_green) , (body_x , body_y , block_size , block_size))

def draw_apple(apple_position, block_size , window , color):
        apple_x = int((apple_position[0] + 0.5) * block_size)
        apple_y = int((apple_position[1] + 0.5) * block_size)
        apple_red = random.randint(0,255)
        apple_green = random.randint(0,255)
        apple_blue = random.randint(0,255)
        if color == 'white':
                pygame.draw.circle(window, (255 , 255 ,255) , (apple_x , apple_y) , int(block_size / 2))                
        else:
                pygame.draw.circle(window, (apple_red , apple_green , apple_blue) , (apple_x , apple_y) , int(block_size / 2))

                
def pick_random_buff_position(snake_list_player1, snake_list_player2 , apple_position , number_columns , number_rows):
        while True:
                        buff_x = random.randint(0 , number_columns - 1)
                        buff_y = random.randint(0 , number_rows - 1)
                        if ((buff_x,buff_y) not in snake_list_player1) and ((buff_x,buff_y) not in snake_list_player2) and ([buff_x,buff_y] != apple_position):
                                return[buff_x , buff_y]        



def draw_buff(buff_position , block_size , window , buff_change_score , buff_change_direction):
        buff_x = int((buff_position[0] + 0.5) * block_size)
        buff_y = int((buff_position[1] + 0.5) * block_size)
        if buff_change_score:
                pygame.draw.circle(window, (255,255,0) , (buff_x , buff_y) , int(block_size / 2))
        if buff_change_direction:
                pygame.draw.circle(window, (255 ,0,255) , (buff_x , buff_y) , int(block_size / 2))
        
def keyboard_input(event , new_direction , player2):
        if player2 :
                if event.key == pygame.K_a:
                        return[-1,0]
                if event.key == pygame.K_d:
                        return[1,0]
                if event.key == pygame.K_w:
                        return[0,-1]
                if event.key == pygame.K_s:
                        return[0,1]
                else:
                        return(new_direction)

        else:
                if event.key == pygame.K_LEFT:
                        return[-1,0]
                if event.key == pygame.K_RIGHT:
                        return[1,0]
                if event.key == pygame.K_UP:
                        return[0,-1]
                if event.key == pygame.K_DOWN:
                        return[0,1]
                else:
                        return(new_direction)

def mouse_input():
        return(pygame.mouse.get_pos())

def show_score(player1_apple , player2_apple , width , height , window):
        font = pygame.font.Font(None , int(1.4 * int((width * height // 192)) ** 0.5))
        rect_text_one = font.render( str(player1_apple), 1 , (255 , 0 , 0))
        rect_text_two = font.render( str(player2_apple), 1 , (0 , 0 , 255))
        goal = font.render('10' , 1 , (255 , 255 , 255))
        window.blit(rect_text_one, (width * 0.44 , height * 0.01))
        window.blit(rect_text_two, (width * 0.58 , height * 0.01))
        window.blit(goal , (width * 0.49 , height * 0.01 ))
        
def menu(width , height , window , clock , FPS):
        
        font = pygame.font.Font(None , int(1.4 * int(width * height // 192) ** 0.5))
 
        rect_width = width //3
        rect_height = height //5
        
        rect_one_text_x = width // 3
        rect_one_text_y = height * 0.27

        rect_two_text_x = width // 3
        rect_two_text_y = height * 0.67
        while True:
                write_words(font , 'One Player' , rect_one_text_x , rect_one_text_y , (255 , 255 , 255)  ,window)
                write_words(font , 'Two Player' , rect_two_text_x , rect_two_text_y , (255 , 255 , 255)  ,window)
                
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                                
                mouse_position = mouse_input()
                mouse_x = mouse_position[0]
                mouse_y = mouse_position[1]
                if (mouse_x >= rect_width) and (mouse_x <= (2 * rect_width)) and (mouse_y >= rect_height) and (mouse_y <= 2 * rect_height):
                        write_words(font , 'One Player' , rect_one_text_x , rect_one_text_y , (0 , 255 , 255) , window)
                        if pygame.mouse.get_pressed()[0]:
                                do_one_player = True
                                do_two_player = False
                                return(do_one_player , do_two_player)
                        
                if (mouse_x >= rect_width) and (mouse_x <= (2 * rect_width)) and (mouse_y >= (3 * rect_height)) and (mouse_y <= (4 * rect_height)):
                        write_words(font , 'Two Player' , rect_two_text_x , rect_two_text_y , (0 , 255 , 255) , window)
                        if pygame.mouse.get_pressed()[0]:
                                do_one_player = False
                                do_two_player = True
                                return(do_one_player , do_two_player)
                pygame.display.update()
                clock.tick(2 * FPS)

                       
def player_1(initial_snake_length , number_columns , number_rows, width , height , block_size , window , clock , FPS):
        BGM = pygame.mixer.music.load('BGM.mp3')
        pygame.mixer.music.play()
        coin = pygame.mixer.Sound("get_apple.wav")
        
        
        current_direction = [1,0]
        new_direction = [1,0]
                           
        snake_list = get_initial_snake_player1 (initial_snake_length , number_columns , number_rows , False)
                           
        apple_position = pick_random_apple_position_one(snake_list, number_columns , number_rows)
        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.KEYDOWN:
                                new_direction = keyboard_input(event , new_direction , False)
                                
                current_direction = update_direction(current_direction , new_direction)
                snake_list , apple_eaten = update_snake(snake_list , current_direction, apple_position)
                if apple_eaten :
                        coin.play()
                        apple_position = pick_random_apple_position_one(snake_list , number_columns , number_rows)

                if snake_hit_itself(snake_list) or not_snake_inside_window(snake_list , number_columns , number_rows):
                        font = pygame.font.Font(None , int(1.4 * int((width * height // 192)) ** 0.5))
                        rect_text_x = width * 0.35
                        rect_text_y = height * 0.2
                        write_words(font , 'Game Over!' , rect_text_x , rect_text_y , (255 , 0 , 0) , window)
                        pygame.mixer.music.stop()
                        lost(False , window , clock , FPS)

                window.fill((0 , 0 , 0))

                if DRAW_GRID :
                        draw_grid(width , height , block_size , window)
                draw_snake(snake_list , block_size , window , 'random')
                draw_apple (apple_position , block_size , window , 'random')

                if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play()
                        
                pygame.display.update()
                clock.tick(FPS)
        pygame.quit()


def player_2(initial_snake_length , number_columns , number_rows, width , height , block_size , window , clock , FPS):
        BGM = pygame.mixer.music.load('BGM.mp3')
        coin = pygame.mixer.Sound("get_apple.wav")
        buff_change_score = False
        buff_change_direction = False
        buff_position = [-1 , -1]

        pygame.mixer.music.play()
        
        font = pygame.font.Font(None , int(1.4 * int((width * height // 192)) ** 0.5))
        rect_text_x = width * 0.35
        rect_text_y = height * 0.2
                        
        player1_apple = 0
        player2_apple = 0
        
        current_direction_player1 = [1,0]
        new_direction_player1 = [1,0]

        current_direction_player2 = [-1,0]
        new_direction_player2 = [-1,0]
                           
        snake_list_player1 = get_initial_snake_player1 (initial_snake_length , number_columns , number_rows , True)
        snake_list_player2 = get_initial_snake_player2 (initial_snake_length , number_columns , number_rows)                 

        apple_position = pick_random_apple_position_two(snake_list_player1 , snake_list_player2 , buff_position , number_columns , number_rows)
        buff_position = pick_random_buff_position(snake_list_player1, snake_list_player2 , apple_position , number_columns , number_rows)
        
        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.KEYDOWN:
                                new_direction_player1 = keyboard_input(event , new_direction_player1 , False)
                                new_direction_player2 = keyboard_input(event , new_direction_player2 , True)
                                
                if not buff_change_direction and not buff_change_score:
                        var = random.random()
                        if var < 0.01:
                                if var < 0.001:
                                        buff_change_score = True
                                        draw_buff(buff_position , block_size , window , buff_change_score , buff_change_direction)
                                if not buff_change_score:
                                        buff_change_direction = True
                                        draw_buff(buff_position , block_size , window , buff_change_score , buff_change_direction)
                
                current_direction_player1 = update_direction(current_direction_player1 , new_direction_player1)
                current_direction_player2 = update_direction(current_direction_player2 , new_direction_player2)

                
                snake_list_player1 , apple_eaten = update_snake(snake_list_player1 , current_direction_player1, apple_position)
                snake_list_player1 = snake_go_through_window(snake_list_player1 , number_columns , number_rows)
                if apple_eaten :
                        coin.play()
                        player1_apple += 1
                        apple_position = pick_random_apple_position_two(snake_list_player1 , snake_list_player2 , buff_position , number_columns , number_rows)
                draw_apple (apple_position , block_size , window , 'white')
                show_score(player1_apple , player2_apple , width , height , window)

                buff_eaten = update_buff(snake_list_player1 , buff_position)
                if buff_eaten:
                        if buff_change_direction:
                                current_direction_player2[0] = current_direction_player2[0] * -1
                                current_direction_player2[1] = current_direction_player2[1] * -1
                                snake_list_player2.reverse()
                                buff_change_direction = False
                        if buff_change_score:
                                player1_apple , player2_apple = player2_apple , player1_apple
                                show_score(player1_apple , player2_apple , width , height , window)
                                buff_change_score = False
                        buff_position = pick_random_buff_position(snake_list_player1, snake_list_player2 , apple_position , number_columns , number_rows)
                        draw_buff(buff_position , block_size , window , buff_change_score , buff_change_direction)
                                
                

                
                snake_list_player2 , apple_eaten = update_snake(snake_list_player2 , current_direction_player2, apple_position)
                snake_list_player2 = snake_go_through_window(snake_list_player2 , number_columns , number_rows)
                if apple_eaten :
                        coin.play()
                        player2_apple += 1
                        apple_position = pick_random_apple_position_two(snake_list_player1 , snake_list_player2 , buff_position , number_columns , number_rows)
                draw_apple (apple_position , block_size , window , 'white')
                show_score(player1_apple , player2_apple , width , height , window)
                        
                buff_eaten = update_buff(snake_list_player2 , buff_position)
                if buff_eaten:
                        if buff_change_direction:
                                current_direction_player1[0] = current_direction_player1[0] * -1
                                current_direction_player1[1] = current_direction_player1[1] * -1
                                snake_list_player1.reverse()
                                buff_change_direction = False
                        if buff_change_score:
                                player1_apple , player2_apple = player2_apple , player1_apple
                                show_score(player1_apple , player2_apple , width , height , window)
                                buff_change_score = False
                        buff_position = pick_random_buff_position(snake_list_player1, snake_list_player2 , apple_position , number_columns , number_rows)
                        draw_buff(buff_position , block_size , window , buff_change_score , buff_change_direction)
                        
                if player1_apple == 10 :
                        write_words(font , 'Player1 Wins!' , rect_text_x , rect_text_y , (255 , 0 , 0) , window)
                        pygame.mixer.music.stop()
                        lost(True , window , clock , FPS)

                if player2_apple == 10:
                        write_words(font , 'Player2 Wins!' , rect_text_x , rect_text_y , (0 , 0 , 255) , window)
                        pygame.mixer.music.stop()
                        lost(True , window , clock , FPS)
                        
                if snake_hit_itself(snake_list_player1):
                        write_words(font , 'Player2 Wins!' , rect_text_x , rect_text_y , (0, 0 , 255) , window)
                        pygame.mixer.music.stop()
                        lost(True , window , clock , FPS)

                if snake_hit_itself(snake_list_player2):
                        write_words(font , 'Player1 Wins!' , rect_text_x , rect_text_y , (255, 0 , 0) , window)
                        pygame.mixer.music.stop()
                        lost(True , window , clock , FPS)

                snake_hit , which_snake = snake_hit_each_other(snake_list_player1 , snake_list_player2)
                if snake_hit :
                        if which_snake == 1:
                                write_words(font , 'Player2 Wins!' , rect_text_x , rect_text_y , (0, 0 , 255) , window)
                                pygame.mixer.music.stop()
                                lost(True, window , clock , FPS)
                        if which_snake == 2:
                                write_words(font , 'Player1 Wins!' , rect_text_x , rect_text_y , (255, 0 , 0) , window)
                                pygame.mixer.music.stop()
                                lost(True , window , clock , FPS)
                        if which_snake == 3:
                                if player2_apple > player1_apple :
                                        snake_list_player1 = get_initial_snake_player1 (initial_snake_length , number_columns , number_rows , True)
                                        player1_apple = 0
                                if player2_apple < player1_apple :
                                        snake_list_player2 = get_initial_snake_player2 (initial_snake_length , number_columns , number_rows)
                                        player2_apple = 0        
                                if player1_apple == player2_apple:
                                        snake_list_player1[-1] = list(snake_list_player1[-1])
                                        snake_list_player1[-1][0] = snake_list_player1[-2][0] + (current_direction_player1[0] // 2)
                                        snake_list_player1[-1][1] = snake_list_player1[-2][1] + (current_direction_player1[1] // 2)
                                        snake_list_player1[-1] = tuple(snake_list_player1[-1])
                                        
                                        snake_list_player2[-1] = list(snake_list_player2[-1])
                                        snake_list_player2[-1][0] = snake_list_player2[-2][0] + (current_direction_player2[0] // 2)
                                        snake_list_player2[-1][1] = snake_list_player2[-2][1] + (current_direction_player2[1] // 2)
                                        snake_list_player2[-1] = tuple(snake_list_player2[-1])
                                        
                                        draw_snake(snake_list_player1 , block_size , window , 'red')
                                        draw_snake(snake_list_player2 , block_size , window , 'blue')
                                        draw_apple (apple_position , block_size , window , 'white')
                                        draw_buff(buff_position , block_size , window , buff_change_score , buff_change_direction)
                                        
                                        write_words(font , 'Game Over' , rect_text_x , rect_text_y , (255, 0 , 0) , window)
                                        pygame.mixer.music.stop()
                                        lost(True, window , clock , FPS)
                clock.tick(FPS)
                window.fill((0 , 0 , 0))
                show_score(player1_apple , player2_apple , width , height , window)
                if DRAW_GRID :
                        draw_grid(width , height , block_size , window)     
                draw_snake(snake_list_player1 , block_size , window , 'red')
                draw_snake(snake_list_player2 , block_size , window , 'blue')
                draw_apple (apple_position , block_size , window , 'white')
                draw_buff(buff_position , block_size , window , buff_change_score , buff_change_direction)

                if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play()
                
                pygame.display.update()
                
        pygame.quit()        

def tutorial(initial_snake_length , number_columns , number_rows, width , height , block_size , window , clock , FPS):
                
        font1 = pygame.font.Font(None , int(0.8 * int(width * height // 192) ** 0.5))
        font2 = pygame.font.Font(None , int(int(width * height // 192) ** 0.5))
        
        rect_one_text_x = width * 0.35
        rect_one_text_y = height * 0.1

        rect_two_text_x = width * 0.35
        rect_two_text_y = height * 0.3

        rect_three_text_x = width * 0.27
        rect_three_text_y = height * 0.8

        window.fill((0 , 0 , 0))
        while True:
                write_words(font1 , "This point can exchange two" , rect_one_text_x , rect_one_text_y , (255 , 255 , 255)  ,window)
                write_words(font1 , "players' scores" , rect_one_text_x , rect_one_text_y + height * 0.05 , (255 , 255 , 255)  ,window)
                pygame.draw.circle(window, (255 , 255 , 0) , ( int(width * 0.2) , int(rect_one_text_y + height * 0.05) ) , int(block_size / 2))
                
                write_words(font1 , "This point can reverse your rivial's" , rect_two_text_x , rect_two_text_y , (255 , 255 , 255)  ,window)
                write_words(font1 , "moving direction" , rect_two_text_x , rect_two_text_y + height * 0.05 , (255 , 255 , 255)  ,window)
                pygame.draw.circle(window, (255 , 0 , 255) , ( int(width * 0.2) , int(rect_two_text_y + height * 0.05) ) , int(block_size / 2))

                snake_x1 = int(width * 0.2)
                snake_y1 = int(height * 0.5)
                for i in range(snake_y1 , int(height * 0.7) , block_size):
                        pygame.draw.rect(window, (255 , 0 , 0) , (snake_x1 , int(i) , block_size , block_size))
                write_words(font1 , "Player1 uses" , int(snake_x1 + width * 0.1) , snake_y1 , (255 , 255 , 255)  ,window)
                write_words(font1 , "arrows" , int(snake_x1 + width * 0.1) , int(snake_y1 + height * 0.05) , (255 , 255 , 255)  ,window)        

                snake_x2 = int(width * 0.6)
                snake_y2 = int(height * 0.5)
                for j in range(snake_y2 , int(height * 0.7) , block_size):
                        pygame.draw.rect(window, (0 , 0 , 255) , (snake_x2 , int(j) , block_size , block_size))
                write_words(font1 , "Player2 uses " , int(snake_x2 + width * 0.1) , snake_y2 , (255 , 255 , 255)  ,window)
                write_words(font1 , "'w','a','s','d'" , int(snake_x2 + width * 0.1) , int(snake_y2 + height * 0.05) , (255 , 255 , 255)  ,window)
                
                write_words(font2 , "Press Space to play", rect_three_text_x , rect_three_text_y , (200 , 0 , 0 ) , window)
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                        player_2(initial_snake_length , number_columns , number_rows, width , height , block_size , window , clock , FPS) 
                pygame.display.update()
                clock.tick(2 * FPS)
        
        
        
def lost(two_player , window , clock , FPS):
        font = pygame.font.Font(None , int(int(width * height // 192) ** 0.5))
        
        rect_width = width * 0.1
        rect_height = height * 0.05
        
        rect_one_text_x = width * 0.4
        rect_one_text_y = height * 0.4

        rect_two_text_x = width * 0.4
        rect_two_text_y = height * 0.6


        while True:
                write_words(font , 'Retry' , rect_one_text_x , rect_one_text_y , (255, 255 , 255) , window)
                write_words(font , 'Quit to menu' , rect_two_text_x , rect_two_text_y , (255, 255 , 255) , window)

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                                
                mouse_position = mouse_input()
                mouse_x = mouse_position[0]
                mouse_y = mouse_position[1]
                if (mouse_x >= rect_one_text_x) and (mouse_x <= (rect_one_text_x + rect_width)) and (mouse_y >= rect_one_text_y) and (mouse_y <= (rect_one_text_y + rect_height)):
                        write_words(font , 'Retry' , rect_one_text_x , rect_one_text_y , (255, 255 , 0) , window)
                        if pygame.mouse.get_pressed()[0]:
                                if two_player :
                                        player_2(initial_snake_length , number_columns , number_rows, width , height , block_size , window , clock , FPS)
                                else:
                                        player_1(initial_snake_length , number_columns , number_rows, width , height , block_size , window , clock , FPS)
                                
                        
                if (mouse_x >= rect_two_text_x) and (mouse_x <= 1.35 * (rect_two_text_x + rect_width)) and (mouse_y >= rect_two_text_y) and (mouse_y <= (rect_two_text_y + rect_height)):
                        write_words(font , 'Quit to menu' , rect_two_text_x , rect_two_text_y , (255, 255 , 0) , window)
                        if pygame.mouse.get_pressed()[0]:
                                main()
                pygame.display.update()
                clock.tick(2 * FPS)
          
def main():
        pygame.init()
        window = pygame.display.set_mode ((width + 1 , height + 1))
        clock = pygame.time.Clock()
        pygame.display.set_caption('Snake Game')
        do_one_player , do_two_player = menu(width , height , window , clock , FPS)

        if do_one_player :
                player_1(initial_snake_length , number_columns , number_rows, width , height , block_size , window , clock , FPS)

        if do_two_player :
                tutorial(initial_snake_length , number_columns , number_rows, width , height , block_size , window , clock , FPS)
main()
