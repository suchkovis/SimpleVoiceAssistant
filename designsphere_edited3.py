import pygame
import math
import sys


class PulsatingSphereUI:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.LIGHT_THEME = (255, 255, 255)
        self.DARK_THEME = (30, 30, 30)
        self.BUTTON_COLOR = (70, 70, 70)
        self.BUTTON_HOVER_COLOR = (100, 100, 100)
        self.TEXT_COLOR = (255, 255, 255)

        # Инициализация окна
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Пульсирующая сфера")

        # Основные параметры сферы
        self.center_x, self.center_y = self.WIDTH // 2, self.HEIGHT // 2
        self.radius_base = 100
        self.amplitude = 20
        self.speed = 6.0
        self.theme = self.DARK_THEME
        self.time = 0
        self.state = "rest"  # rest, processing, implementation
        self.running = True
        self.settings_open = False  # Флаг для отображения настроек

        # Цветовые режимы
        self.colors = {
            "rest": [(255, 255, 0), (255, 165, 0)],  # Желтый -> Оранжевый
            "processing": [(0, 255, 0), (0, 0, 255)],  # Зеленый -> Синий
            "implementation": [(128, 0, 128), (255, 0, 0)],  # Фиолетовый -> Красный
        }
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)

    def set_state_rest(self):
        """Установить состояние 'Покой'."""
        self.state = "rest"
        self.amplitude = 10

    def set_state_processing(self):
        """Установить состояние 'Обработка'."""
        self.state = "processing"
        self.amplitude = 20

    def set_state_implementation(self):
        """Установить состояние 'Реализация'."""
        self.state = "implementation"
        self.amplitude = 40

    def set_theme_light(self):
        """Установить светлую тему."""
        self.theme = self.LIGHT_THEME

    def set_theme_dark(self):
        """Установить темную тему."""
        self.theme = self.DARK_THEME

    def _get_gradient_color(self):
        """Получить текущий цвет для градиентного режима."""
        colors = self.colors[self.state]
        color1, color2 = colors
        factor = (math.sin(self.time) + 1) / 2  # Синус от 0 до 1
        return [
            int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3)
        ]

    def _draw_text(self, surface, text, pos, color):
        """Отрисовка текста."""
        text_surface = self.font.render(text, True, color)
        surface.blit(text_surface, pos)

    def _create_button(self, surface, text, rect, action=None):
        """Создание кнопки."""
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        pygame.draw.rect(surface, self.BUTTON_HOVER_COLOR if is_hovered else self.BUTTON_COLOR, rect)
        self._draw_text(surface, text, (rect.x + 10, rect.y + 5), self.TEXT_COLOR)
        return is_hovered and pygame.mouse.get_pressed()[0]

    def run(self):
        """Основной игровой цикл."""
        while self.running:
            self.time += self.clock.get_time() / 1000 * self.speed
            self.screen.fill(self.theme)

            if self.settings_open:
                # Отрисовка настроек
                settings_rect = pygame.Rect(self.WIDTH // 4, self.HEIGHT // 4, self.WIDTH // 2, self.HEIGHT // 2)
                pygame.draw.rect(self.screen, self.BUTTON_COLOR, settings_rect)

                light_theme_button = pygame.Rect(settings_rect.x + 50, settings_rect.y + 50, 200, 40)
                dark_theme_button = pygame.Rect(settings_rect.x + 50, settings_rect.y + 110, 200, 40)
                back_button = pygame.Rect(settings_rect.x + 50, settings_rect.y + 170, 200, 40)

                if self._create_button(self.screen, "Светлая тема", light_theme_button):
                    self.set_theme_light()
                if self._create_button(self.screen, "Темная тема", dark_theme_button):
                    self.set_theme_dark()
                if self._create_button(self.screen, "Назад", back_button):
                    self.settings_open = False
            else:
                # Получение текущего цвета
                current_color = self._get_gradient_color()

                # Отрисовка пульсирующей сферы
                radius = self.radius_base + self.amplitude * (0.5 + 0.5 * math.sin(self.time))
                pygame.draw.circle(self.screen, current_color, (self.center_x, self.center_y), int(radius))

                # Отрисовка кнопок управления
                rest_button = pygame.Rect(10, 10, 150, 40)
                processing_button = pygame.Rect(10, 60, 150, 40)
                implementation_button = pygame.Rect(10, 110, 150, 40)
                settings_button = pygame.Rect(self.WIDTH - 160, 10, 150, 40)

                if self._create_button(self.screen, "Покой", rest_button):
                    self.set_state_rest()
                if self._create_button(self.screen, "Обработка", processing_button):
                    self.set_state_processing()
                if self._create_button(self.screen, "Реализация", implementation_button):
                    self.set_state_implementation()
                if self._create_button(self.screen, "Настройки", settings_button):
                    self.settings_open = True

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Обновление экрана
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


# Пример использования
if __name__ == "__main__":
    ui = PulsatingSphereUI()
    ui.run()
