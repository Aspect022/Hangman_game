import pygame
import random

# Separate lists for 4-letter, 5-letter, and 6-letter words
four_letter_words = [
    'bird', 'fish', 'frog', 'lion', 'bear', 'wolf', 'goat', 'deer', 'duck', 'crab',
    'moth', 'toad', 'bull', 'dove', 'kite', 'lamb', 'mule', 'seal', 'swan', 'worm'
]

five_letter_words = [
    'apple', 'peach', 'grape', 'mango', 'lemon', 'melon', 'plumb', 'olive', 'cherry', 'berry',
    'piano', 'guitar', 'viola', 'flute', 'drums', 'cello', 'horns', 'harps', 'lyres', 'oboes'
]

six_letter_words = [
    'tomato', 'carrot', 'pepper', 'potato', 'celery', 'onions', 'cabbage', 'radish', 'garlic', 'squash',
    'pencil', 'eraser', 'notebook', 'ruler', 'marker', 'stapler', 'scotch', 'glue', 'folder', 'binder'
]

# Initialize pygame
pygame.init()

# Dimensions
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hangman")
icon = pygame.image.load("D:\\Coding\\games\\hangman\\Hangman_png.png")  # Use double backslashes or raw strings for Windows paths
pygame.display.set_icon(icon)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)

# Game variables
tries_left = 10
current_image = 0
input_letters = ""
selected_word = ""
word_length = 4  # Default to 4-letter words, will change based on selection
last_word = ""  # Initialize last_word to keep track of the previous word

# Load resources
font = pygame.font.SysFont("comicsans", 60)
small_font = pygame.font.SysFont("comicsans", 40)
images = [pygame.image.load(f"D:\\Coding\\games\\hangman\\Hangman_{i}.png") for i in range(11)]

title_font = pygame.font.SysFont("comicsans", 60)
word_font = pygame.font.SysFont("comicsans", 40)
keyboard_font = pygame.font.SysFont("comicsans", 30)

# Key states dictionary to track the state of each key
key_states = {key: "default" for key in "abcdefghijklmnopqrstuvwxyz"}

def draw_rounded_rect(surface, color, rect, border_color, corner_radius):
    pygame.draw.rect(surface, border_color, rect, border_radius=corner_radius)
    inner_rect = rect.inflate(-6, -6)  # Adjust the thickness of the border
    pygame.draw.rect(surface, color, inner_rect, border_radius=corner_radius)

def draw_main_page():
    screen.fill(white)
    title = title_font.render("HANGMAN", True, black)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 40))

    options = word_font.render("Choose the number of letters", True, black)
    screen.blit(options, (screen_width // 2 - options.get_width() // 2, 140))

    choice1_box = pygame.Rect(425, 240, 200, 60)
    choice2_box = pygame.Rect(425, 340, 200, 60)
    choice3_box = pygame.Rect(425, 440, 200, 60)

    draw_rounded_rect(screen, white, choice1_box, black, 12)
    draw_rounded_rect(screen, white, choice2_box, black, 12)
    draw_rounded_rect(screen, white, choice3_box, black, 12)

    choice1_text = word_font.render("4 Letters", True, black)
    choice2_text = word_font.render("5 Letters", True, black)
    choice3_text = word_font.render("6 Letters", True, black)

    screen.blit(choice1_text, (choice1_box.x + (choice1_box.width - choice1_text.get_width()) // 2,
                               choice1_box.y + (choice1_box.height - choice1_text.get_height()) // 2))
    screen.blit(choice2_text, (choice2_box.x + (choice2_box.width - choice2_text.get_width()) // 2,
                               choice2_box.y + (choice2_box.height - choice2_text.get_height()) // 2))
    screen.blit(choice3_text, (choice3_box.x + (choice3_box.width - choice3_text.get_width()) // 2,
                               choice3_box.y + (choice3_box.height - choice3_text.get_height()) // 2))

    pygame.display.flip()

def draw_title_and_tries():
    title = title_font.render("HANGMAN", True, black)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 20))

    tries_text = small_font.render(f"Tries left: {tries_left}", True, black)
    screen.blit(tries_text, (80, 20))

def draw_virtual_keyboard():
    global keys_1, keys_2, keys_3, start_x_1, start_x_2, start_x_3, y_1, y_2, y_3, key_box_height, key_box_width

    keys_1 = "qwertyuiop"
    keys_2 = "asdfghjkl"
    keys_3 = "zxcvbnm"

    key_box_height = 50
    key_box_width = 50
    start_x_1 = (screen_width - (key_box_width + 10) * 10) // 2
    start_x_2 = (screen_width - (key_box_width + 10) * 9) // 2
    start_x_3 = (screen_width - (key_box_width + 10) * 7) // 2
    y_1 = 600
    y_2 = y_1 + 55
    y_3 = y_2 + 55

    for i, letter in enumerate(keys_1):
        rect = pygame.Rect(start_x_1 + (key_box_width + 10) * (i % 13), y_1 + (key_box_height + 10) * (i // 13), key_box_width, key_box_height)
        color = {"default": white, "correct": green, "present": yellow}.get(key_states[letter], white)
        draw_rounded_rect(screen, color, rect, black, 12)
        text = keyboard_font.render(letter, True, black)
        screen.blit(text, (rect.x + (key_box_width - text.get_width()) // 2, rect.y + (key_box_height - text.get_height()) // 2))

    for i, letter in enumerate(keys_2):
        rect = pygame.Rect(start_x_2 + (key_box_width + 10) * (i % 13), y_2 + (key_box_height + 10) * (i // 13), key_box_width, key_box_height)
        color = {"default": white, "correct": green, "present": yellow}.get(key_states[letter], white)
        draw_rounded_rect(screen, color, rect, black, 12)
        text = keyboard_font.render(letter, True, black)
        screen.blit(text, (rect.x + (key_box_width - text.get_width()) // 2, rect.y + (key_box_height - text.get_height()) // 2))

    for i, letter in enumerate(keys_3):
        rect = pygame.Rect(start_x_3 + (key_box_width + 10) * (i % 13), y_3 + (key_box_height + 10) * (i // 13), key_box_width, key_box_height)
        color = {"default": white, "correct": green, "present": yellow}.get(key_states[letter], white)
        draw_rounded_rect(screen, color, rect, black, 12)
        text = keyboard_font.render(letter, True, black)
        screen.blit(text, (rect.x + (key_box_width - text.get_width()) // 2, rect.y + (key_box_height - text.get_height()) // 2))

def draw_hangman_images():
    screen.blit(images[current_image], (screen_width // 2 - images[0].get_width() // 2, 100))

def draw_boxes():
    box_width = 80
    box_height = 80
    start_x = (screen_width - (box_width + 10) * word_length) // 2
    y = 450

    for i in range(word_length):
        rect = pygame.Rect(start_x + (box_width + 10) * i, y, box_width, box_height)
        draw_rounded_rect(screen, white, rect, black, 12)
        if i < len(input_letters):
            text = word_font.render(input_letters[i], True, black)
            screen.blit(text, (rect.x + (box_width - text.get_width()) // 2, rect.y + (box_height - text.get_height()) // 2))

def draw_success_screen(random_word):
    screen.fill(white)

    title = title_font.render("HANGMAN", True, black)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 20))

    msg = font.render("Congrats!!", True, black)
    screen.blit(msg, (screen_width // 2 - msg.get_width() // 2, 100))

    word = word_font.render(f"The word was: {random_word}", True, black)
    screen.blit(word, (screen_width // 2 - word.get_width() // 2, 250))

    pygame.display.flip()

def draw_failure_screen(random_word):
    screen.fill(white)

    title = title_font.render("HANGMAN", True, black)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 20))

    msg = font.render("Game Over!", True, red)
    screen.blit(msg, (screen_width // 2 - msg.get_width() // 2, 100))

    word = word_font.render(f"The word was: {random_word}", True, black)
    screen.blit(word, (screen_width // 2 - word.get_width() // 2, 250))

    pygame.display.flip()

def previous_word():
    if last_word:
        text = keyboard_font.render(f"Last word was: {last_word}", True, black)
        screen.blit(text, (450, 750))

def update_game_state(input_word):
    global tries_left, current_image, input_letters, key_states, last_word

    # Store the current input_word as last_word before resetting input_letters
    last_word = input_word

    # Clear key_states for new input
    for key in key_states:
        key_states[key] = "default"

    correct_positions = [i for i in range(len(input_word)) if input_word[i] == selected_word[i]]
    correct_letters = set(selected_word) & set(input_word)

    if input_word == selected_word:
        success()
    else:
        tries_left -= 1
        current_image += 1
        input_letters = ""

        for letter in input_word:
            if letter in selected_word:
                if letter in correct_letters and key_states[letter] == "default":
                    key_states[letter] = "present"
                for pos in correct_positions:
                    if selected_word[pos] == letter:
                        key_states[letter] = "correct"
                        break
            else:
                key_states[letter] = "default"

        if tries_left == 0:
            failure()

def Hangman_Game(word_list, word_len):
    global selected_word, input_letters, tries_left, current_image, word_length, last_word
    selected_word = random.choice(word_list)
    input_letters = ""
    tries_left = 10
    current_image = 0
    word_length = word_len
    last_word = ""  # Reset last_word when starting a new game
    running = True

    while running:
        screen.fill(white)
        draw_title_and_tries()
        draw_hangman_images()
        draw_boxes()
        draw_virtual_keyboard()
        previous_word()  # Update this to use the new last_word logic
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and len(input_letters) < word_length:
                    input_letters += event.unicode.lower()
                elif event.key == pygame.K_BACKSPACE and len(input_letters) > 0:
                    input_letters = input_letters[:-1]
                elif event.key == pygame.K_RETURN and len(input_letters) == word_length:
                    update_game_state(input_letters)

def Four_Word_Hangman():
    Hangman_Game(four_letter_words, 4)

def Five_Word_Hangman():
    Hangman_Game(five_letter_words, 5)

def Six_Word_Hangman():
    Hangman_Game(six_letter_words, 6)

def success():
    draw_success_screen(selected_word)
    pygame.time.delay(5000)  # Pause for 5 seconds
    main_screen()

def failure():
    draw_failure_screen(selected_word)
    pygame.time.delay(5000)  # Pause for 5 seconds
    main_screen()

def main_screen():
    running = True
    while running:
        draw_main_page()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                Four_Words = pygame.Rect(425, 240, 200, 60)
                Five_Words = pygame.Rect(425, 340, 200, 60)
                Six_Words = pygame.Rect(425, 440, 200, 60)
                if Four_Words.collidepoint(mouse_pos):
                    Four_Word_Hangman()
                elif Five_Words.collidepoint(mouse_pos):
                    Five_Word_Hangman()
                elif Six_Words.collidepoint(mouse_pos):
                    Six_Word_Hangman()

    pygame.quit()

main_screen()
