import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button, BtnEasy, BtnHard
from scoreboard import Scoreboard

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #Создание экземпляра статистики
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self) # don't work without this.
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #Кнопка play
        self.play_button = Button(self, "Play")
        self.play_easy = BtnEasy(self, "Easy mode")
        self.play_hard = BtnHard(self, "Hard mode")

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с вражеской силой."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Создает флот aliens."""
        """Создание пришельца и вычисление их количества в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определение количества рядов"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        """Создание флота вторжения"""
        for row_number in range(number_rows):   
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
    def _create_alien(self, alien_number, row_number):
        """Создает одного пришельца и размещает его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Проверяет, достиг ли флот края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Изменяет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
             
    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает игру при нажатии Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) 
        button_easy_clicked = self.play_easy.rect.collidepoint(mouse_pos)
        button_hard_clicked = self.play_hard.rect.collidepoint(mouse_pos)

        def other_settings():
            self.aliens.empty()
            self.bullets.empty()
            self.ship.center_ship()
            self._create_fleet()
            pygame.mouse.set_visible(False)

        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score() # 302 - 306 Дублировать логику для easy / hard
            self.sb.prep_level()
            self.sb.prep_ships()
            other_settings()
        elif button_easy_clicked and not self.stats.game_active:
            self.settings.initialize_easy_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            other_settings()
        elif button_hard_clicked and not self.stats.game_active:
            self.settings.initialize_hard_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            other_settings()

    def _check_keydown_events(self, event):
        """Отслеживание нажатия клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.rect.x += 1
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.rect.x -= 1
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self.stats.reset_stats()
                self.stats.game_active = True
                self.aliens.empty()
                self.bullets.empty()
                self.ship.center_ship()
                self._create_fleet()
                pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Создание нового снаряда и добавление его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keyup_events(self, event):
        """Отслеживание отпускания клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """Обновление положения пуль."""
        self.bullets.update()
        """Удаление пуль, вышедших за пределы экрана."""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Проверка столкновений пуль с пришельцами."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #Увеличнение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        """Обновляет изображение на экране и изменяет его цвет."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        # Кнопка play отображается в не активном режиме
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.play_easy.draw_button()
            self.play_hard.draw_button()

        pygame.display.flip()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        #Проверка коллизий (корабль - пришелец)
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Проверка, достигли ли пришельцы нижней части экрана."""
        screen_rect = self.screen.get_rect()    
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()