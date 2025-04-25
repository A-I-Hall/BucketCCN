import threading
import pygame
import socket
import sys
import random

name = "bucket"
bucketX = 300
bucketY = 350
score = 0
gameOver = False
gameHasStarted = False

#falling object
objectX = random.randint(0, 575)
objectY = 0
objectSpeed = 3

#bucket speed increment
bucketSpeed = 20

def resetGame():
    global bucketX, bucketY, score, objectX, objectY, objectSpeed, gameOver, bucketSpeed, gameHasStarted
    bucketX = 300
    bucketY = 350
    score = 0
    objectX = random.randint(0, 575)
    objectY = 0
    objectSpeed = 3
    gameOver = False
    gameHasStarted = True  # Keep it True so game restarts instantly
    bucketSpeed = 30

def gameThread():
    global bucketX, bucketY, score, objectX, objectY, objectSpeed, gameOver, gameHasStarted, bucketSpeed

    pygame.init()

    fps = pygame.time.Clock()
    screenSize = screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('Bucket Catch Game')

    backgroundImage = pygame.image.load("Background.png").convert()
    backgroundImage = pygame.transform.scale(backgroundImage, (screen_width, screen_height))

    textColor = (0, 0, 0)
    font = pygame.font.SysFont(None, 36)

    # load and scale bucket/object images
    bucketImage = pygame.image.load("Bucket.png").convert_alpha()
    objectImage = pygame.image.load("Object.png").convert_alpha()

    bucketScale = 2.5
    objectScale = 2.5

    bucketWidth, bucketHeight = bucketImage.get_size()
    objectWidth, objectHeight = objectImage.get_size()

    bucketImage = pygame.transform.scale(bucketImage, (int(bucketWidth * bucketScale), int(bucketHeight * bucketScale)))
    objectImage = pygame.transform.scale(objectImage, (int(objectWidth * objectScale), int(objectHeight * objectScale)))

    # create rects from images
    bucketRect = bucketImage.get_rect()
    objectRect = objectImage.get_rect()

    # Collision rect adjustment
    collisionMargin = 30  # adjust this for tighter/looser hitbox
    bucketCollisionRect = pygame.Rect(0, 0, bucketRect.width - collisionMargin, bucketRect.height - collisionMargin)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(backgroundImage, (0, 0))  # draw background

        if not gameHasStarted:
            startText = font.render("Press 'E' to Start the Game", True, textColor)
            screen.blit(startText, (130, 180))
        elif not gameOver:
            bucketRect.center = (bucketX, bucketY)
            objectRect.center = (objectX, objectY)
            bucketCollisionRect.center = bucketRect.center  # align smaller collision box

            screen.blit(bucketImage, bucketRect)
            screen.blit(objectImage, objectRect)

            if bucketCollisionRect.colliderect(objectRect):
                score += 1
                objectY = 0
                objectX = random.randint(0, screen_width - objectRect.width)
                objectSpeed += 0.3
                bucketSpeed = min(30, bucketSpeed + 1)
            else:
                objectY += objectSpeed

            if objectY >= screen_height:
                gameOver = True

            scoreText = font.render("Score: " + str(score), True, textColor)
            screen.blit(scoreText, (10, 10))
        else:
            gameOverText = font.render("Game Over! Final Score: " + str(score), True, textColor)
            screen.fill((255, 204, 204))
            screen.blit(gameOverText, (120, 180))

        pygame.display.update()
        fps.tick(60)

def serverThread():
    global bucketX, bucketY, gameHasStarted, bucketSpeed

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
    print("Connection from:", str(address))

    try:
        prevInput = ''
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            # avoid holding key spam for 'r'
            if data == prevInput and data == 'r':
                continue
            prevInput = data

            if data.lower() == 'e':
                gameHasStarted = True
            elif data == 'a':
                bucketX -= bucketSpeed
            elif data == 'd':
                bucketX += bucketSpeed
            elif data == 'w':
                bucketY -= bucketSpeed
            elif data == 's':
                bucketY += bucketSpeed
            elif data == 'r':
                print("Restarting game...")
                resetGame()

            # boundary check
            bucketX = max(0, min(bucketX, 600))
            bucketY = max(0, min(bucketY, 400))

    except ConnectionResetError:
        print("Client disconnected unexpectedly.")
    finally:
        conn.close()


#run threads
t1 = threading.Thread(target=gameThread)
t2 = threading.Thread(target=serverThread)
t1.start()
t2.start()
