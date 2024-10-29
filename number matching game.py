# build an alphabet matching game

import pygame
import random

pygame.init()

#game variables and constants
WIDTH = 600
HEIGHT = 600
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)
fps = 60
timer = pygame.time.Clock()
rows = 4
columns = 5
correct = [[0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0]]

options_list = []
spaces = []
used = []
new_board = True
first_guess = False
second_guess = False
first_guess_num = 0
second_guess_num = 0
score = 0
matches = 0
best_score = 0
game_over = False

#create screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Number Matching Game")
title_font = pygame.font.Font("freesansbold.ttf", 36)
small_font = pygame.font.Font("freesansbold.ttf", 31)

def generate_board():
    global options_list
    global spaces
    global used
    for item in range(rows * columns // 2):
        options_list.append(item)

    for item in range(rows * columns):
        piece = options_list[random.randint(0, len(options_list)-1)]
        spaces.append(piece)
        if piece in used:
            used.remove(piece)
            options_list.remove(piece)
        else:
            used.append(piece)


def draw_background():
    top_menu = pygame.draw.rect(screen, black, [0, 0, WIDTH, 100])
    title_text = title_font.render("The Number Matching Game!", True, white)
    screen.blit(title_text, (10, 20))
    board_space = pygame.draw.rect(screen, gray, [0, 100, WIDTH, HEIGHT -200], 0)
    bottom_menu = pygame.draw.rect(screen, black, [0, HEIGHT -100, WIDTH, 100], 0)
    restart_button = pygame.draw.rect(screen, gray, [10, HEIGHT - 90, 200, 80], 0, 5)
    restart_text = title_font.render("Restart", True, white)
    screen.blit(restart_text, (10, 520))
    score_text = small_font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (350, 520))
    best_text = small_font.render(f"Current turns: {best_score}", True, white)
    screen.blit(best_text, (350, 560))
    return restart_button

def draw_board():
    global rows
    global columns
    global correct
    board_list = []
    for i in range(columns):
        for j in range(rows):
            piece = pygame.draw.rect(screen, white, [i * 75 + 12, j * 65 + 112, 50, 50], 0, 4)
            board_list.append(piece)
            #piece_text = small_font.render(f'{spaces[i * rows + j]}', True, gray)
            #screen.blit(piece_text, (i * 75 + 18, j * 65 + 120))

    for r in range(rows):
        for c in range(columns):
            if correct [r][c] == 1:
                pygame.draw.rect(screen, green, [c * 75 + 10, r * 65 + 110, 54, 54], 3, 4)    
                piece_text = small_font.render(f'{spaces[c * rows + r]}', True, gray)
                screen.blit(piece_text, (c * 75 + 18, r * 65 + 120))


    return board_list

def check_guesses(first, second):
    global spaces
    global correct
    global matches
    global score
    print(f"First guess: {spaces[first]}, Second guess: {spaces[second]}")
    if spaces[first] == spaces[second]:
        print("Match found!")
        columns1 = first // rows
        columns2 = second // rows
        row1 = first - (first // rows * rows)
        row2 = second - (second // rows * rows)
        if correct[row1][columns1] == 0 and correct[row2][columns2] == 0: 
            correct[row1][columns1] = 1
            correct[row2][columns2] = 1
            score += 1
            matches += 1
            print(f"Updated correct matrix: {correct}")
    else:
        print("No match found!")
        score += 1
        print(f"Correct matrix remains: {correct}")


running = True
while running:
    timer.tick(fps)
    screen.fill(white)
    if new_board:
        generate_board()
        print(f"Generated spaces: {spaces}")
        print(spaces)
        new_board = False

    restart = draw_background()
    board = draw_board()

    if first_guess and second_guess:
        print(f"First guess index: {first_guess_num}, Second guess index: {second_guess_num}")
        print(f"Calling check_guesses for indices {first_guess_num} and {second_guess_num}")
        check_guesses(first_guess_num, second_guess_num)
        pygame.time.delay(1000)
        first_guess = False
        second_guess = False

        if first_guess and second_guess:
            first_guess = False
            second_guess = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(board)):
                button = board[i]
                if not game_over:
                    if button.collidepoint(event.pos) and not first_guess:
                        first_guess = True
                        first_guess_num = i
                        print(f"First guess selected at index {i}")
        
                    elif button.collidepoint(event.pos) and not second_guess and first_guess and i != first_guess_num:
                        second_guess = True
                        second_guess_num = i
                        print(f"Second guess selected at index {i}")      
            if restart.collidepoint(event.pos):
                options_list = []
                used = []
                spaces = []
                new_board = True
                score = 0
                matches = 0
                first_guess = False
                second_guess = False
                correct = [[0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0]]
                game_over = False


    if matches == rows * columns // 2:
        game_over = True
        winner = pygame.draw.rect(screen, gray, [10, HEIGHT - 300, WIDTH - 20, 80], 0, 5)
        winner_text = title_font.render(f"You Won in {score} moves!", True, white)
        screen.blit(winner_text, (10, HEIGHT - 290))
        if best_score > score or best_score == 0:
            best_score = score
    
    
    if first_guess:
        piece_text = small_font.render(f'{spaces[first_guess_num]}', True, blue)
        location = (first_guess_num // rows * 75 + 18, (first_guess_num - (first_guess_num // rows * rows)) * 65 + 120)
        screen.blit(piece_text, (location))
        
    if second_guess:
        piece_text = small_font.render(f'{spaces[second_guess_num]}', True, blue)
        location = (second_guess_num // rows * 75 + 18, (second_guess_num - (second_guess_num // rows * rows)) * 65 + 120)
        screen.blit(piece_text, (location))
            

    pygame.display.flip()
pygame.quit()  