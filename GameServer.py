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
    global bucketX, bucketY, score, objectX, objectY, objectSpeed, gameOver, gameHasStarted, bucketSpeed
    #reset the game state
    bucketX = 300
    bucketY = 350
    score = 0
    objectX = random.randint(0, 575)
    objectY = 0
    objectSpeed = 3
    gameOver = False
    gameHasStarted = False
    bucketSpeed = 30 #reset bucket speed to default

def gameThread():
    global bucketX, bucketY, score, objectX, objectY, objectSpeed, gameOver, gameHasStarted, bucketSpeed

    pygame.init()
    background = (204, 230, 255)
    bucketColor = (0, 51, 204)
    objectColor = (255, 0, 0)
    textColor = (0, 0, 0)

    fps = pygame.time.Clock()
    screenSize = screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('Bucket Catch Game')

    font = pygame.font.SysFont(None, 36)

    bucketRect = pygame.Rect(0, 0, 75, 30)
    objectRect = pygame.Rect(0, 0, 25, 25)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background)

        if not gameHasStarted:
            startText = font.render("Press 'E' to Start the Game", True, textColor)
            screen.blit(startText, (130, 180))
        elif not gameOver:
            #update positions
            bucketRect.center = (bucketX, bucketY)
            objectRect.center = (objectX, objectY)

            #draw shapes
            pygame.draw.rect(screen, bucketColor, bucketRect)
            pygame.draw.rect(screen, objectColor, objectRect)

            #collision
            if bucketRect.colliderect(objectRect):
                score += 1
                objectY = 0
                objectX = random.randint(0, 575)
                objectSpeed += 0.3  #increase falling speed as the game progresses
                bucketSpeed = min(30, bucketSpeed + 1)  # increase bucket speed, capped at 30
            else:
                objectY += objectSpeed

            #check game over
            if objectY >= 400:
                gameOver = True

            #score
            scoreText = font.render("Score: " + str(score), True, textColor)
            screen.blit(scoreText, (10, 10))
        else:
            #show Game Over
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
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        if data.lower() == 'e':
            gameHasStarted = True
        if data == 'a':
            bucketX -= bucketSpeed  #use the dynamic bucket speed
        if data == 'd':
            bucketX += bucketSpeed
        if data == 'w':
            bucketY -= bucketSpeed
        if data == 's':
            bucketY += bucketSpeed

        #boundary check
        bucketX = max(0, min(bucketX, 600))
        bucketY = max(0, min(bucketY, 400))

        if data == 'r':  #restart the game
            print("Restarting game...")
            resetGame()  #reset all game variables

    conn.close()


#run threads
t1 = threading.Thread(target=gameThread)
t2 = threading.Thread(target=serverThread)
t1.start()
t2.start()
