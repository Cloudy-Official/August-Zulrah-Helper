import pygame
import sys
import os
from pynput import keyboard

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("August RSPS Zulrah Helper")

def load_image(image_path, placeholder=None):
    if getattr(sys, 'frozen', False):
        image_path = os.path.join(sys._MEIPASS, image_path)
    if os.path.exists(image_path):
        return pygame.image.load(image_path)
    else:
        print(f"Warning: {image_path} not found!")
        if placeholder:
            return placeholder
        return None

placeholder_image = pygame.Surface((width, height))
placeholder_image.fill((255, 0, 0))

preview_images = {
    1: load_image("images/pattern1_1.png", placeholder_image),
    2: load_image("images/pattern2_1.png", placeholder_image),
    3: load_image("images/pattern3_1.png", placeholder_image),
    4: load_image("images/pattern4_1.png", placeholder_image),
    5: load_image("images/pattern5_1.png", placeholder_image),
    6: load_image("images/pattern6_1.png", placeholder_image),
}

patterns = {
    1: [load_image(f"images/pattern1_{i}.png", placeholder_image) for i in range(1, 12)],
    2: [load_image(f"images/pattern2_{i}.png", placeholder_image) for i in range(1, 12)],
    3: [load_image(f"images/pattern3_{i}.png", placeholder_image) for i in range(1, 11)],
    4: [load_image(f"images/pattern4_{i}.png", placeholder_image) for i in range(1, 12)],
    5: [load_image(f"images/pattern5_{i}.png", placeholder_image) for i in range(1, 12)],
    6: [load_image(f"images/pattern6_{i}.png", placeholder_image) for i in range(1, 11)],
}

current_option = None
current_pattern = 0

hotkeys = {
    keyboard.KeyCode.from_char('q'): 1,
    keyboard.KeyCode.from_char('w'): 2,
    keyboard.KeyCode.from_char('e'): 3,
    keyboard.KeyCode.from_char('r'): 4,
    keyboard.KeyCode.from_char('t'): 5,
    keyboard.KeyCode.from_char('y'): 6,
}

key_labels = {
    1: 'Q',
    2: 'W',
    3: 'E',
    4: 'R',
    5: 'T',
    6: 'Y',
}

previews = {}

def draw_preview():
    global previews
    window.fill((50, 50, 50))
    
    preview_width = width // 3
    preview_height = height // 2

    for i in range(1, 7):
        x = (i - 1) % 3 * preview_width
        y = (i - 1) // 3 * preview_height
        preview_resized = pygame.transform.scale(preview_images[i], (preview_width, preview_height))
        window.blit(preview_resized, (x, y))

        font = pygame.font.SysFont(None, 48)
        label = font.render(key_labels[i], True, (0, 0, 0))
        window.blit(label, (x + 10, y + 10))

        previews[i] = (x, y, preview_width, preview_height)

        if current_option == i:
            pygame.draw.rect(window, (0, 255, 0), (x - 5, y - 5, preview_width + 10, preview_height + 10), 5)

def draw_patterns():
    window.fill((50, 50, 50))
    pattern_image = patterns[current_option][current_pattern]
    pattern_resized = pygame.transform.scale(pattern_image, (width, height))
    window.blit(pattern_resized, (0, 0))

def on_press(key):
    global current_option, current_pattern
    if key in hotkeys and current_option is None:
        current_option = hotkeys[key]
        current_pattern = 0
    elif key == keyboard.Key.delete:
        current_option = None
    elif key == keyboard.Key.space:
        if current_option is not None:
            current_pattern = (current_pattern + 1) % len(patterns[current_option])
            if current_pattern == 0:
                current_option = None  # Return to the preview screen
    elif key == keyboard.Key.left:
        if current_option is not None:
            current_pattern = (current_pattern - 1) % len(patterns[current_option])
            if current_pattern == len(patterns[current_option]) - 1:
                current_option = None  # Return to the preview screen

listener = keyboard.Listener(on_press=on_press)
listener.start()

def check_mouse_click(pos):
    global current_option
    for i, (x, y, w, h) in previews.items():
        if x <= pos[0] <= x + w and y <= pos[1] <= y + h:
            current_option = i
            return

def check_pattern_click(pos):
    global current_pattern, current_option
    # Check if the user clicked anywhere on the pattern display
    pattern_width = width
    pattern_height = height
    if 0 <= pos[0] <= pattern_width and 0 <= pos[1] <= pattern_height:
        # If clicked, advance to the next pattern image
        current_pattern = (current_pattern + 1) % len(patterns[current_option])
        if current_pattern == 0:  # When at the last image, return to the preview screen
            current_option = None
        return

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if current_option is None:
                    check_mouse_click(event.pos)
                else:
                    check_pattern_click(event.pos)

    if current_option is None:
        draw_preview()
    else:
        draw_patterns()

    pygame.display.flip()

pygame.quit()
sys.exit()
