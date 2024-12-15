"""
Module for creating a Text Area.

It is a multi-line control for editing plain text.
"""


from pgpyui import *


class TextArea:
    """A multi-line control for editing plain text with a border."""

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        font_size: int,
        max_symbols: int,
        is_enter: bool = True,
        font: str = "Comic Sans MS",
    ) -> None:

        self.rect = pygame.Rect(*position, *size)
        self.bg_color = pygame.Color("white")
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, self.font_size)
        self.font_color = pygame.Color("black")
        self.lines = [""]  # List of strings, one per line
        self.active = False  # Track whether the text area is active
        self.border_color = pygame.Color(200, 200, 200)  # Light gray
        self.border_width = 5

        self.max_symbols = max_symbols
        self.is_enter = is_enter
        self.cursor_pos = (0, 0)  # (line_index, char_index)

    def __add_text(self, text: str) -> None:
        """Adds text, handling line wrapping and max symbols."""
        total_chars = sum(len(line) for line in self.lines)
        available_chars = self.max_symbols - total_chars

        if available_chars <= 0:
            return  # No space left

        new_text = text
        line_index = self.cursor_pos[0]
        char_index = self.cursor_pos[1]

        if new_text == '\n':  # Handle newline separately
            self.lines.append("")  # Append a new empty line
            self.cursor_pos = (self.cursor_pos[0] + 1, 0)
            return  # Exit early after handling newline

        # Insert text if not a newline
        self.lines[line_index] = self.lines[line_index][:char_index] + new_text + self.lines[line_index][char_index:]

        # Handle line wrapping
        while True:
            line = self.lines[line_index]
            rendered_text = self.font.render(line, True, self.font_color)
            if rendered_text.get_width() <= self.rect.width - 2 * self.border_width:
                break

            # Split line if too long
            last_space = line.rfind(" ", 0, len(line) - 1)
            if last_space == -1:
                last_space = len(line) - 1

            next_line = line[last_space + 1:]
            self.lines[line_index] = line[:last_space]
            self.lines.insert(line_index + 1, next_line)
            line_index += 1
            self.cursor_pos = (line_index, 0)



    def draw(self, window: pygame.Surface) -> None:
        """Draws the text area with a light gray border."""
        # Draw the border
        pygame.draw.rect(window, self.border_color, self.rect, self.border_width)

        # Draw the inner rectangle (background)
        inner_rect = self.rect.copy()
        inner_rect.inflate_ip(-2 * self.border_width, -2 * self.border_width)  # Adjust for border width
        pygame.draw.rect(window, self.bg_color, inner_rect)

        # Draw the text
        y_offset = self.rect.top + self.border_width
        for line in self.lines:
            text_surface = self.font.render(line, True, self.font_color)
            window.blit(text_surface, (self.rect.left + self.border_width, y_offset))
            y_offset += self.font_size


    def check_events(self, event: pygame.event.Event) -> None:
        """Handles events for the text area."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN and self.is_enter:
                self.__add_text("\n")
                self.lines.append("")
                self.cursor_pos = (self.cursor_pos[0] + 1, 0)
            elif event.key == pygame.K_BACKSPACE:
                line_index, char_index = self.cursor_pos
                if char_index > 0:
                    self.lines[line_index] = self.lines[line_index][:char_index - 1] + self.lines[line_index][char_index:]
                    self.cursor_pos = (line_index, char_index - 1)
                elif line_index > 0:
                    self.lines[line_index - 1] += self.lines[line_index]
                    del self.lines[line_index]
                    self.cursor_pos = (line_index - 1, len(self.lines[line_index - 1]))
            else:
                self.__add_text(event.unicode)
                self.cursor_pos = (self.cursor_pos[0], self.cursor_pos[1] + 1)


    def data_return(self) -> list:
        """Returns the text as a list of lines."""
        return self.lines
