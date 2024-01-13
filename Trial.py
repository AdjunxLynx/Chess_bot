import pygame
import os
import numpy as np
import threading



class ChessGame:
    def __init__(self):
        # board display variables
        self.board_width = 800  # Width of the chessboard
        self.board_height = 800  # Height of the chessboard
        self.info_height = 50  # Height for the information area
        self.board_size = 8  # Size of the chessboard (8x8)
        self.square_size = self.board_width // self.board_size  # Size of a single square
        self.fps = 9999

        pygame.init()  # pygame variables # Initialize Pygame
        self.font = pygame.font.SysFont(None, 36)  # Default font and size for text
        self.width = self.board_width  # Total width of the window
        self.height = self.board_height + 2 * self.info_height  # Total height of the window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()

        # chess logic variables
        self.current_turn = 'white'
        self.selected_piece = None
        self.selected_pos = None

    def highlight_selected_piece(self):
        if self.selected_piece:
            row, col = self.selected_pos
            # Define the rectangle to highlight
            highlight_rect = (
            col * self.square_size, row * self.square_size + self.info_height, self.square_size, self.square_size)
            # Draw the highlight rectangle
            pygame.draw.rect(self.screen, (255, 255, 0), highlight_rect, 2)  # Yellow color, 2 pixels thick

    def handle_mouse_click(self, pos):
        row, col = self.get_board_position(pos)

        if self.selected_piece and (row, col) == self.selected_pos:
            # Deselect if the same piece is clicked again
            self.selected_piece, self.selected_pos = None, None
        elif self.is_valid_selection(row, col):
            # Select the piece
            self.selected_piece = self.board[row][col]
            self.selected_pos = (row, col)
        else:
            # Invalid selection, deselect any currently selected piece
            self.selected_piece, self.selected_pos = None, None

    def get_board_position(self, pos):
        # Convert screen position to board row and column
        x, y = pos
        row = (y - self.info_height) // self.square_size
        col = x // self.square_size
        return row, col

    def draw_possible_moves(self):
        if self.selected_piece:
            possible_moves = self.selected_piece.get_possible_moves(self.board)
            for move in possible_moves:
                if self.is_valid_move(move):
                    self.draw_move_dot(move)

    def draw_move_dot(self, position):
        row, col = position
        center_x = col * self.square_size + self.square_size // 2
        center_y = row * self.square_size + self.square_size // 2 + self.info_height
        pygame.draw.circle(self.screen, (0, 255, 0), (center_x, center_y), 10)  # Green dot

    def is_valid_move(self, move):
        # Check if the move is valid (e.g., not landing on a friendly piece)
        # Placeholder for actual validation logic
        return True

    def is_valid_selection(self, row, col):
        # Add logic to determine if the selection is valid (e.g., the piece belongs to the current player)
        # This is a placeholder for your validation logic
        return True  # Replace with actual validation

    def draw_pieces(self, ):
        threads = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row, col]
                thread = threading.Thread(target=self.draw_piece, args=(piece,))
                threads.append(thread)
                thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def draw_piece(self, piece):
        if piece is not None:
            x = piece.col * self.square_size
            y = piece.row * self.square_size + self.info_height
            self.screen.blit(piece.image, (x, y))

    def create_chess_board(self):
        # Initialize an 8x8 board with None
        board = np.full((8, 8), None)

        # Setup for white pieces
        board[0, 0] = Rook("white", 0, 0)
        board[0, 1] = Knight("white", 0, 1)
        board[0, 2] = Bishop("white", 0, 2)
        board[0, 3] = Queen("white", 0, 3)
        board[0, 4] = King("white", 0, 4)
        board[0, 5] = Bishop("white", 0, 5)
        board[0, 6] = Knight("white", 0, 6)
        board[0, 7] = Rook("white", 0, 7)
        for col in range(8):
            board[1, col] = Pawn("white", 1, col)

        # Setup for black pieces
        board[7, 0] = Rook("black", 7, 0)
        board[7, 1] = Knight("black", 7, 1)
        board[7, 2] = Bishop("black", 7, 2)
        board[7, 3] = Queen("black", 7, 3)
        board[7, 4] = King("black", 7, 4)
        board[7, 5] = Bishop("black", 7, 5)
        board[7, 6] = Knight("black", 7, 6)
        board[7, 7] = Rook("black", 7, 7)
        for col in range(8):
            board[6, col] = Pawn("black", 6, col)

        return board

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
        pygame.draw.rect(self.screen, pygame.Color("black"), (0, 0, self.width, self.info_height))
        # Draw the bottom info area
        pygame.draw.rect(self.screen, pygame.Color("black"), (0, self.height - self.info_height, self.width, self.info_height))

        # Display FPS
        fps_text = self.font.render(f"FPS: {int(fps)}", True, pygame.Color("white"))
        self.screen.blit(fps_text, (10, 10))

        # Display current turn
        turn_text = f"Turn: {self.current_turn.capitalize()}"
        turn_surface = self.font.render(turn_text, True, pygame.Color("white"))
        self.screen.blit(turn_surface, (self.width - 150, 10))  # Adjust position as needed

    def move_piece(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.board[start_row][start_col]

        if piece and self.is_legal_move(piece, start_pos, end_pos):
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = None
            piece.move(end_row, end_col)  # Update the piece's position
            # Additional move logic (e.g., handling captures) goes here

        if isinstance(self.board[end_row][end_col], Pawn):
            if end_pos in self.board[end_row][end_col].get_potential_moves(self.board, self.last_move):
                pass
        # Handle promotion or en passant

    def is_legal_move(self, piece, start_pos, end_pos):
        # Check if a move is legal. This is a placeholder for actual validation logic.
        # For example, checking if the end position is in the piece's potential moves.
        potential_moves = piece.get_potential_moves(self.board)
        return end_pos in potential_moves

    def draw_player_turn(self):
        turn_text = f"Turn: {self.current_turn.capitalize()}"
        text_surface = self.font.render(turn_text, True, pygame.Color("black"))
        self.screen.blit(text_surface, (self.width - 150, 10))  # Adjust position as needed

    def draw_game(self):
        self.draw_board()
        self.draw_pieces()
        self.highlight_selected_piece()
        self.draw_player_turn()
        if self.selected_piece:
            self.draw_possible_moves()

    def run(self):
        running = True
        self.board = self.create_chess_board()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

            self.draw_game()  # Calls the method to draw all game components
            pygame.display.flip()
            self.clock.tick(self.fps)  # Maintain a steady framerate

        pygame.quit()

class Piece(ChessGame):
    images = {}

    def __init__(self, color, row, col):
        super().__init__()
        self.color = color  # The color of the piece, e.g., 'white' or 'black'
        self.row = row      # The row position of the piece on the board
        self.col = col      # The column position of the piece on the board
        self.image = None   # This will hold the image of the piece for rendering
        self.load_image(self.square_size)

        # Update this method to record the last move
    def move_piece(self, start_pos, end_pos):
        # ... existing move logic ...
        self.last_move = (start_pos, end_pos)  # Record the move

    def load_image(self, square_size):
        # Construct the image key and filename
        image_key = f"{self.__class__.__name__.lower()}_{self.color}"
        filename = f"{image_key}.png"
        filepath = os.path.join("Images", filename)

        # Load the image if not already in the cache
        if image_key not in Piece.images:
            loaded_image = pygame.image.load(filepath)
            Piece.images[image_key] = pygame.transform.scale(loaded_image, (square_size, square_size))

        self.image = Piece.images[image_key]


    def move(self, row, col):
        """Move the piece to a new position."""
        self.row = row
        self.col = col


    def get_possible_moves(self, board):

        """
        This method should be overridden by each specific piece type.
        It should return a list of legal moves for the piece.
        """
        raise NotImplementedError("This method should be implemented by subclasses")

class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        # Additional King-specific initialization can go here

class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        # Additional Queen-specific initialization can go here

class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        # Additional Rook-specific initialization can go here

class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        # Additional Bishop-specific initialization can go here

class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        # Additional Knight-specific initialization can go here

class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        # Additional Pawn-specific initialization can go here

    def get_potential_moves(self, board, last_move):
        moves = []
        direction = 1 if self.color == 'white' else -1
        start_row = 1 if self.color == 'white' else 6

        # Single move forward
        if board[self.row + direction][self.col] is None:
            moves.append((self.row + direction, self.col))
            # En passant logic
        if last_move:
            last_start_pos, last_end_pos = last_move
            last_piece = board[last_start_pos[0]][last_start_pos[1]]
            if isinstance(last_piece, Pawn) and abs(last_start_pos[0] - last_end_pos[0]) == 2:
                # Check if the pawn is adjacent to the current pawn
                if last_end_pos[1] == self.col + 1 or last_end_pos[1] == self.col - 1:
                    en_passant_row = self.row + direction
                    en_passant_col = last_end_pos[1]
                    moves.append((en_passant_row, en_passant_col))

        # Double move from start position
        if self.row == start_row and board[self.row + 2 * direction][self.col] is None:
            moves.append((self.row + 2 * direction, self.col))

        promotion_row = 0 if self.color == 'white' else 7
        if self.row + direction == promotion_row:
            pass

        # ... add capture moves and other logic ...

        return moves










if __name__ == "__main__":
    game = ChessGame()
    game.run()