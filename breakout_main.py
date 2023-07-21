import pygame
import random

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")
clock = pygame.time.Clock()
running = True
dt = 0

pygame.font.init()
font = pygame.font.Font(None, 50)
score = 0

#player setup
player_pos = pygame.Vector2(550, 680)
rect_size = (100,25)
rect_color = (255,0,0)

#ball setup
ball_position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
original_ball_velocity = pygame.Vector2(random.uniform(-40, 40), -220)
ball_velocity = original_ball_velocity.copy()
ball_radius = 10
gravity = pygame.Vector2(0, 1)

game_over = False
retry_button = pygame.Rect(0, 0, 0, 0)
exit_button = pygame.Rect(0, 0, 0, 0)


def brick_wall():
    bricks = []
    yellow_row1 = pygame.Rect(-75, 275, 70, 20)
    yellow_row2 = pygame.Rect(-75, 250, 70, 20)
    green_row1 = pygame.Rect(-75, 225, 70, 20)
    green_row2 = pygame.Rect(-75, 200, 70, 20)
    orange_row1 = pygame.Rect(-75, 175, 70, 20)
    orange_row2 = pygame.Rect(-75, 150, 70, 20)
    red_row1 = pygame.Rect(-75, 125, 70, 20)
    red_row2 = pygame.Rect(-75, 100, 70, 20)
    for brick in range(16):
        yellow_row1[0] += 80
        bricks.append((pygame.Rect(5 + 80 * brick, 275, 70, 20), (255, 255, 0)))

        yellow_row2[0] += 80
        bricks.append((pygame.Rect(5 + 80 * brick, 250, 70, 20), (255, 255, 0)))

        green_row1[0] += 80
        bricks.append((pygame.Rect(5 + 80 * brick, 225, 70, 20), (0, 255, 0)))

        green_row2[0] += 80
        bricks.append((pygame.Rect(5 + 80 * brick, 200, 70, 20), (0, 255, 0)))

        orange_row1[0] += 80
        bricks.append((pygame.Rect(5 + 80 * brick, 175, 70, 20), (255, 191, 0)))

        orange_row2[0] += 80
        bricks.append((pygame.Rect(5 + 80 * brick, 150, 70, 20), (255, 191, 0)))

        red_row1[0] += 80
        bricks.append((pygame.Rect(5 + 80 * brick, 125, 70, 20), (255, 0, 0)))

        red_row2[0] += 80
        bricks.append((pygame.Rect(5 + 80 * brick, 100, 70, 20), (255, 0, 0)))

    return bricks

brick_wall()

colors_hit = set()

bricks = brick_wall()

while running:

    screen.fill('black')

    dt = clock.tick(144) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_over and event.type == pygame.MOUSEBUTTONDOWN:  # handle button clicks when game is over
            x, y = pygame.mouse.get_pos()
            if retry_button.collidepoint((x, y)):
                # reset to restart the game
                player_pos = pygame.Vector2(550, 680)
                ball_position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
                ball_velocity = pygame.Vector2(random.uniform(-40, 40), -220)

                bricks = brick_wall()

                game_over = False
                score = 0
            elif exit_button.collidepoint((x, y)):
                running = False


    if not game_over:
        rect = pygame.Rect(player_pos.x, player_pos.y, *rect_size) #player's paddle
        pygame.draw.rect(screen, rect_color, rect)

        # draw remaining bricks
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_pos.x > 5:
                player_pos.x -= 700 * dt
        if keys[pygame.K_d] and player_pos.x < 1145:
                player_pos.x += 700 * dt

        #ball physics
        ball_velocity += gravity * dt
        ball_position += ball_velocity * dt
        ball_rect = pygame.Rect(ball_position.x - ball_radius, ball_position.y - ball_radius,ball_radius * 2, ball_radius * 2)

        # border collision
        if ball_position.x - ball_radius < 0:  # left border
            ball_position.x = ball_radius
            ball_velocity.x *= -1
        elif ball_position.x + ball_radius > SCREEN_WIDTH:  # right border
            ball_position.x = SCREEN_WIDTH - ball_radius
            ball_velocity.x *= -1

        if ball_position.y - ball_radius < 90:  # top border
            ball_position.y = 90 + ball_radius
            ball_velocity.y *= -1
        elif ball_position.y + ball_radius > SCREEN_HEIGHT:  # bottom border
            game_over = True

        # paddle
        if ball_rect.colliderect(rect):
            if ball_velocity.y > 0:  #reverse y velocity if ball is moving downward
                ball_velocity.y *= -1
                relative_intersect_x = (rect.centerx - ball_position.x) / rect.width
                ball_velocity.x = relative_intersect_x * -220

        for i, brick in enumerate(bricks):
            brick_rect, color = brick  # unpack tuple
            if ball_rect.colliderect(brick_rect):
                overlap = ball_rect.clip(brick_rect)
                if overlap.width >= overlap.height:  # hit brick on top or bottom
                    ball_velocity.y *= -1
                else:  # hit brick on left or right
                    ball_velocity.x *= -1

                # increase the speed by 30% if it's not a yellow brick, and it's the first time hitting this color
                if color != (255, 255, 0) and color not in colors_hit:
                    ball_velocity *= 1.3
                colors_hit.add(color)


                del bricks[i]  # delete the brick from the list
                if color == (255, 255, 0):
                    score += 1
                elif color == (0, 255, 0):
                    score += 2
                elif color == (255, 191, 0):
                    score += 3
                elif color == (255, 0, 0):
                    score += 5
                break

        pygame.draw.circle(screen, "gray", (int(ball_position.x), int(ball_position.y)), ball_radius)


        score_surface = font.render('Score: ' + str(score), True, (255, 255, 255))
        screen.blit(score_surface, (20, 20))


    else:
        msg_surface = font.render(f'Your score: {score}', True, (255, 255, 255))
        screen.blit(msg_surface, (SCREEN_WIDTH // 2 - msg_surface.get_width() // 2,
                                  SCREEN_HEIGHT // 2 - msg_surface.get_height() // 2 - 50))

        retry_button = pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50))
        retry_surface = font.render('Retry', True, (0, 0, 0))
        screen.blit(retry_surface, (SCREEN_WIDTH // 2 - retry_surface.get_width() // 2, SCREEN_HEIGHT // 2 + retry_surface.get_height() // 2 - 10))

        exit_button = pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50))
        exit_surface = font.render('Exit', True, (0, 0, 0))
        screen.blit(exit_surface, (SCREEN_WIDTH // 2 - exit_surface.get_width() // 2, SCREEN_HEIGHT // 2 + exit_surface.get_height() // 2 + 90))

    pygame.display.flip()

pygame.quit()
