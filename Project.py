import arcade

# Параметры экрана
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Крестики Нолики"


class Game(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title, cell_size):
        super().__init__(screen_width, screen_height, screen_title)

        self.cell_size = cell_size
        self.rows = screen_height // cell_size
        self.cols = screen_width // cell_size
        self.dots_list = arcade.shape_list.ShapeElementList()
        self.grid = [[0 for _ in range(5)] for _ in range(5)]
        self.game_over = False
        self.current_player = 1
        self.count_red = 5
        self.count_green = 5
        self.count_blue = 5

    def setup(self): #Создаёт вертикальные и горизонтальные линии сетки.Линии добавляются в self.dots_list для последующей отрисовки.
        for i in range(5):
            x = 180 * (i + 1)
            y = 180 * (i + 1)
            self.dots_list.append(arcade.shape_list.create_line(x, 0, x, 900, arcade.color.BLACK, 5))
            self.dots_list.append(arcade.shape_list.create_line(0, y, 900, y, arcade.color.BLACK, 5))

    def on_draw(self): #Отрисовка
        self.clear()
        arcade.draw_rect_outline(arcade.rect.XYWH(1050, 500, 115, 115), arcade.color.BLACK, 4)
        arcade.draw_text("Игрок", 1020, 570, arcade.color.BLACK, 17)
        arcade.draw_text("ПКМ - удалить фигуру", 950, 850, arcade.color.BLACK, 17)
        arcade.draw_text("Ходы", 1000, 230, arcade.color.BLACK, 17)
        arcade.draw_text(f"Красный - {self.count_red} ходов", 950, 160, arcade.color.BLACK, 17)
        arcade.draw_text(f"Синий - {self.count_blue} ходов", 950, 110, arcade.color.BLACK, 17)
        arcade.draw_text(f"Зелёный - {self.count_green} ходов", 950, 60, arcade.color.BLACK, 17)

        arcade.set_background_color(arcade.color.WHITE)
        self.dots_list.draw()
        for row in range(5):
            for col in range(5):
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2
                if self.grid[row][col] == 1:
                    # Рисуем крестик
                    size = self.cell_size // 3
                    arcade.draw_line(x - size, y - size, x + size, y + size, arcade.color.RED, 4)
                    arcade.draw_line(x - size, y + size, x + size, y - size, arcade.color.RED, 4)

                elif self.grid[row][col] == 2:  # Рисуем нолик
                    radius = self.cell_size // 3
                    arcade.draw_circle_outline(x, y, radius, arcade.color.BLUE, 4)

                elif self.grid[row][col] == 3:
                    arcade.draw_triangle_outline(x - 70, y - 35, x, y + 70, x + 70, y - 35, arcade.color.GREEN, 4)

        if self.game_over:
            if self.winner == 1:
                text = "Крестики победили! Жми R, чтобы сыграть снова."
            elif self.winner == 2:
                text = "Нолики торжествуют! Жми R, чтобы отыграться."
            elif self.winner == 3:
                text = "Треугольники победили! Жми R, чтобы сыграть снова."
            else:
                text = "Ничья. Жми R!"
            arcade.draw_text(text, 290, SCREEN_HEIGHT // 2, arcade.color.BLACK, 15, align="center")
        if self.current_player == 1:
            arcade.draw_line(1100, 450, 1000, 550, arcade.color.RED, 4)
            arcade.draw_line(1000, 450, 1100, 550, arcade.color.RED, 4)
        elif self.current_player == 2:
            arcade.draw_circle_outline(1050, 500, 50, arcade.color.BLUE, 4)
        else:
            arcade.draw_triangle_outline(1000, 500 - 40, 1050, 545, 1050 + 50, 500 - 40, arcade.color.GREEN, 4)

    def on_mouse_press(self, x, y, button, modifiers): #Обработка кликов мыши.
        if self.game_over:
            return  # Игру уже выиграли

        col = int(x // self.cell_size)
        row = int(y // self.cell_size)

        if x <= 900 and button == arcade.MOUSE_BUTTON_LEFT:
            if self.grid[row][col] == 0:
                self.grid[row][col] = self.current_player
                self.check_winner()
                if not self.game_over:
                    if self.current_player == 1:
                        self.current_player = 2
                        self.count_red -= 1
                        if self.count_red < 0:
                            self.count_red = 0
                            self.grid[row][col] = 0
                    elif self.current_player == 2:
                        self.current_player = 3
                        self.count_blue -= 1
                        if self.count_blue < 0:
                            self.count_blue = 0
                            self.grid[row][col] = 0
                    elif self.current_player == 3:
                        self.current_player = 1
                        self.count_green -= 1
                        if self.count_green < 0:
                            self.count_green = 0
                            self.grid[row][col] = 0

        if button == arcade.MOUSE_BUTTON_RIGHT: #ПКМ - Удаления фигуры
            if self.grid[row][col] == self.current_player:
                if self.grid[row][col] == 1:
                    self.grid[row][col] = 0
                    self.count_red += 1
                elif self.grid[row][col] == 2:
                    self.grid[row][col] = 0
                    self.count_blue += 1
                else:
                    self.grid[row][col] = 0
                    self.count_green += 1

        if all(cell != 0 for row in self.grid for cell in row): #Ничья
            self.winner = 0
            self.game_over = True

    def check_winner(self):
        lines = []

        # Горизонтали и вертикали
        lines.extend(self.grid)  # Строки
        lines.extend([[self.grid[r][c] for r in range(5)] for c in range(5)])  # Столбцы

        # Диагонали
        lines.append([self.grid[i][i] for i in range(5)])
        lines.append([self.grid[i][4 - i] for i in range(5)])

        for line in lines:
            if line == [1, 1, 1, 1, 1]:
                self.winner = 1
                self.game_over = True
                return
            elif line == [2, 2, 2, 2, 2]:
                self.winner = 2
                self.game_over = True
                return
            elif line == [3, 3, 3, 3, 3]:
                self.winner = 3
                self.game_over = True

    def on_key_press(self, button, modifiers):
        if button == arcade.key.R:
            self.grid = [[0 for _ in range(5)] for _ in range(5)]
            self.game_over = False
            self.current_player = 1
            self.count_red = 5
            self.count_green = 5
            self.count_blue = 5


def main():
    game = Game(SCREEN_WIDTH + 300, SCREEN_HEIGHT, SCREEN_TITLE, 180)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
