import pygame
import random

def flappy_bird_game():
    # 游戏设置
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    GRAVITY = 0.1
    BIRD_JUMP = -3
    PIPE_WIDTH = 80
    PIPE_HEIGHT = 400
    BASE_PIPE_SPEED = 3
    SPEED_INCREASE = 0.1
    BIRD_WIDTH = 70
    BIRD_HEIGHT = 70
    GAP_SIZE = 200
    MIN_PIPE_HEIGHT = 100
    Width_pipes = 250

    # 创建屏幕
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    # 加载游戏资源并调整大小
    bird_img = pygame.image.load("bird.png")
    bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
    bird_rect = bird_img.get_rect()

    pipe_img = pygame.image.load("pipe.png")
    pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))
    pipe_rect = pipe_img.get_rect()

    # 初始化游戏变量
    bird_x = 50
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes = [{"x": SCREEN_WIDTH, "y": SCREEN_HEIGHT-50, "scored": False}]
    score = 0
    font = pygame.font.Font(None, 36)
    PIPE_SPEED = BASE_PIPE_SPEED

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = BIRD_JUMP

        bird_y += bird_velocity
        bird_velocity += GRAVITY
        bird_y = max(bird_y, 0)
        bird_y = min(bird_y, SCREEN_HEIGHT - bird_rect.height)

        for pipe in pipes:
            pipe["x"] -= PIPE_SPEED

        # bird_rect.topleft = (bird_x, bird_y)
        bird_rect.topleft = (bird_x + 10, bird_y + 10)
        bird_rect.width = BIRD_WIDTH - 20
        bird_rect.height = BIRD_HEIGHT - 20

        for pipe in pipes:
            pipe_rect.topleft = (pipe["x"], pipe["y"])
            if bird_rect.colliderect(pipe_rect):
                running = False

        pipes = [pipe for pipe in pipes if pipe["x"] > -PIPE_WIDTH]

        if pipes[-1]["x"] < SCREEN_WIDTH - Width_pipes:
            top_pipe_visible_height = random.randint(MIN_PIPE_HEIGHT, SCREEN_HEIGHT - GAP_SIZE - MIN_PIPE_HEIGHT)
            bottom_pipe_y = top_pipe_visible_height + GAP_SIZE
            pipes.append({"x": SCREEN_WIDTH, "y": bottom_pipe_y, "scored": False})

        for pipe in pipes:
            if pipe["x"] + PIPE_WIDTH < bird_x + BIRD_WIDTH and not pipe["scored"]:
                score += 1
                pipe["scored"] = True
                PIPE_SPEED = BASE_PIPE_SPEED + (score * SPEED_INCREASE)

        screen.fill((255, 255, 255))
        for pipe in pipes:
            screen.blit(pipe_img, (pipe["x"], pipe["y"]))
            screen.blit(pygame.transform.flip(pipe_img, False, True), (pipe["x"], pipe["y"] - GAP_SIZE - PIPE_HEIGHT))

        screen.blit(bird_img, (bird_x, bird_y))
        draw_text(screen, f"Score: {score}", 50, 20)
        pygame.display.flip()
        clock.tick(60)

    # 游戏结束界面
    def game_over_screen():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "RESTART"
                    if event.key == pygame.K_q:
                        return "QUIT"

            screen.fill((255, 255, 255))
            draw_text(screen, "Game Over", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
            draw_text(screen, f"Final Score: {score}", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
            draw_text(screen, "Press R to Restart, Q to Quit", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50)
            pygame.display.flip()
            clock.tick(60)

    return game_over_screen()

def draw_text(screen, text, x, y):
    text_surface = pygame.font.Font(None, 36).render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    pygame.init()
    action = "RESTART"
    while action == "RESTART":
        action = flappy_bird_game()
    pygame.quit()
