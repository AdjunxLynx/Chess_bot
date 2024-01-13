import pygame


class ChessGame():
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.fps = 9999
        self.board_width = 800  # Width of the chessboard
        self.board_height = 800  # Height of the chessboard
        self.info_height = 50    # Height for the information area
        self.width = self.board_width  # Total width of the window
        self.height = self.board_height + 2 * self.info_height  # Total height of the window
        self.board_size = 8  # Size of the chessboard (8x8)
        self.square_size = self.board_width // self.board_size  # Size of a single square
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)  # Default font and size for text


    def draw_board(self):
        light_green = (118, 150, 86)
        dark_green = (238, 238, 210)
        colors = [light_green, dark_green]  # Chessboard colors
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size + self.info_height, self.square_size, self.square_size))

    def draw_info_area(self, fps):
        # Draw the top info area
        pygame.draw.rect(self.screen, pygame.Color("lightblue"), (0, 0, self.width, self.info_height))
        # Draw the bottom info area
        pygame.draw.rect(self.screen, pygame.Color("lightblue"),
                         (0, self.height - self.info_height, self.width, self.info_height))
        fps_text = self.font.render(f"FPS: {int(fps)}", True, pygame.Color("black"))
        self.screen.blit(fps_text, (10, 10))




    def run(self):
        running = True
        while running:
            fps = self.clock.get_fps()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(pygame.Color("black"))  # Fill the background
            self.draw_info_area(fps)
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()


if __name__ == "__main__":
    game = ChessGame()
    game.run()