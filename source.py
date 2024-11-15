import pygame
import sys
import os

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("August RSPS Zulrah Helper")

def load_image(image_path, placeholder=None):
    if getattr(sys, 'frozen', False):  # Check if running as a bundled executable
        image_path = os.path.join(sys._MEIPASS, image_path)  # Access the bundled path
    if os.path.exists(image_path):
        return pygame.image.load(image_path)
    else:
        print(f"Warning: {image_path} not found!")
        if placeholder:
            return placeholder
        return None

placeholder_image = pygame.Surface((width, height))
placeholder_image.fill((255, 0, 0))

# Loading preview images
preview_images = {
    1: load_image("images/pattern1_1.png", placeholder_image),
    2: load_image("images/pattern2_1.png", placeholder_image),
    3: load_image("images/pattern3_1.png", placeholder_image),
    4: load_image("images/pattern4_1.png", placeholder_image),
    5: load_image("images/pattern5_1.png", placeholder_image),
    6: load_image("images/pattern6_1.png", placeholder_image),
}

# Loading pattern images (1-12 for each, some with 10 patterns)
patterns = {
    1: [load_image(f"images/pattern1_{i}.png", placeholder_image) for i in range(1, 12)],
    2: [load_image(f"images/pattern2_{i}.png", placeholder_image) for i in range(1, 12)],
    3: [load_image(f"images/pattern3_{i}.png", placeholder_image) for i in range(1, 11)],
    4: [load_image(f"images/pattern4_{i}.png", placeholder_image) for i in range(1, 12)],
    5: [load_image(f"images/pattern5_{i}.png", placeholder_image) for i in range(1, 11)],
    6: [load_image(f"images/pattern6_{i}.png", placeholder_image) for i in range(1, 11)],
}

current_option = None
current_pattern = 0

hotkeys = {
    pygame.K_F1: 1,
    pygame.K_F2: 2,
    pygame.K_F3: 3,
    pygame.K_F4: 4,
    pygame.K_F5: 5,
    pygame.K_F6: 6,
}

def draw_preview():
    window.fill((50, 50, 50))
    
    preview_width = width // 3
    preview_height = height // 2

    for i in range(1, 7):
        x = (i - 1) % 3 * preview_width
        y = (i - 1) // 3 * preview_height
        preview_resized = pygame.transform.scale(preview_images[i], (preview_width, preview_height))
        window.blit(preview_resized, (x, y))

        font = pygame.font.SysFont(None, 48)
        label = font.render(f"F{i}", True, (0, 0, 0))
        window.blit(label, (x + 10, y + 10))

        previews[i] = (x, y, preview_width, preview_height)

def draw_patterns():
    window.fill((50, 50, 50))
    pattern_image = patterns[current_option][current_pattern]
    pattern_resized = pygame.transform.scale(pattern_image, (width, height))
    window.blit(pattern_resized, (0, 0))

previews = {}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_option is None:
                if event.key in hotkeys:
                    current_option = hotkeys[event.key]
                    current_pattern = 0
            else:
                if event.key == pygame.K_DELETE:
                    current_option = None
                elif event.key == pygame.K_SPACE:
                    current_pattern = (current_pattern + 1) % len(patterns[current_option])
                    if current_pattern == 0:
                        current_option = None
                elif event.key == pygame.K_LEFT:
                    current_pattern = (current_pattern - 1) % len(patterns[current_option])
                    if current_pattern == len(patterns[current_option]) - 1:
                        current_option = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_option is None:
                for option, (x, y, w, h) in previews.items():
                    mouse_x, mouse_y = event.pos
                    if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                        current_option = option
                        current_pattern = 0
                if event.pos[0] < width // 3 and event.pos[1] < height // 2:
                    current_pattern = (current_pattern + 1) % len(patterns[current_option])
                    if current_pattern == 0:
                        current_option = None

        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    if current_option is None:
        draw_preview()
    else:
        draw_patterns()

    pygame.display.flip()

pygame.quit()
sys.exit()
