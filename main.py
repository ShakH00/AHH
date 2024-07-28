import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set the screen dimensions and create the screen object
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
empty_background = pygame.image.load("Graphics/empty.png")
empty_background = pygame.transform.scale(empty_background, (screen_width, screen_height))
pygame.display.set_caption("MindMaze: The Emotional Odyssey")

# Emojis
emoji_happy = pygame.image.load("Graphics/emoji_happy.png")
emoji_sad = pygame.image.load("Graphics/emoji_sad.png")
emoji_angry = pygame.image.load("Graphics/emoji_angry.png")
emoji_neutral = pygame.image.load("Graphics/emoji_neutral.png")

# Set initial sizes and positions for emojis
emoji_size = (100, 100)
emoji_happy = pygame.transform.scale(emoji_happy, emoji_size)
emoji_sad = pygame.transform.scale(emoji_sad, emoji_size)
emoji_angry = pygame.transform.scale(emoji_angry, emoji_size)
emoji_neutral = pygame.transform.scale(emoji_neutral, emoji_size)

# Set font and size
font = pygame.font.SysFont(None, 65)
font_small = pygame.font.SysFont(None, 40)
font_tiny = pygame.font.SysFont(None, 30)

# Load title image
title_image = pygame.image.load("Graphics/title_image.png")
title_image_rect = title_image.get_rect(center=(screen_width // 2, 110))
title_desc = pygame.image.load("Graphics/title_image2.png")
title_desc_rect = title_desc.get_rect(center=(screen_width // 2, 210))

# Feeling image
feeling_image = pygame.image.load("Graphics/feeling_text.png")
feeling_image_rect = feeling_image.get_rect(center=(screen_width // 2, 380))

# Emoji positions
emoji_positions = {
    "happy": (screen_width // 2 - 350, 430),
    "sad": (screen_width // 2 - 150, 430),
    "angry": (screen_width // 2 + 50, 430),
    "neutral": (screen_width // 2 + 250, 430)
}

# Interpolation variables
scaling_factor = 0.1
target_size = (120, 120)
current_sizes = {
    "happy": list(emoji_size),
    "sad": list(emoji_size),
    "angry": list(emoji_size),
    "neutral": list(emoji_size)
}

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Load images
player_img = pygame.image.load("Graphics/player.png")

# Player settings
player_size = 20
player_pos = [50, 50]
player_speed = 5

# Define walls (list of rects)
walls = []

# Goal position
goal_rect = pygame.Rect(screen_width - 60, screen_height - 60, 30, 30)

def is_over(pos, rect):
    """Check if the mouse is over a given rectangle"""
    return rect.collidepoint(pos)

def randomize_walls(level):
    """Randomize walls based on difficulty level"""
    walls.clear()
    cell_size = 40
    cols, rows = screen_width // cell_size, screen_height // cell_size

    # Initialize grid and walls
    grid = [[False for _ in range(cols)] for _ in range(rows)]
    cell_walls = [[[True, True, True, True] for _ in range(cols)] for _ in range(rows)]

    def draw_maze():
        for y in range(rows):
            for x in range(cols):
                if cell_walls[y][x][0]:  # Top
                    walls.append(pygame.Rect(x * cell_size, y * cell_size, cell_size, 3))
                if cell_walls[y][x][1]:  # Right
                    walls.append(pygame.Rect((x + 1) * cell_size, y * cell_size, 3, cell_size))
                if cell_walls[y][x][2]:  # Bottom
                    walls.append(pygame.Rect(x * cell_size, (y + 1) * cell_size, cell_size, 3))
                if cell_walls[y][x][3]:  # Left
                    walls.append(pygame.Rect(x * cell_size, y * cell_size, 3, cell_size))

    def get_neighbors(x, y):
        neighbors = []
        if y > 0:
            neighbors.append((x, y - 1))
        if x < cols - 1:
            neighbors.append((x + 1, y))
        if y < rows - 1:
            neighbors.append((x, y + 1))
        if x > 0:
            neighbors.append((x - 1, y))
        return neighbors

    def remove_walls(current, next):
        cx, cy = current
        nx, ny = next
        dx = cx - nx
        if dx == 1:
            cell_walls[cy][cx][3] = False
            cell_walls[ny][nx][1] = False
        elif dx == -1:
            cell_walls[cy][cx][1] = False
            cell_walls[ny][nx][3] = False
        dy = cy - ny
        if dy == 1:
            cell_walls[cy][cx][0] = False
            cell_walls[ny][nx][2] = False
        elif dy == -1:
            cell_walls[cy][cx][2] = False
            cell_walls[ny][nx][0] = False

    # Maze generation using Recursive Backtracking
    stack = [(0, 0)]
    grid[0][0] = True

    while stack:
        current = stack[-1]
        neighbors = [n for n in get_neighbors(*current) if not grid[n[1]][n[0]]]
        if neighbors:
            next_cell = random.choice(neighbors)
            remove_walls(current, next_cell)
            grid[next_cell[1]][next_cell[0]] = True
            stack.append(next_cell)
        else:
            stack.pop()

    # Draw the maze
    draw_maze()


def main_game(level):
    global back_rect
    running = True
    clock = pygame.time.Clock()
    player_pos[:] = [50, 50]
    randomize_walls(level)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if is_over(pygame.mouse.get_pos(), back_rect):
                    main_screen()
                    return

        # Movement
        keys = pygame.key.get_pressed()
        x_change = 0
        y_change = 0

        if keys[K_a] or keys[K_LEFT]:
            x_change = -player_speed
        if keys[K_d] or keys[K_RIGHT]:
            x_change = player_speed
        if keys[K_w] or keys[K_UP]:
            y_change = -player_speed
        if keys[K_s] or keys[K_DOWN]:
            y_change = player_speed

        # Update player position and handle collisions
        new_pos = player_pos.copy()
        new_pos[0] += x_change
        new_pos[1] += y_change

        player_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
        collision = False

        for wall in walls:
            if player_rect.colliderect(wall):
                collision = True
                break

        if not collision:
            player_pos[:] = new_pos
        else:
            if x_change != 0:
                new_pos = player_pos.copy()
                new_pos[0] += x_change
                player_rect = pygame.Rect(new_pos[0], player_pos[1], player_size, player_size)
                if not any(player_rect.colliderect(wall) for wall in walls):
                    player_pos[0] = new_pos[0]

        if y_change != 0:
            new_pos = player_pos.copy()
            new_pos[1] += y_change
            player_rect = pygame.Rect(player_pos[0], new_pos[1], player_size, player_size)
            if not any(player_rect.colliderect(wall) for wall in walls):
                player_pos[1] = new_pos[1]

        # Check for level completion
        if player_rect.colliderect(goal_rect):
            display_message("You Win!")

        # Drawing
        screen.blit(empty_background, (0, 0))
        pygame.draw.rect(screen, blue, player_rect)
        for wall in walls:
            pygame.draw.rect(screen, black, wall)
        pygame.draw.rect(screen, (0, 255, 0), goal_rect)

        # Draw back button
        back_text = font_small.render("Back", True, black)
        back_rect = pygame.Rect(800, 50, back_text.get_width(), back_text.get_height())
        screen.blit(back_text, (800, 50))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

def main_screen():
    """Display the main screen with emojis"""
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
                if is_over(mouse_pos, happy_rect):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_game("happy")
                elif is_over(mouse_pos, sad_rect):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_game("sad")
                elif is_over(mouse_pos, angry_rect):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_game("angry")
                elif is_over(mouse_pos, neutral_rect):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_game("neutral")
        # Fill the screen with the background image
        background_image = pygame.image.load("Graphics/bg1.png")
        screen.blit(background_image, (0, 0))

        # Draw title image
        screen.blit(title_image, title_image_rect)
        screen.blit(title_desc, title_desc_rect)

        # Draw text img
        screen.blit(feeling_image, feeling_image_rect)

        # Calculate the box dimensions around all emojis
        box_left = emoji_positions["happy"][0] - 50
        box_top = emoji_positions["happy"][1] - 18
        box_width = emoji_positions["neutral"][0] + emoji_size[0] + 50 - box_left
        box_height = emoji_size[1] + 60

        # Draw emojis and get their rectangles
        happy_rect = screen.blit(emoji_happy, emoji_positions["happy"])
        sad_rect = screen.blit(emoji_sad, emoji_positions["sad"])
        angry_rect = screen.blit(emoji_angry, emoji_positions["angry"])
        neutral_rect = screen.blit(emoji_neutral, emoji_positions["neutral"])

        # Draw the filled grey box around all emojis
        pygame.draw.rect(screen, (178, 178, 178), (box_left, box_top, box_width, box_height), border_radius=30)
        # Draw the black border around the grey box
        pygame.draw.rect(screen, "black", (box_left, box_top, box_width, box_height), 3, border_radius=30)

        # Smooth scaling of emojis
        for emoji_key in emoji_positions.keys():
            rect = pygame.Rect(emoji_positions[emoji_key], emoji_size)
            if is_over(mouse_pos, rect):
                current_sizes[emoji_key][0] += (target_size[0] - current_sizes[emoji_key][0]) * scaling_factor
                current_sizes[emoji_key][1] += (target_size[1] - current_sizes[emoji_key][1]) * scaling_factor
            else:
                current_sizes[emoji_key][0] += (emoji_size[0] - current_sizes[emoji_key][0]) * scaling_factor
                current_sizes[emoji_key][1] += (emoji_size[1] - current_sizes[emoji_key][1]) * scaling_factor

            scaled_emoji = pygame.transform.scale(eval(f"emoji_{emoji_key}"), (int(current_sizes[emoji_key][0]), int(current_sizes[emoji_key][1])))
            screen.blit(scaled_emoji, (emoji_positions[emoji_key][0] - (scaled_emoji.get_width() - emoji_size[0]) // 2, emoji_positions[emoji_key][1] - (scaled_emoji.get_height() - emoji_size[1]) // 2))

        # Draw emotion texts under emojis
        screen.blit(font_tiny.render("Happy", True, black), (emoji_positions["happy"][0] + (emoji_size[0] // 2 - font_tiny.render("Happy", True, black).get_width() // 2), emoji_positions["happy"][1] + emoji_size[1] + 5))
        screen.blit(font_tiny.render("Sad", True, black), (emoji_positions["sad"][0] + (emoji_size[0] // 2 - font_tiny.render("Sad", True, black).get_width() // 2), emoji_positions["sad"][1] + emoji_size[1] + 5))
        screen.blit(font_tiny.render("Angry", True, black), (emoji_positions["angry"][0] + (emoji_size[0] // 2 - font_tiny.render("Angry", True, black).get_width() // 2), emoji_positions["angry"][1] + emoji_size[1] + 5))
        screen.blit(font_tiny.render("Neutral", True, black), (emoji_positions["neutral"][0] + (emoji_size[0] // 2 - font_tiny.render("Neutral", True, black).get_width() // 2), emoji_positions["neutral"][1] + emoji_size[1] + 5))

        # Change the cursor to a pointer on hover
        if is_over(mouse_pos, happy_rect) or is_over(mouse_pos, sad_rect) or is_over(mouse_pos, angry_rect) or is_over(mouse_pos, neutral_rect):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_changed = True

        if not cursor_changed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Update the display
        pygame.display.flip()

# Define the display_message function
def display_message(message):
    """Display the message screen with a back button"""
    global back_rect
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

        # Draw back button
        back_text = font_small.render("Back", True, black)
        back_rect = pygame.Rect(800, 50, back_text.get_width(), back_text.get_height())
        pygame.draw.rect(screen, white, back_rect)
        screen.blit(back_text, (800, 50))

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
