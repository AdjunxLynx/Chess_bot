import pygame
import os
import numpy as np
import pygame.font


class Piece:
    _images = {}
    def __init__(self, row, col, color, square_size, piece_type):
        self.row = row
        self.col = col
        self.color = color
        self.square_size = square_size
        self.piece_type = piece_type
        self.image = self.load_image(piece_type, color, square_size)
        self.first_move = True
        self.move_cache = None
        
    def get_potential_moves(self, board, last_move):
        if self.move_cache is not None:
            return self.move_cache
        else:
            self.move_cache = self.calculate_potential_moves(board, last_move, game)
            return self.move_cache
        
    def invalidate_cache(self):
        self.move_cache = None

    @classmethod
    def load_image(cls, piece_type, color, square_size):
            key = (piece_type, color)
            if key not in cls._images:
                filename = f'{piece_type}_{color}.png'
                path = os.path.join('Images', filename)
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (square_size, square_size))
                cls._images[key] = image
            return cls._images[key]


    def draw(self, win):
        x = self.col * self.square_size
        y = self.row * self.square_size
        win.blit(self.image, (x, y))


class Pawn(Piece):
    piece_type = 'pawn'

    def __init__(self, row, col, color, square_size):
        super().__init__(row, col, color, square_size, self.piece_type)
        self.first_move = True

    def calculate_potential_moves(self, board, last_move, game):
        moves = []
        direction = -1 if self.color == 'white' else 1  
        # White moves up (-1), Black moves down (+1)
        start_row, start_col = self.row, self.col

        # Forward move
        if self.is_valid_move(start_row + direction, start_col, board):
            moves.append((start_row + direction, start_col))
            # Two squares forward on first move
            if self.first_move and self.is_valid_move(start_row + 2 * direction, start_col, board):
                moves.append((start_row + 2 * direction, start_col))

        # Diagonal captures
        for d_col in [-1, 1]:
            if self.is_valid_capture(start_row + direction, start_col + d_col, board):
                moves.append((start_row + direction, start_col + d_col))
        print(f"moves before en passent calc: {moves}")
                
        if last_move:  # Checking if there was a last move
            last_piece, (start_row, start_col), (end_row, end_col) = last_move
            if isinstance(last_piece, Pawn) and abs(start_row - end_row) == 2:
                # Check if the last move was a two-square pawn move adjacent to this pawn
                if self.row == end_row and abs(self.col - end_col) == 1:
                    en_passant_row = end_row + direction  
                    # The row where the en passant capture would end up
                    moves.append((en_passant_row, end_col))

        return moves


    def is_valid_move(self, row, col, board):
        # Check if the move is within board bounds and the target square is empty
        return 0 <= row < 8 and 0 <= col < 8 and board[row][col] is None

    def is_valid_capture(self, row, col, board):
        # Check if the capture move is within board bounds and captures an opponent's piece
        return 0 <= row < 8 and 0 <= col < 8 and board[row][col] is not None and board[row][col].color != self.color
    
    
class Rook(Piece):
    piece_type = "rook"
    
    def __init__(self, row, col, color, square_size):
        super().__init__(row, col, color, square_size, self.piece_type)
        # Additional Rook-specific initialization (if any)

    def calculate_potential_moves(piece, board, last_move, game):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        for dir in directions:
            for i in range(1, 8):
                end_row = piece.row + dir[0] * i
                end_col = piece.col + dir[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Check if within board boundaries
                    end_piece = board[end_row][end_col]
                    if end_piece is None:  # Empty square
                        moves.append((end_row, end_col))
                    elif end_piece.color != piece.color:  # Capture opponent's piece
                        moves.append((end_row, end_col))
                        break
                    else:  # Blocked by own piece
                        break
                else:  # Off the board
                    break

        return moves
    
    
class Bishop(Piece):
    piece_type = "bishop"
    def __init__(self, row, col, color, square_size):
        super().__init__(row, col, color, square_size, self.piece_type)
        # Additional Bishop-specific initialization (if any)
    def calculate_potential_moves(piece, board, last_move, game):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonal directions

        for dir in directions:
            for i in range(1, 8):
                end_row = piece.row + dir[0] * i
                end_col = piece.col + dir[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Check if within board boundaries
                    end_piece = board[end_row][end_col]
                    if end_piece is None:  # Empty square
                        moves.append((end_row, end_col))
                    elif end_piece.color != piece.color:  # Capture opponent's piece
                        moves.append((end_row, end_col))
                        break
                    else:  # Blocked by own piece
                        break
                else:  # Off the board
                    break

        return moves
    

class Queen(Piece):
    piece_type = 'queen'

    def __init__(self, row, col, color, square_size):
        super().__init__(row, col, color, square_size, self.piece_type)

    def calculate_potential_moves(self, board, last_move, game):
        rook_moves = Rook.calculate_potential_moves(self, board, last_move, game)
        bishop_moves = Bishop.calculate_potential_moves(self, board, last_move, game)
        return rook_moves + bishop_moves
    

class Knight(Piece):
    piece_type = "knight"
    
    def __init__(self, row, col, color, square_size):
        super().__init__(row, col, color, square_size, self.piece_type)


    def calculate_potential_moves(self, board, last_move, game):
        moves = []
        row, col = self.row, self.col
        move_offsets = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

        for offset in move_offsets:
            end_row, end_col = row + offset[0], col + offset[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:  # Check if within board boundaries
                end_piece = board[end_row][end_col]
                if end_piece is None or end_piece.color != self.color:  # Either capture or move to empty square
                    moves.append((end_row, end_col))

        return moves


class King(Piece):
    piece_type = "king"
    def __init__(self, row, col, color, square_size):
        super().__init__(row, col, color, square_size, self.piece_type)
        
    def calculate_potential_moves(self, board, last_move, game):
        moves = []
        row, col = self.row, self.col
        move_offsets = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]  # Moves in all eight directions

        for offset in move_offsets:
            end_row, end_col = row + offset[0], col + offset[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:  # Check if within board boundaries
                end_piece = board[end_row][end_col]
                if end_piece is None or end_piece.color != self.color:  # Either move to empty square or capture
                    moves.append((end_row, end_col))
                    
        if self.can_castle_kingside(self.row, self.col, board, game):
                moves.append((self.row, self.col + 2))
                
        if self.can_castle_queenside(self.row, self.col, board, game):
            moves.append((self.row, self.col - 2))
            
        return moves


    
    def can_castle_queenside(self, king_row, king_col, board, game):
        # Check if squares between the king and the queenside rook are empty
        if all(board[king_row][col] is None for col in range(king_col - 1, king_col - 4, -1)):
            rook = board[king_row][king_col - 4]
            if isinstance(rook, Rook) and rook.first_move:
                # Ensure the king does not pass through a square under attack
                if not game.is_king_in_check(board, 'white' if king_row == 7 else 'black') and not game.is_square_under_attack(king_row, king_col - 1, board) and not game.is_square_under_attack(king_row, king_col - 2, board):
                    return True
        return False

    def can_castle_kingside(self, king_row, king_col, board, game):
        # Logic for kingside castling, use king_row and king_col
        if board[king_row][king_col + 1] is None and board[king_row][king_col + 2] is None:
            rook = board[king_row][king_col + 3]
            if isinstance(rook, Rook) and rook.first_move:
                # Ensure the king does not pass through a square under attack
                if not game.is_king_in_check(board, 'white' if king_row == 7 else 'black') and not game.is_square_under_attack(king_row, king_col + 1, board) and not game.is_square_under_attack(king_row, king_col + 2, board):
                    return True
        return False
    
    
class ChessGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 800
        self.ROWS, self.COLS = 8, 8
        self.fps = 30
        self.SQUARE_SIZE = self.WIDTH // self.COLS
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Chess Game')
        self.pieces = self.create_pieces()
        self.selected_piece = None
        self.possible_moves = []
        self.turn = 'white'
        pygame.font.init()  
        self.font = pygame.font.SysFont('Arial', 24)
        self.last_move = None
        
    def describe_board(self, board):
        piece_descriptions = {
            'Rook': 'rook',
            'Knight': 'knight',
            'Bishop': 'bishop',
            'Queen': 'queen',
            'King': 'king',
            'Pawn': 'pawn'
        }

        described_board = [
            ', '.join(
                f"{piece.color} {piece_descriptions[type(piece).__name__]}" if piece else "empty"
                for piece in row
            )
            for row in board
        ]

        return '\n'.join(described_board)
    
    def calculate_potential_moves(self, piece):
        moves = piece.calculate_potential_moves(self.pieces, self.last_move, self)
        return moves

    def move_piece(self, start_row, start_col, end_row, end_col):
        moving_piece = self.pieces[start_row][start_col]
        if moving_piece and moving_piece.color == self.turn:
            potential_moves = self.calculate_potential_moves(moving_piece)
            if (end_row, end_col) in potential_moves:
                # Simulate the move
                simulated_board = self.simulate_move(start_row, start_col, end_row, end_col)
                if not self.is_king_in_check(simulated_board, self.turn):
                    # Perform the move
                    self.pieces[end_row][end_col] = moving_piece
                    self.pieces[start_row][start_col] = None
                    moving_piece.row, moving_piece.col = end_row, end_col
                    moving_piece.first_move = False
                    
                    
                    # Handle castling (move the rook)
                    if moving_piece.piece_type == "king" and abs(start_col - end_col) == 2:
                        # Kingside castling
                        if end_col > start_col:
                            rook = self.pieces[start_row][7]
                            self.pieces[start_row][5] = rook
                            self.pieces[start_row][7] = None
                            rook.col = 5
                        # Queenside castling
                        else:
                            rook = self.pieces[start_row][0]
                            self.pieces[start_row][3] = rook
                            self.pieces[start_row][0] = None
                            rook.col = 3
                        rook.first_move = False  # The rook has moved
                    
                    self.last_move = (moving_piece, (start_row, start_col), (end_row, end_col))

                    return True
                else:
                    print("Illegal move: would place king in check.")
            else:
                print("Illegal move: not a valid destination.")
        else:
            if not moving_piece:
                print("No piece selected to move.")
            else:
                print("Not your turn.")
        return False

    def invalidate_relevant_caches(self, start_row, start_col, end_row, end_col):
        # Invalidate the cache of the moved piece
        self.pieces[end_row][end_col].invalidate_cache()
        # Invalidate caches of other pieces that might be affected
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.pieces[row][col] is not None:
                    # Add logic to determine if this piece's moves could be affected
                    self.pieces[row][col].invalidate_cache()

    def simulate_move(self, start_row, start_col, end_row, end_col):
        # Create a new board with the same piece references
        temp_board = [[self.pieces[r][c] for c in range(self.COLS)] for r in range(self.ROWS)]

        # Move the piece on the temp_board
        temp_board[end_row][end_col] = temp_board[start_row][start_col]
        temp_board[start_row][start_col] = None

        # If the piece is a pawn and this is its first move, mark it as such
        if temp_board[end_row][end_col] and isinstance(temp_board[end_row][end_col], Pawn):
            temp_board[end_row][end_col].first_move = False

        return temp_board
    
    def is_king_in_check(self, board, color):
        king_position = None
        for row in range(self.ROWS):
            for col in range(self.COLS):
                piece = board[row][col]
                if piece and piece.piece_type == 'king' and piece.color == color:
                    king_position = (row, col)
                    break
            if king_position:
                break

        if king_position:
            opponent_color = 'white' if color == 'black' else 'black'
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    piece = board[row][col]
                    if piece and piece.color == opponent_color:
                        potential_moves = piece.calculate_potential_moves(board, self.last_move, self)
                        if king_position in potential_moves:
                            # Ensure the path to the king is not blocked for linear-moving pieces (rook, bishop, queen)
                            if not self.is_path_blocked(piece, king_position, board):
                                return True
        return False
    
    def is_path_blocked(self, piece, target_position, board):
        if isinstance(piece, Knight):  # Knights can jump, so no path check needed
            return False

        row_diff = target_position[0] - piece.row
        col_diff = target_position[1] - piece.col
        row_step = 1 if row_diff > 0 else -1 if row_diff < 0 else 0
        col_step = 1 if col_diff > 0 else -1 if col_diff < 0 else 0

        current_row, current_col = piece.row, piece.col
        while (current_row, current_col) != target_position:
            current_row += row_step
            current_col += col_step
            if (current_row, current_col) != target_position and board[current_row][current_col] is not None:
                return True  # Path is blocked

        return False  # Path is not blocked

    def is_square_under_attack(self, row, col, board):
        opponent_color = 'black' if self.turn == 'white' else 'white'
        for r in range(self.ROWS):
            for c in range(self.COLS):
                piece = board[r][c]
                if piece and piece.color == opponent_color:
                    if (row, col) in piece.calculate_potential_moves(board, self.last_move):
                        return True
        return False

    def create_pieces(self):
        # Create an 8x8 matrix of None
        pieces = np.full((self.ROWS, self.COLS), None, dtype=object)

        # Black pieces
        pieces[0][0], pieces[0][7] = Rook(0, 0, 'black', self.SQUARE_SIZE), Rook(0, 7, 'black', self.SQUARE_SIZE)
        pieces[0][1], pieces[0][6] = Knight(0, 1, 'black', self.SQUARE_SIZE), Knight(0, 6, 'black', self.SQUARE_SIZE)
        pieces[0][2], pieces[0][5] = Bishop(0, 2, 'black', self.SQUARE_SIZE), Bishop(0, 5, 'black', self.SQUARE_SIZE)
        pieces[0][3] = Queen(0, 3, 'black', self.SQUARE_SIZE)
        pieces[0][4] = King(0, 4, 'black', self.SQUARE_SIZE)
        for col in range(self.COLS):
            pieces[1][col] = Pawn(1, col, 'black', self.SQUARE_SIZE)

        # White pieces
        pieces[7][0], pieces[7][7] = Rook(7, 0, 'white', self.SQUARE_SIZE), Rook(7, 7, 'white', self.SQUARE_SIZE)
        pieces[7][1], pieces[7][6] = Knight(7, 1, 'white', self.SQUARE_SIZE), Knight(7, 6, 'white', self.SQUARE_SIZE)
        pieces[7][2], pieces[7][5] = Bishop(7, 2, 'white', self.SQUARE_SIZE), Bishop(7, 5, 'white', self.SQUARE_SIZE)
        pieces[7][3] = Queen(7, 3, 'white', self.SQUARE_SIZE)
        pieces[7][4] = King(7, 4, 'white', self.SQUARE_SIZE)
        for col in range(self.COLS):
            pieces[6][col] = Pawn(6, col, 'white', self.SQUARE_SIZE)

        return pieces

    def highlight_selected_piece(self):
        if self.selected_piece:
            # Original highlight for the selected piece
            highlight_color = (255, 255, 0)  # Yellow color
            highlight_thickness = 4  # Thickness of the highlight border
            x = self.selected_piece.col * self.SQUARE_SIZE
            y = self.selected_piece.row * self.SQUARE_SIZE
            pygame.draw.rect(self.window, highlight_color, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE), highlight_thickness)

            # New code to highlight possible moves
            move_highlight_color = (0, 255, 0)  # Green color
            for move in self.possible_moves:
                move_x = move[1] * self.SQUARE_SIZE
                move_y = move[0] * self.SQUARE_SIZE
                pygame.draw.circle(self.window, move_highlight_color, (move_x + self.SQUARE_SIZE // 2, move_y + self.SQUARE_SIZE // 2), self.SQUARE_SIZE // 10)

    def draw_turn_indicator(self):
        turn_text = f"{self.turn.capitalize()}'s Turn"
        text_surface = self.font.render(turn_text, True, (0, 0, 0))  # Black text
        self.window.blit(text_surface, (10, self.HEIGHT - 30))

    def draw_fps_counter(self, clock):
        fps = int(clock.get_fps())  # Get the current FPS
        fps_text = self.font.render(f'FPS: {fps}', True, (255, 0, 0))  # Red text
        self.window.blit(fps_text, (self.WIDTH - 100, 10))  # Position the FPS counter at the top-right corner

    def draw_board(self):
        light_green = (118, 150, 86)
        dark_green = (238, 238, 210)
        self.window.fill(light_green)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(self.window, dark_green, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                piece = self.pieces[row][col]
                if piece is not None:
                    piece.draw(self.window)

    def get_square_at_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        row, col = mouse_pos[1] // self.SQUARE_SIZE, mouse_pos[0] // self.SQUARE_SIZE
        return row, col
    
    def select_piece(self, row, col):
        piece = self.pieces[row][col]
        if self.selected_piece:
            # Move the piece and switch turns if the move is valid
            if self.move_piece(self.selected_piece.row, self.selected_piece.col, row, col):
                self.switch_turn()
                self.invalidate_relevant_caches(self.selected_piece.row, self.selected_piece.col, row, col)
            self.selected_piece = None
            self.possible_moves = []

        elif piece:
            print(f"Piece selected: {piece.__class__.__name__} at ({row}, {col})")  # Print statement
            if piece.color == self.turn:
                self.selected_piece = piece
                self.possible_moves = piece.get_potential_moves(self.pieces, self.last_move)
                print(self.possible_moves)
        
    def switch_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'

    def run(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = self.get_square_at_mouse()
                    self.select_piece(row, col)


            # Additional rendering to highlight selected piece and possible moves
            self.draw_board()
            self.draw_pieces()
            self.draw_turn_indicator()
            self.draw_fps_counter(clock)
            self.highlight_selected_piece()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()