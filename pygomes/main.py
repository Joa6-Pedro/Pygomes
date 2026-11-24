import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

playerPos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, size=None):
        super().__init__()
        loaded_image = pygame.image.load(image_path).convert_alpha()

        if size is not None:
            loaded_image = pygame.transform.smoothscale(loaded_image, size)

        self.image = loaded_image
        self.rect = self.image.get_rect(center=pos)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed=700, radius=5, color="yellow"):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.Vector2(pos)
        self.direction = direction
        self.speed = speed

    def update(self, dt, screen_rect):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

        # Remove a bala se sair da tela
        if not screen_rect.colliderect(self.rect):
            self.kill()


player = Player("./img/download.jfif", playerPos, size=(64, 64))
all_sprites = pygame.sprite.Group(player)
bullets = pygame.sprite.Group()

screen_rect = screen.get_rect()
shoot_cooldown = 0.15  # segundos entre tiros
time_since_last_shot = 0.0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza temporizadores
    time_since_last_shot += dt

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    move_dir = pygame.Vector2(0, 0)
    if keys[pygame.K_w]:
        move_dir.y -= 1
    if keys[pygame.K_s]:
        move_dir.y += 1
    if keys[pygame.K_a]:
        move_dir.x -= 1
    if keys[pygame.K_d]:
        move_dir.x += 1

    # Normaliza o vetor para que andar na diagonal não seja mais rápido
    if move_dir.length_squared() > 0:
        move_dir = move_dir.normalize()
        playerPos += move_dir * 300 * dt

    # Mantém o jogador dentro da tela
    playerPos.x = max(player.rect.width / 2, min(screen.get_width() - player.rect.width / 2, playerPos.x))
    playerPos.y = max(player.rect.height / 2, min(screen.get_height() - player.rect.height / 2, playerPos.y))
    player.rect.center = playerPos

    # Disparo com botão esquerdo do mouse (segurar ou clicar)
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0] and time_since_last_shot >= shoot_cooldown:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        aim_dir = mouse_pos - playerPos

        # Só atira se o mouse não estiver exatamente em cima do centro do jogador
        if aim_dir.length_squared() > 0:
            bullet = Bullet(playerPos, aim_dir.normalize())
            bullets.add(bullet)
            all_sprites.add(bullet)
            time_since_last_shot = 0.0

    # Atualiza projéteis
    bullets.update(dt, screen_rect)

    # Desenha tudo
    screen.fill("black")
    all_sprites.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()