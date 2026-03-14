import pygame
import random
import sys
import json
import os
from enum import Enum
import math
from datetime import datetime

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Get display info for fullscreen
display_info = pygame.display.Info()
DEFAULT_WIDTH = display_info.current_w
DEFAULT_HEIGHT = display_info.current_h

# Constants
MAZE_SIZE = 20  # Fixed 20x20 grid
TIME_LIMIT = 600  # 10 minutes = 600 seconds

# Game states
class GameState(Enum):
    PLAYING = 1
    WIN = 2
    LOSE = 3
    MENU = 4
    LEADERBOARD = 5

# Display modes
class DisplayMode(Enum):
    FULLSCREEN = 1
    FULL_BOX = 2
    HALF_BOX = 3

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        
    def draw(self, screen, x, y, cell_size, colors):
        if self.walls['top']:
            pygame.draw.line(screen, colors['wall'], (x, y), (x + cell_size, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, colors['wall'], (x + cell_size, y), (x + cell_size, y + cell_size), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, colors['wall'], (x + cell_size, y + cell_size), (x, y + cell_size), 2)
        if self.walls['left']:
            pygame.draw.line(screen, colors['wall'], (x, y + cell_size), (x, y), 2)

class Maze:
    def __init__(self):
        self.size = MAZE_SIZE  # Fixed at 20
        self.grid = [[Cell(x, y) for y in range(self.size)] for x in range(self.size)]
        self.start_pos = (0, 0)
        self.end_pos = (self.size - 1, self.size - 1)
        self.generate_maze()
        
    def generate_maze(self):
        """Generate a random maze using Depth-First Search"""
        # Reset all cells
        for x in range(self.size):
            for y in range(self.size):
                self.grid[x][y].visited = False
                self.grid[x][y].walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        
        # Random starting point for generation
        start_x = random.randint(0, self.size - 1)
        start_y = random.randint(0, self.size - 1)
        
        # Depth-first search maze generation
        stack = []
        current = self.grid[start_x][start_y]
        current.visited = True
        stack.append(current)
        
        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)
            
            if neighbors:
                next_cell, direction = random.choice(neighbors)
                self.remove_walls(current, next_cell, direction)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
        
        # Ensure start and end are accessible
        self.grid[0][0].walls['top'] = False
        self.grid[0][0].walls['left'] = False
        self.grid[self.size-1][self.size-1].walls['bottom'] = False
        self.grid[self.size-1][self.size-1].walls['right'] = False
        
        # Add some random loops for variety (30% chance)
        if random.random() < 0.3:
            self.add_loops()
    
    def add_loops(self):
        """Add some loops to make maze more interesting"""
        num_loops = random.randint(1, self.size // 4)
        for _ in range(num_loops):
            x = random.randint(1, self.size - 2)
            y = random.randint(1, self.size - 2)
            wall_to_remove = random.choice(['top', 'right', 'bottom', 'left'])
            
            if wall_to_remove == 'top' and y > 0:
                self.grid[x][y].walls['top'] = False
                self.grid[x][y-1].walls['bottom'] = False
            elif wall_to_remove == 'right' and x < self.size - 1:
                self.grid[x][y].walls['right'] = False
                self.grid[x+1][y].walls['left'] = False
            elif wall_to_remove == 'bottom' and y < self.size - 1:
                self.grid[x][y].walls['bottom'] = False
                self.grid[x][y+1].walls['top'] = False
            elif wall_to_remove == 'left' and x > 0:
                self.grid[x][y].walls['left'] = False
                self.grid[x-1][y].walls['right'] = False
    
    def get_unvisited_neighbors(self, cell):
        neighbors = []
        directions = [
            (0, -1, 'top', 'bottom'),
            (1, 0, 'right', 'left'),
            (0, 1, 'bottom', 'top'),
            (-1, 0, 'left', 'right')
        ]
        
        for dx, dy, wall, opposite in directions:
            new_x, new_y = cell.x + dx, cell.y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                if not self.grid[new_x][new_y].visited:
                    neighbors.append((self.grid[new_x][new_y], (wall, opposite)))
        
        return neighbors
    
    def remove_walls(self, current, next_cell, directions):
        wall, opposite = directions
        current.walls[wall] = False
        next_cell.walls[opposite] = False
    
    def is_wall(self, x, y, direction):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[x][y].walls[direction]
        return True
    
    def draw(self, screen, rect, colors):
        """Draw maze within given rectangle"""
        cell_size = min(rect.width // self.size, rect.height // self.size)
        maze_width = cell_size * self.size
        maze_height = cell_size * self.size
        
        # Center the maze in the rectangle
        offset_x = rect.x + (rect.width - maze_width) // 2
        offset_y = rect.y + (rect.height - maze_height) // 2
        
        # Draw maze background
        maze_rect = pygame.Rect(offset_x, offset_y, maze_width, maze_height)
        pygame.draw.rect(screen, colors['maze_bg'], maze_rect)
        
        # Draw cells
        for x in range(self.size):
            for y in range(self.size):
                cell_x = offset_x + x * cell_size
                cell_y = offset_y + y * cell_size
                self.grid[x][y].draw(screen, cell_x, cell_y, cell_size, colors)
        
        # Draw start and end markers
        start_x = offset_x + self.start_pos[0] * cell_size + cell_size // 2
        start_y = offset_y + self.start_pos[1] * cell_size + cell_size // 2
        end_x = offset_x + self.end_pos[0] * cell_size + cell_size // 2
        end_y = offset_y + self.end_pos[1] * cell_size + cell_size // 2
        
        pygame.draw.circle(screen, colors['start'], (start_x, start_y), cell_size // 3)
        pygame.draw.circle(screen, colors['end'], (end_x, end_y), cell_size // 3)
        
        return cell_size, offset_x, offset_y

class Player:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = 0
        self.pixel_y = 0
        self.target_x = x
        self.target_y = y
        self.speed = 5
        self.moves = 0
        
    def move(self, dx, dy, maze):
        new_x = self.target_x + dx
        new_y = self.target_y + dy
        
        # Check if move is valid
        if 0 <= new_x < maze.size and 0 <= new_y < maze.size:
            # Check walls
            if dx > 0 and not maze.is_wall(self.target_x, self.target_y, 'right'):
                self.target_x = new_x
                self.moves += 1
                return True
            elif dx < 0 and not maze.is_wall(self.target_x, self.target_y, 'left'):
                self.target_x = new_x
                self.moves += 1
                return True
            elif dy > 0 and not maze.is_wall(self.target_x, self.target_y, 'bottom'):
                self.target_y = new_y
                self.moves += 1
                return True
            elif dy < 0 and not maze.is_wall(self.target_x, self.target_y, 'top'):
                self.target_y = new_y
                self.moves += 1
                return True
        return False
    
    def update(self, cell_size, offset_x, offset_y):
        # Update pixel position based on grid target
        target_pixel_x = offset_x + self.target_x * cell_size + cell_size // 2
        target_pixel_y = offset_y + self.target_y * cell_size + cell_size // 2
        
        # Smooth movement
        dx = target_pixel_x - self.pixel_x
        dy = target_pixel_y - self.pixel_y
        
        if abs(dx) > self.speed:
            self.pixel_x += self.speed if dx > 0 else -self.speed
        else:
            self.pixel_x = target_pixel_x
            
        if abs(dy) > self.speed:
            self.pixel_y += self.speed if dy > 0 else -self.speed
        else:
            self.pixel_y = target_pixel_y
    
    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (int(self.pixel_x), int(self.pixel_y)), 12)

class Leaderboard:
    def __init__(self, filename="leaderboard.json"):
        self.filename = filename
        self.scores = []
        self.load()
    
    def load(self):
        """Load scores from file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.scores = json.load(f)
        except:
            self.scores = []
    
    def save(self):
        """Save scores to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except:
            pass
    
    def add_score(self, name, time_seconds, moves):
        """Add a new score to leaderboard"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        score = {
            'name': name[:20],  # Limit name length
            'time': time_seconds,
            'time_str': f"{time_seconds//60:02d}:{time_seconds%60:02d}",
            'moves': moves,
            'date': timestamp
        }
        self.scores.append(score)
        
        # Sort by time (ascending) then by moves (ascending)
        self.scores.sort(key=lambda x: (x['time'], x['moves']))
        
        # Keep only top 10
        self.scores = self.scores[:10]
        self.save()
    
    def get_top_scores(self, limit=10):
        """Get top scores"""
        return self.scores[:limit]

class Game:
    def __init__(self):
        # Display settings
        self.display_mode = DisplayMode.FULL_BOX
        self.screen = None
        self.set_display_mode()
        
        pygame.display.set_caption("Maze Game - 20x20 Random Maze")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 72)
        
        # Color scheme
        self.colors = {
            'background': (10, 10, 20),
            'maze_bg': (30, 30, 40),
            'wall': (180, 180, 200),
            'player': (100, 200, 255),
            'start': (100, 255, 100),
            'end': (255, 100, 100),
            'text': (255, 255, 255),
            'text_bg': (40, 40, 50, 200),
            'hud_bg': (20, 20, 30, 180),
            'warning': (255, 255, 100),
            'danger': (255, 100, 100),
            'gold': (255, 215, 0),
            'silver': (192, 192, 192),
            'bronze': (205, 127, 50)
        }
        
        # Game variables
        self.state = GameState.MENU
        self.player_name = "Player"
        self.name_input = ""
        self.show_name_input = False
        
        # Generate first maze (always 20x20)
        self.maze = Maze()
        self.player = Player(0, 0)
        
        # Timer (10 minutes = 600 seconds)
        self.time_limit = TIME_LIMIT
        self.time_remaining = self.time_limit
        self.last_time_update = pygame.time.get_ticks()
        
        # Leaderboard
        self.leaderboard = Leaderboard()
        
        # Camera/View settings
        self.maze_rect = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
        self.cell_size = 0
        self.offset_x = 0
        self.offset_y = 0
        
        # Sounds
        self.setup_sounds()
        
    def set_display_mode(self):
        """Set the display mode based on selection"""
        if self.display_mode == DisplayMode.FULLSCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif self.display_mode == DisplayMode.FULL_BOX:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:  # HALF_BOX
            width = DEFAULT_WIDTH // 2
            height = DEFAULT_HEIGHT // 2
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    
    def toggle_display_mode(self):
        """Cycle through display modes"""
        modes = list(DisplayMode)
        current_index = modes.index(self.display_mode)
        self.display_mode = modes[(current_index + 1) % len(modes)]
        self.set_display_mode()
        
    def setup_sounds(self):
        try:
            self.bg_music = pygame.mixer.Sound("background.wav") if os.path.exists("background.wav") else None
            self.win_sound = pygame.mixer.Sound("win.wav") if os.path.exists("win.wav") else None
            self.lose_sound = pygame.mixer.Sound("lose.wav") if os.path.exists("lose.wav") else None
            self.move_sound = pygame.mixer.Sound("move.wav") if os.path.exists("move.wav") else None
        except:
            self.bg_music = None
            self.win_sound = None
            self.lose_sound = None
            self.move_sound = None
            print("Sound files not found. Running without sound effects.")
        
        if self.bg_music:
            self.bg_music.play(-1)
    
    def new_random_game(self):
        """Start a new game with a random 20x20 maze"""
        # Generate new 20x20 maze
        self.maze = Maze()
        
        # Reset player
        self.player = Player(0, 0)
        self.player.moves = 0
        
        # Reset timer to 10 minutes
        self.time_remaining = self.time_limit
        self.last_time_update = pygame.time.get_ticks()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_display_mode()
                
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.new_random_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_l:
                        self.state = GameState.LEADERBOARD
                    elif event.key == pygame.K_ESCAPE:
                        return False
                
                elif self.state == GameState.PLAYING:
                    moved = False
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        moved = self.player.move(0, -1, self.maze)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        moved = self.player.move(0, 1, self.maze)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        moved = self.player.move(-1, 0, self.maze)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        moved = self.player.move(1, 0, self.maze)
                    
                    if moved and self.move_sound:
                        self.move_sound.play()
                
                elif self.state == GameState.LEADERBOARD:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                
                elif self.state == GameState.WIN:
                    if self.show_name_input:
                        if event.key == pygame.K_RETURN and self.name_input:
                            self.player_name = self.name_input
                            # Save to leaderboard
                            time_taken = self.time_limit - self.time_remaining
                            self.leaderboard.add_score(
                                self.player_name, 
                                time_taken, 
                                self.player.moves
                            )
                            self.show_name_input = False
                            self.name_input = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.name_input = self.name_input[:-1]
                        else:
                            # Add character to name (limit length)
                            if len(self.name_input) < 20 and event.unicode.isprintable():
                                self.name_input += event.unicode
                    else:
                        if event.key == pygame.K_SPACE:
                            self.state = GameState.MENU
                        elif event.key == pygame.K_r:
                            self.new_random_game()
                            self.state = GameState.PLAYING
                        elif event.key == pygame.K_ESCAPE:
                            return False
                
                elif self.state == GameState.LOSE:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.MENU
                    elif event.key == pygame.K_r:
                        self.new_random_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        return False
            
            elif event.type == pygame.VIDEORESIZE:
                if self.display_mode == DisplayMode.HALF_BOX:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        return True
    
    def update(self):
        if self.state == GameState.PLAYING:
            # Update timer
            current_time = pygame.time.get_ticks()
            if current_time - self.last_time_update >= 1000:
                self.time_remaining -= 1
                self.last_time_update = current_time
                
                if self.time_remaining <= 0:
                    self.time_remaining = 0
                    self.state = GameState.LOSE
                    if self.lose_sound:
                        self.lose_sound.play()
            
            # Update player position
            self.player.update(self.cell_size, self.offset_x, self.offset_y)
            
            # Check for win condition
            if (self.player.target_x == self.maze.end_pos[0] and 
                self.player.target_y == self.maze.end_pos[1]):
                self.state = GameState.WIN
                self.show_name_input = True
                if self.win_sound:
                    self.win_sound.play()
    
    def draw_hud(self, screen_width, screen_height):
        """Draw HUD elements"""
        # Create HUD background at the top
        hud_height = 80
        hud_surface = pygame.Surface((screen_width, hud_height), pygame.SRCALPHA)
        hud_surface.fill(self.colors['hud_bg'])
        self.screen.blit(hud_surface, (0, 0))
        
        # Timer (left side)
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        timer_text = f"⏱️ {minutes:02d}:{seconds:02d} / 10:00"
        
        # Choose color based on time remaining
        if self.time_remaining < 60:
            timer_color = self.colors['danger']
        elif self.time_remaining < 120:
            timer_color = self.colors['warning']
        else:
            timer_color = self.colors['text']
        
        timer_surface = self.font.render(timer_text, True, timer_color)
        self.screen.blit(timer_surface, (20, 20))
        
        # Maze info (center)
        info_text = f"Maze: 20x20 (Random)"
        info_surface = self.font.render(info_text, True, self.colors['text'])
        info_rect = info_surface.get_rect(center=(screen_width // 2, 25))
        self.screen.blit(info_surface, info_rect)
        
        # Controls hint (right side)
        controls = "F11: View | ESC: Menu"
        controls_surface = self.small_font.render(controls, True, self.colors['text'])
        controls_rect = controls_surface.get_rect(topright=(screen_width - 20, 25))
        self.screen.blit(controls_surface, controls_rect)
        
        # Move counter
        moves_text = f"Moves: {self.player.moves}"
        moves_surface = self.small_font.render(moves_text, True, self.colors['text'])
        moves_rect = moves_surface.get_rect(topright=(screen_width - 20, 55))
        self.screen.blit(moves_surface, moves_rect)
        
        return hud_height
    
    def draw_menu(self):
        self.screen.fill(self.colors['background'])
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Title with animation
        title_y = screen_height // 4 + math.sin(pygame.time.get_ticks() * 0.002) * 10
        
        title_shadow = self.big_font.render("MAZE GAME", True, (50, 50, 70))
        title = self.big_font.render("MAZE GAME", True, self.colors['text'])
        
        shadow_rect = title_shadow.get_rect(center=(screen_width//2 + 4, title_y + 4))
        title_rect = title.get_rect(center=(screen_width//2, title_y))
        
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font.render("20x20 Random Maze - 10 Minutes", True, self.colors['gold'])
        subtitle_rect = subtitle.get_rect(center=(screen_width//2, title_y + 60))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        menu_items = [
            ("Press SPACE to Start", "New random maze every time"),
            ("Press L for Leaderboard", "View top scores"),
            ("Press F11 to Toggle View", f"Mode: {self.display_mode.name}"),
            ("Press ESC to Quit", "")
        ]
        
        y_offset = screen_height // 2 + 50
        for text, subtext in menu_items:
            # Main option
            text_surface = self.font.render(text, True, self.colors['text'])
            text_rect = text_surface.get_rect(center=(screen_width//2, y_offset))
            
            # Draw highlight
            highlight_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, self.colors['hud_bg'], highlight_rect, border_radius=5)
            
            self.screen.blit(text_surface, text_rect)
            
            # Subtext
            if subtext:
                sub_surface = self.small_font.render(subtext, True, self.colors['wall'])
                sub_rect = sub_surface.get_rect(center=(screen_width//2, y_offset + 25))
                self.screen.blit(sub_surface, sub_rect)
            
            y_offset += 70
        
        # Stats
        total_games = len(self.leaderboard.scores)
        stats_text = f"Total Records: {total_games}"
        stats_surface = self.small_font.render(stats_text, True, self.colors['text'])
        stats_rect = stats_surface.get_rect(bottomright=(screen_width - 20, screen_height - 20))
        self.screen.blit(stats_surface, stats_rect)
    
    def draw_leaderboard(self):
        self.screen.fill(self.colors['background'])
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Title
        title = self.big_font.render("LEADERBOARD", True, self.colors['gold'])
        title_rect = title.get_rect(center=(screen_width//2, 80))
        self.screen.blit(title, title_rect)
        
        # Subtitle - fixed maze size and time
        subtitle = self.font.render("20x20 Maze - 10 Minute Limit", True, self.colors['text'])
        subtitle_rect = subtitle.get_rect(center=(screen_width//2, 130))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Get top scores
        top_scores = self.leaderboard.get_top_scores()
        
        if not top_scores:
            # No scores yet
            no_scores = self.font.render("No scores yet. Be the first!", True, self.colors['text'])
            no_rect = no_scores.get_rect(center=(screen_width//2, screen_height//2))
            self.screen.blit(no_scores, no_rect)
        else:
            # Draw headers
            headers = ["Rank", "Name", "Time", "Moves", "Date"]
            header_x_positions = [150, 300, 450, 550, 650]
            
            for i, header in enumerate(headers):
                header_surf = self.small_font.render(header, True, self.colors['gold'])
                self.screen.blit(header_surf, (header_x_positions[i], 180))
            
            # Draw scores
            y_offset = 220
            for i, score in enumerate(top_scores):
                # Rank with medal colors
                rank = i + 1
                if rank == 1:
                    rank_color = self.colors['gold']
                elif rank == 2:
                    rank_color = self.colors['silver']
                elif rank == 3:
                    rank_color = self.colors['bronze']
                else:
                    rank_color = self.colors['text']
                
                # Row background for alternating rows
                if i % 2 == 0:
                    row_bg = pygame.Rect(100, y_offset - 5, screen_width - 200, 30)
                    pygame.draw.rect(self.screen, (30, 30, 40), row_bg, border_radius=3)
                
                # Rank
                rank_surf = self.font.render(f"#{rank}", True, rank_color)
                self.screen.blit(rank_surf, (150, y_offset))
                
                # Name
                name_surf = self.small_font.render(score['name'], True, self.colors['text'])
                self.screen.blit(name_surf, (300, y_offset))
                
                # Time
                time_surf = self.small_font.render(score['time_str'], True, self.colors['text'])
                self.screen.blit(time_surf, (450, y_offset))
                
                # Moves
                moves_surf = self.small_font.render(str(score['moves']), True, self.colors['text'])
                self.screen.blit(moves_surf, (550, y_offset))
                
                # Date (show month-day)
                date_surf = self.small_font.render(score['date'][5:10], True, self.colors['text'])
                self.screen.blit(date_surf, (650, y_offset))
                
                y_offset += 35
        
        # Back instruction
        back_text = "Press SPACE or ESC to return to menu"
        back_surf = self.small_font.render(back_text, True, self.colors['text'])
        back_rect = back_surf.get_rect(center=(screen_width//2, screen_height - 50))
        self.screen.blit(back_surf, back_rect)
    
    def draw_game(self):
        self.screen.fill(self.colors['background'])
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Draw HUD and get available space for maze
        hud_height = self.draw_hud(screen_width, screen_height)
        
        # Calculate maze area (below HUD)
        maze_area = pygame.Rect(0, hud_height, screen_width, screen_height - hud_height)
        
        # Draw maze and get cell size and offsets
        self.cell_size, self.offset_x, self.offset_y = self.maze.draw(self.screen, maze_area, self.colors)
        
        # Draw player
        self.player.draw(self.screen, self.colors['player'])
        
        # Draw minimap
        self.draw_minimap()
    
    def draw_minimap(self):
        """Draw a small minimap in the corner"""
        minimap_size = 150
        margin = 20
        screen_width = self.screen.get_width()
        
        # Create minimap surface
        minimap = pygame.Surface((minimap_size, minimap_size))
        minimap.fill((20, 20, 30))
        
        # Draw simplified maze on minimap
        cell_size = minimap_size // self.maze.size
        
        for x in range(self.maze.size):
            for y in range(self.maze.size):
                # Draw walls
                if self.maze.grid[x][y].walls['top']:
                    pygame.draw.line(minimap, (100, 100, 120), 
                                   (x * cell_size, y * cell_size), 
                                   ((x + 1) * cell_size, y * cell_size), 1)
                if self.maze.grid[x][y].walls['right']:
                    pygame.draw.line(minimap, (100, 100, 120),
                                   ((x + 1) * cell_size, y * cell_size),
                                   ((x + 1) * cell_size, (y + 1) * cell_size), 1)
                if self.maze.grid[x][y].walls['bottom']:
                    pygame.draw.line(minimap, (100, 100, 120),
                                   ((x + 1) * cell_size, (y + 1) * cell_size),
                                   (x * cell_size, (y + 1) * cell_size), 1)
                if self.maze.grid[x][y].walls['left']:
                    pygame.draw.line(minimap, (100, 100, 120),
                                   (x * cell_size, (y + 1) * cell_size),
                                   (x * cell_size, y * cell_size), 1)
        
        # Draw player position on minimap
        player_x = self.player.target_x * cell_size + cell_size // 2
        player_y = self.player.target_y * cell_size + cell_size // 2
        pygame.draw.circle(minimap, self.colors['player'], (player_x, player_y), 4)
        
        # Draw start and end
        start_x = self.maze.start_pos[0] * cell_size + cell_size // 2
        start_y = self.maze.start_pos[1] * cell_size + cell_size // 2
        end_x = self.maze.end_pos[0] * cell_size + cell_size // 2
        end_y = self.maze.end_pos[1] * cell_size + cell_size // 2
        
        pygame.draw.circle(minimap, self.colors['start'], (start_x, start_y), 3)
        pygame.draw.circle(minimap, self.colors['end'], (end_x, end_y), 3)
        
        # Draw minimap on screen
        self.screen.blit(minimap, (screen_width - minimap_size - margin, margin + 100))
        
        # Draw minimap border
        pygame.draw.rect(self.screen, self.colors['wall'], 
                        (screen_width - minimap_size - margin - 2, margin + 98, 
                         minimap_size + 4, minimap_size + 4), 2)
        
        # Add minimap label
        label = self.small_font.render("MINIMAP", True, self.colors['text'])
        label_rect = label.get_rect(center=(screen_width - minimap_size//2 - margin, margin + 80))
        self.screen.blit(label, label_rect)
    
    def draw_win_screen(self):
        self.screen.fill(self.colors['background'])
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Victory text with animation
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 20
        win_text = self.big_font.render("VICTORY!", True, self.colors['start'])
        win_rect = win_text.get_rect(center=(screen_width//2, screen_height//4))
        
        # Draw pulsing effect
        pulse_rect = win_rect.inflate(pulse, pulse)
        pygame.draw.rect(self.screen, self.colors['start'], pulse_rect, 3, border_radius=10)
        
        self.screen.blit(win_text, win_rect)
        
        # Stats
        time_taken = self.time_limit - self.time_remaining
        minutes = time_taken // 60
        seconds = time_taken % 60
        
        stats = [
            f"Time: {minutes:02d}:{seconds:02d} / 10:00",
            f"Moves: {self.player.moves}",
            f"Maze: 20x20 (Random)"
        ]
        
        y_offset = screen_height // 2 - 50
        for stat in stats:
            stat_surface = self.font.render(stat, True, self.colors['text'])
            stat_rect = stat_surface.get_rect(center=(screen_width//2, y_offset))
            
            # Draw background
            bg_rect = stat_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, self.colors['hud_bg'], bg_rect, border_radius=5)
            
            self.screen.blit(stat_surface, stat_rect)
            y_offset += 50
        
        # Name input for leaderboard
        if self.show_name_input:
            name_prompt = self.font.render("Enter your name for leaderboard:", True, self.colors['gold'])
            prompt_rect = name_prompt.get_rect(center=(screen_width//2, y_offset))
            self.screen.blit(name_prompt, prompt_rect)
            y_offset += 40
            
            # Draw input box
            input_box = pygame.Rect(screen_width//2 - 100, y_offset - 15, 200, 40)
            pygame.draw.rect(self.screen, self.colors['text_bg'], input_box, border_radius=5)
            pygame.draw.rect(self.screen, self.colors['gold'], input_box, 2, border_radius=5)
            
            name_display = self.name_input if self.name_input else "_"
            name_surface = self.font.render(name_display, True, self.colors['text'])
            name_rect = name_surface.get_rect(center=input_box.center)
            self.screen.blit(name_surface, name_rect)
            
            y_offset += 60
            
            # Instruction
            inst = self.small_font.render("Press ENTER to save", True, self.colors['text'])
            inst_rect = inst.get_rect(center=(screen_width//2, y_offset))
            self.screen.blit(inst, inst_rect)
        else:
            # Options
            options = [
                "Press SPACE for Menu",
                "Press R to Play Again (New Random Maze)",
                "Press ESC to Quit"
            ]
            
            y_offset = screen_height - 120
            for option in options:
                opt_surface = self.small_font.render(option, True, self.colors['text'])
                opt_rect = opt_surface.get_rect(center=(screen_width//2, y_offset))
                self.screen.blit(opt_surface, opt_rect)
                y_offset += 25
    
    def draw_lose_screen(self):
        self.screen.fill(self.colors['background'])
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Game Over text
        lose_text = self.big_font.render("GAME OVER", True, self.colors['danger'])
        lose_rect = lose_text.get_rect(center=(screen_width//2, screen_height//3))
        self.screen.blit(lose_text, lose_rect)
        
        # Reason
        if self.time_remaining <= 0:
            reason = "Time's Up! (10 minute limit)"
        else:
            reason = "Better Luck Next Time!"
        
        reason_surface = self.font.render(reason, True, self.colors['text'])
        reason_rect = reason_surface.get_rect(center=(screen_width//2, screen_height//2))
        self.screen.blit(reason_surface, reason_rect)
        
        # Stats
        stats = [
            f"Time Remaining: {self.time_remaining//60:02d}:{self.time_remaining%60:02d} / 10:00",
            f"Moves Made: {self.player.moves}",
            f"Maze: 20x20 (Random)"
        ]
        
        y_offset = screen_height//2 + 50
        for stat in stats:
            stat_surface = self.small_font.render(stat, True, self.colors['text'])
            stat_rect = stat_surface.get_rect(center=(screen_width//2, y_offset))
            self.screen.blit(stat_surface, stat_rect)
            y_offset += 30
        
        # Options
        options = [
            "Press SPACE for Menu",
            "Press R to Try Again (New Random Maze)",
            "Press ESC to Quit"
        ]
        
        y_offset = screen_height - 120
        for option in options:
            opt_surface = self.small_font.render(option, True, self.colors['text'])
            opt_rect = opt_surface.get_rect(center=(screen_width//2, y_offset))
            self.screen.blit(opt_surface, opt_rect)
            y_offset += 25
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_game()
            elif self.state == GameState.LEADERBOARD:
                self.draw_leaderboard()
            elif self.state == GameState.WIN:
                self.draw_win_screen()
            elif self.state == GameState.LOSE:
                self.draw_lose_screen()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Main execution
if __name__ == "__main__":
    game = Game()
    game.run()