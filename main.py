import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set the screen dimensions and create the screen object
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MindMaze: The Emotional Odyssey")

white = (255, 255, 255)
black = (0, 0, 0)
TILE_SIZE = 64
WIDTH = TILE_SIZE*8
HEIGHT = TILE_SIZE*8
player = pygame.image.load("Graphics/player.png")
playerX = 1*TILE_SIZE
playerY = 1*TILE_SIZE
tile_options = ['empty','wall','endgoal']
rows, cols = (15, 15)
maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Emojis
emoji_happy = pygame.image.load("Graphics/emoji_happy.png")
emoji_sad = pygame.image.load("Graphics/emoji_sad.png")
emoji_angry = pygame.image.load("Graphics/emoji_angry.png")
emoji_neutral = pygame.image.load("Graphics/emoji_neutral.png")

# Scale emojis
emoji_size = (100, 100)
emoji_happy = pygame.transform.scale(emoji_happy, emoji_size)
emoji_sad = pygame.transform.scale(emoji_sad, emoji_size)
emoji_angry = pygame.transform.scale(emoji_angry, emoji_size)
emoji_neutral = pygame.transform.scale(emoji_neutral, emoji_size)

# Set font and size
font = pygame.font.SysFont(None, 65)
font_small = pygame.font.SysFont(None, 40)
font_tiny = pygame.font.SysFont(None, 30)

# Render text
feeling_text = font_small.render("How are you feeling today?", True, black)
welcome_text = font_tiny.render("Welcome to", True, black)

# Load title image
title_image = pygame.image.load("Graphics/title_image.png")
title_image_rect = title_image.get_rect(center=(screen_width // 2, 110))

# Emoji positions
emoji_positions = {
    "happy": (screen_width // 2 - 350, 300),
    "sad": (screen_width // 2 - 150, 300),
    "angry": (screen_width // 2 + 50, 300),
    "neutral": (screen_width // 2 + 250, 300)
}

def is_over(pos, rect):
    """Check if the mouse is over a given rectangle"""
    return rect.collidepoint(pos)

#algorithm used for generating maze levels
def create_maze(emotion):
    running = True
    print("A")
    screen.fill(white)
    print("E")
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            if maze[row][column] == 1:
                screen.blit(pygame.image.load("Graphics/wall.png"), (x, y))
            elif maze[row][column] == 0:
                screen.blit(pygame.image.load("Graphics/empty.png"), (x, y))
            elif maze[row][column] == 2:
                screen.blit(pygame.image.load("Graphics/endgoal.png"), (x, y))
            #tile = tile_options[maze[row][column]]
            #screen.blit(pygame.image.load(f"Graphics/{tile}.png"), (x, y))
    screen.blit(player,(playerX,playerY))
    #if emotion == "happy":

    #elif emotion == "sad":

    #elif emotion == "angry":

    #elif emotion == "neutral":


#function to display the maze on the screen
def display_maze(maze_txt):
    running = True

def main_screen():
    """Display the main screen with emojis"""
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        cursor_changed = False

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if is_over(mouse_pos, happy_rect):
                    #display_message("Happy")
                    create_maze("happy")
                elif is_over(mouse_pos, sad_rect):
                    display_message("Sad")
                    create_maze("sad")
                elif is_over(mouse_pos, angry_rect):
                    display_message("Angry")
                    create_maze("angry")
                elif is_over(mouse_pos, neutral_rect):
                    display_message("Neutral")
                    create_maze("neutral")

        # Fill the screen with the background image
        background_image = pygame.image.load("Graphics/bg.jpg")
        screen.blit(background_image, (0, 0))

        # Draw title image
        screen.blit(title_image, title_image_rect)

        # Draw text
        screen.blit(feeling_text, (screen_width // 2 - feeling_text.get_width() // 2, 230))

        # Draw emojis and get their rectangles
        happy_rect = screen.blit(emoji_happy, emoji_positions["happy"])
        sad_rect = screen.blit(emoji_sad, emoji_positions["sad"])
        angry_rect = screen.blit(emoji_angry, emoji_positions["angry"])
        neutral_rect = screen.blit(emoji_neutral, emoji_positions["neutral"])

        # Draw emotion texts under emojis
        screen.blit(font_tiny.render("Happy", True, black), (emoji_positions["happy"][0] + 15, emoji_positions["happy"][1] + 110))
        screen.blit(font_tiny.render("Sad", True, black), (emoji_positions["sad"][0] + 33, emoji_positions["sad"][1] + 110))
        screen.blit(font_tiny.render("Angry", True, black), (emoji_positions["angry"][0] + 20, emoji_positions["angry"][1] + 110))
        screen.blit(font_tiny.render("Neutral", True, black), (emoji_positions["neutral"][0] + 15, emoji_positions["neutral"][1] + 110))

        # Check if the mouse is over any emoji and change the cursor to a pointer
        if is_over(mouse_pos, happy_rect) or is_over(mouse_pos, sad_rect) or is_over(mouse_pos, angry_rect) or is_over(mouse_pos, neutral_rect):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_changed = True

        if not cursor_changed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Update the display
        pygame.display.flip()

def display_message(message):
    """Display the message screen with a back button"""
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        cursor_changed = False

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if is_over(mouse_pos, back_rect):
                    running = False

        # Background
        screen.fill(white)

        # Display message
        message_text = font.render(message, True, black)
        screen.blit(message_text, (screen_width // 2 - message_text.get_width() // 2, screen_height // 2 - message_text.get_height() // 2))

        # Draw back button
        back_text = font_small.render("Back", True, black)
        back_rect = pygame.Rect(50, 50, back_text.get_width(), back_text.get_height())
        pygame.draw.rect(screen, white, back_rect)
        screen.blit(back_text, (50, 50))

        # Change the cursor to a pointer on back button
        if is_over(mouse_pos, back_rect):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_changed = True

        if not cursor_changed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Update the display
        pygame.display.flip()

# Run the main screen function
main_screen()

# Quit Pygame
pygame.quit()
sys.exit()