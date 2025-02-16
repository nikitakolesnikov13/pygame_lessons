import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
FPS = 30

# Цвета
WHITE = (255, 255, 255)

# Инициализация окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Animation")
clock = pygame.time.Clock()

# Класс для анимации
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # Загружаем спрайты для анимаций
        self.spritesheets = {
            'idle': self.load_spritesheet('Idle.png', 4),
            'walk_right': self.load_spritesheet('Walk.png', 6),
            'walk_left': self.load_spritesheet('Walk.png', 6, flip=True),  # Отражаем спрайты для ходьбы влево
        }
        self.current_animation = 'idle'
        self.sprites = self.spritesheets[self.current_animation]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=position)
        self.animation_speed = 0.05 # Скорость анимации
        self.last_update = pygame.time.get_ticks()

    def load_spritesheet(self, filename, frames, flip=False):
        spritesheet = pygame.image.load(filename).convert_alpha()
        frame_width = spritesheet.get_width() // frames
        frame_height = spritesheet.get_height()
        sprites = []
        for i in range(frames):
            frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            if flip:  # Если нужно отразить спрайт
                frame = pygame.transform.flip(frame, True, False)
            sprites.append(frame)
        return sprites

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:  # Обновление кадра каждые 100 мс
            self.last_update = now
            self.current_sprite += self.animation_speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]

    def change_animation(self, animation):
        if self.current_animation != animation:
            self.current_animation = animation
            self.sprites = self.spritesheets[self.current_animation]
            self.current_sprite = 0

# Создание персонажа
player = AnimatedSprite((100, 100))
all_sprites = pygame.sprite.Group(player)

# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление персонажем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.change_animation('walk_right')
        player.rect.x += 5
    elif keys[pygame.K_LEFT]:
        player.change_animation('walk_left')
        player.rect.x -= 5
    else:
        player.change_animation('idle')

    # Обновление и отрисовка
    all_sprites.update()
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()