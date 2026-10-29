
import pgzrun
from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Shadow Escape"

ANIMATION_SPEED = 0.15
INVULNERABILITY_TIME = 2.0

MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

game_state = MENU
sound_enabled = True


class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = Rect(x, y, width, height)

    def draw(self):
        screen.draw.filled_rect(self.rect, (45, 50, 75))
        screen.draw.rect(self.rect, (120, 150, 210))
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=26,
            color="white"
        )

    def contains(self, position):
        return self.rect.collidepoint(position)


class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.speed = 4

        self.frames = [
            "hero_idle_0",
            "hero_idle_1",
            "hero_idle_2",
            "hero_idle_3"
        ]

        self.frame_index = 0
        self.animation_timer = 0
        self.protection_timer = 0

        self.actor = Actor(self.frames[0], (x, y))

    def update(self):
        if keyboard.left or keyboard.a:
            self.x -= self.speed
        if keyboard.right or keyboard.d:
            self.x += self.speed
        if keyboard.up or keyboard.w:
            self.y -= self.speed
        if keyboard.down or keyboard.s:
            self.y += self.speed

        self.x = max(
            self.width // 2,
            min(WIDTH - self.width // 2, self.x)
        )
        self.y = max(
            self.height // 2,
            min(HEIGHT - self.height // 2, self.y)
        )

        self.animation_timer += 1 / 60

        if self.animation_timer >= ANIMATION_SPEED:
            self.animation_timer = 0
            self.frame_index = (
                self.frame_index + 1
            ) % len(self.frames)
            self.actor.image = self.frames[self.frame_index]

        self.actor.pos = (self.x, self.y)

        if self.protection_timer > 0:
            self.protection_timer -= 1 / 60

    def take_damage(self):
        if self.protection_timer <= 0:
            self.protection_timer = INVULNERABILITY_TIME
            return True
        return False

    def draw(self):
        if (
            self.protection_timer <= 0
            or int(self.protection_timer * 10) % 2 == 0
        ):
            self.actor.draw()


class Enemy:
    def __init__(self, x, y, speed, patrol_range):
        self.x = x
        self.y = y
        self.speed = speed
        self.start_x = x
        self.patrol_range = patrol_range
        self.size = 30
        self.direction = 1

    def update(self):
        self.x += self.speed * self.direction

        if self.x >= self.start_x + self.patrol_range:
            self.direction = -1
        elif self.x <= self.start_x - self.patrol_range:
            self.direction = 1

    def draw(self):
        enemy_rect = Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )
        screen.draw.filled_rect(enemy_rect, (220, 45, 55))


play_button = Button("PLAY", 300, 250, 200, 55)
sound_button = Button("SOUND: ON", 300, 325, 200, 55)
exit_button = Button("EXIT", 300, 400, 200, 55)
retry_button = Button("PLAY AGAIN", 300, 280, 200, 55)
menu_button = Button("MAIN MENU", 300, 350, 200, 55)


def play_effect(effect_name):
    if sound_enabled:
        try:
            getattr(sounds, effect_name).play()
        except (AttributeError, OSError):
            print("Could not play sound:", effect_name)


def play_background_music():
    if sound_enabled:
        try:
            music.set_volume(0.35)
            music.play("background")
        except (KeyError, OSError):
            print("Could not find background music in music/.")


def stop_background_music():
    music.stop()


def reset_game():
    global hero, enemies, lives

    hero = Hero(100, 300)

    enemies = [
        Enemy(300, 150, 2, 100),
        Enemy(500, 300, 3, 120),
        Enemy(350, 470, 2, 150)
    ]

    lives = 3


def on_mouse_down(pos):
    global game_state, sound_enabled

    if sound_enabled:
        play_effect("button_click")

    if game_state == MENU:
        if play_button.contains(pos):
            reset_game()
            game_state = PLAYING
            play_background_music()

        elif sound_button.contains(pos):
            sound_enabled = not sound_enabled
            sound_button.text = (
                "SOUND: ON" if sound_enabled else "SOUND: OFF"
            )

            if sound_enabled:
                play_background_music()
            else:
                stop_background_music()

        elif exit_button.contains(pos):
            raise SystemExit

    elif game_state == GAME_OVER:
        if retry_button.contains(pos):
            reset_game()
            game_state = PLAYING
            play_background_music()

        elif menu_button.contains(pos):
            game_state = MENU
            stop_background_music()


def update():
    global game_state, lives

    if game_state != PLAYING:
        return

    hero.update()

    hero_rect = Rect(
        hero.x - hero.width // 2,
        hero.y - hero.height // 2,
        hero.width,
        hero.height
    )

    for enemy in enemies:
        enemy.update()

        enemy_rect = Rect(
            enemy.x - enemy.size // 2,
            enemy.y - enemy.size // 2,
            enemy.size,
            enemy.size
        )

        if hero_rect.colliderect(enemy_rect):
            if hero.take_damage():
                lives -= 1
                play_effect("player_hurt")

                if lives <= 0:
                    game_state = GAME_OVER
                    stop_background_music()
                    play_effect("game_over")
                    break


def draw():
    screen.fill((20, 22, 35))

    if game_state == MENU:
        screen.draw.text(
            "SHADOW ESCAPE",
            center=(WIDTH // 2, 140),
            fontsize=54,
            color="white"
        )

        screen.draw.text(
            "Can you survive the shadows?",
            center=(WIDTH // 2, 195),
            fontsize=22,
            color="lightgray"
        )

        play_button.draw()
        sound_button.draw()
        exit_button.draw()

    elif game_state == PLAYING:
        for enemy in enemies:
            enemy.draw()

        hero.draw()

        screen.draw.text(
            f"Lives: {lives}",
            topleft=(20, 20),
            fontsize=28,
            color="white"
        )

        screen.draw.text(
            "Move: WASD or Arrow Keys",
            center=(WIDTH // 2, HEIGHT - 25),
            fontsize=20,
            color="lightgray"
        )

    elif game_state == GAME_OVER:
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, 180),
            fontsize=58,
            color="red"
        )

        screen.draw.text(
            "The shadows got you!",
            center=(WIDTH // 2, 230),
            fontsize=25,
            color="white"
        )

        retry_button.draw()
        menu_button.draw()


pgzrun.go()
