import threading
import pygame
import socket
import sys
import random

name = "bucket"
bucket_x = 300
bucket_y = 350
score = 0
game_over = False
game_started = False

# Falling object
falling_x = random.randint(0, 575)
falling_y = 0
falling_speed = 3

# Bucket speed increment (for responsiveness)
bucket_speed = 20

def reset_game():
    global bucket_x, bucket_y, score, falling_x, falling_y, falling_speed, game_over, game_started, bucket_speed
    # Reset the game state
    bucket_x = 300
    bucket_y = 350
    score = 0
    falling_x = random.randint(0, 575)
    falling_y = 0
    falling_speed = 3
    game_over = False
    game_started = False
    bucket_speed = 30  # Reset bucket speed to default

def GameThread():
    global bucket_x, bucket_y, score, falling_x, falling_y, falling_speed, game_over, game_started, bucket_speed

    pygame.init()
    background = (204, 230, 255)
    bucket_color = (0, 51, 204)
    object_color = (255, 0, 0)
    text_color = (0, 0, 0)

    fps = pygame.time.Clock()
    screen_size = screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Bucket Catch Game')

    font = pygame.font.SysFont(None, 36)

    bucket_rect = pygame.Rect(0, 0, 75, 30)
    object_rect = pygame.Rect(0, 0, 25, 25)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background)

        if not game_started:
            waiting_text = font.render("Press 'E' to Start the Game", True, text_color)
            screen.blit(waiting_text, (130, 180))
        elif not game_over:
            # Update positions
            bucket_rect.center = (bucket_x, bucket_y)
            object_rect.center = (falling_x, falling_y)

            # Draw shapes
            pygame.draw.rect(screen, bucket_color, bucket_rect)
            pygame.draw.rect(screen, object_color, object_rect)

            # Collision
            if bucket_rect.colliderect(object_rect):
                score += 1
                falling_y = 0
                falling_x = random.randint(0, 575)
                falling_speed += 0.3  # increase falling speed as the game progresses
                bucket_speed = min(30, bucket_speed + 1)  # increase bucket speed, capped at 30
            else:
                falling_y += falling_speed

            # Check game over
            if falling_y >= 400:
                game_over = True

            # Score
            score_text = font.render("Score: " + str(score), True, text_color)
            screen.blit(score_text, (10, 10))
        else:
            # Show Game Over
            over_text = font.render("Game Over! Final Score: " + str(score), True, text_color)
            screen.fill((255, 204, 204))
            screen.blit(over_text, (120, 180))

        pygame.display.update()
        fps.tick(60)


def ServerThread():
    global bucket_x, bucket_y, game_started, bucket_speed

    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()

    print("Server running on:", host)
    port = 5050

    server_socket = socket.socket()
    server_socket.bind((host, port))
    print("Waiting for client...")
    server_socket.listen(1)

    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        if data.lower() == 'e':
            game_started = True
        if data == 'a':
            bucket_x -= bucket_speed  # Use the dynamic bucket speed
        if data == 'd':
            bucket_x += bucket_speed
        if data == 'w':
            bucket_y -= bucket_speed
        if data == 's':
            bucket_y += bucket_speed

        # Boundary check
        bucket_x = max(0, min(bucket_x, 600))
        bucket_y = max(0, min(bucket_y, 400))

        if data == 'r':  # Restart the game
            print("Restarting game...")
            reset_game()  # Reset all game variables

    conn.close()


# Run threads
t1 = threading.Thread(target=GameThread)
t2 = threading.Thread(target=ServerThread)
t1.start()
t2.start()
