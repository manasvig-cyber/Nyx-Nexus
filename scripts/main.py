"""
Password Cracker Challenge - Cybersecurity Mini-Game
For integration with existing pygame maze game
"""

import pygame
import random
import sys
import time
import webbrowser
import math

def run(screen):
    """
    Main game function - runs the password cracking challenge
    
    Args:
        screen: pygame surface from the main game
        
    Returns:
        bool: True if password cracked, False if failed or escaped
    """
    
    # Colors (Clean cyber theme)
    COLORS = {
        'bg': (10, 10, 20),              # Dark blue-black background
        'text': (255, 255, 255),         # Pure white text
        'text_dim': (200, 200, 255),      # Soft white-blue
        'text_red': (255, 80, 80),        # Bright red
        'text_blue': (100, 200, 255),     # Bright cyan
        'text_gold': (255, 215, 0),       # Gold
        'input_bg': (30, 30, 50),         # Dark blue-gray
        'input_border': (100, 200, 255),  # Cyan
        'panel_bg': (20, 20, 40),         # Dark blue panel
        'hint_panel_bg': (25, 25, 45),    # Slightly lighter panel
        'glow': (100, 200, 255, 30),      # Cyan glow
        'link_hover': (255, 215, 0),      # Gold hover
        'splash_bg': (10, 10, 20),        # Dark background
        'lightning_blue': (100, 200, 255), # Bright cyan
        'lightning_purple': (180, 130, 255), # Light purple
        'lightning_white': (255, 255, 255) # White
    }
    
    # Initialize fonts (using default pygame font) - Clean, sharp fonts
    try:
        font_large = pygame.font.Font(None, 56)
        font_medium = pygame.font.Font(None, 44)
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 26)
        font_micro = pygame.font.Font(None, 22)
    except:
        # Fallback if no font available
        font_large = pygame.font.Font(None, 56)
        font_medium = pygame.font.Font(None, 44)
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 26)
        font_micro = pygame.font.Font(None, 22)
    
    # Screen dimensions
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Load background image (Zeus storm background)
    try:
        bg_image = pygame.image.load("zeus background.jpg").convert()
        bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
    except:
        bg_image = None
    
    # 4 OSINT case scenarios based on provided challenges
    scenarios = [
        {
            'title': 'Friends Trip – Digital Footprints',
            'paragraph': "CASE FILE: FRIENDS TRIP\n\nA group of college friends went on a memorable trip and shared their memories online through a blog. At first glance, it looks like a simple travel blog post with photos and captions. However, the author unintentionally left behind small clues within the post.\n\nBlog to investigate:\nhttps://mk230513.blogspot.com/2024/10/its-trip-we-all-made-it.html\n\nThe author mentions a group name, a place visited, and a date. Investigators believe the password is hidden in the blog's details.",
            'password': 'GRS_2024_TRIP',
            'link': 'https://mk230513.blogspot.com/2024/10/its-trip-we-all-made-it.html',
            'link_text': 'https://mk230513.blogspot.com/2024/10/its-trip-we-all-made-it.html',
            'hint1': "Sometimes the title of a memory tells more than the photos themselves.",
            'hint2': "Look carefully at the year and the theme of the trip mentioned in the blog.",
            'hint3': "Combine the year with what the trip represents to the group."
        },
        {
            'title': 'Faith Leaves Footprints',
            'paragraph': "CASE FILE: FAITH LEAVES FOOTPRINTS\n\nDuring a digital investigation, analysts discovered an old personal blog belonging to a college student who often wrote reflections about life, faith, and personal experiences.\n\nBlog to investigate:\nhttps://muralikris05.blogspot.com/2022/12/2022-was-boon-would-say-22-will-be-my.html\n\nThe author describes how that year was a blessing and a turning point in life. Hidden within the context of the post are references to faith, belief, and personal inspiration.",
            'password': 'SHIVA_22_FAITH',
            'link': 'https://muralikris05.blogspot.com/2022/12/2022-was-boon-would-say-22-will-be-my.html',
            'link_text': 'https://muralikris05.blogspot.com/2022/12/2022-was-boon-would-say-22-will-be-my.html',
            'hint1': "The author mentions a name that appears in the blog title and reflects their faith.",
            'hint2': "Check the title of the blog post for the year details.",
            'hint3': "Faith is always the foundation of a strong belief. The Password is in capital letters and underscores, combining the name, year, and the concept of faith."
        },
        {
            'title': 'Commit Trace',
            'paragraph': "CASE FILE: COMMIT TRACE\n\nDuring a cyber investigation, analysts came across the GitHub profile of a developer suspected of leaving subtle clues across their online activity.\n\nGitHub profile to investigate:\nhttps://github.com/Krish-legend13\n\nOne specific day stands out: the latest day with the highest contribution activity. Investigators believe that this unusual spike is not random but was deliberately left as a hint.",
            'password': 'GITHUB_7_FEB',
            'link': 'https://github.com/Krish-legend13',
            'link_text': 'https://github.com/Krish-legend13',
            'hint1': "Sometimes the biggest clue is hidden in the brightest square.",
            'hint2': "The month of the highest contributions in 2026 is a key part of the password, along with the count of contributions on that day.",
            'hint3': "The password is in Capital Letters and underscores.The Website name is a part of the password as well"
        },
        {
            'title': 'Sixes Leave a Trace',
            'paragraph': "CASE FILE: SIXES LEAVE A TRACE\n\nDuring a cyber investigation into leaked credentials, analysts discovered that the suspect frequently used public social media discussions as hints for passwords.\n\nTweet to investigate:\nhttps://x.com/IPL2025Auction/status/2029800199221350435\n\nThe suspect left a clear pattern for constructing the password.",
            'password': 'SANJU_16_INDIA_WON',
            'link': 'https://x.com/IPL2025Auction/status/2029800199221350435',
            'link_text': 'https://x.com/IPL2025Auction/status/2029800199221350435',
            'hint1': "Focus on the player known for hitting the most sixes in that discussion.",
            'hint2': "Check whether the player's team won or lost the match.",
            'hint3': "Check the Comment section for the format of the password"
        }
    ]
    
    # Select random scenario
    scenario = random.choice(scenarios)
    
    # Game state
    user_input = ""
    attempts = 5
    message = ""
    message_color = COLORS['text']
    game_over = False
    success = False
    clock = pygame.time.Clock()
    running = True
    show_hint = False
    hint_timer = 0
    current_hint_index = 0
    hint_list = [scenario['hint1'], scenario['hint2'], scenario['hint3']]
    hint_locked = [False, False, False]
    displayed_hints = []
    
    # Link hover state
    link_hover = False
    link_rect = None
    
    # Stopwatch timer variables
    start_time = time.time()
    elapsed_seconds = 0
    
    # Panel dimensions - separate investigation and hint panels
    main_panel_rect = pygame.Rect(40, 70, screen_width - 80, 200)
    hint_panel_rect = pygame.Rect(40, 290, screen_width - 80, 160)
    
    # Input box dimensions - base dimensions for dynamic expansion
    base_input_width = 400
    min_input_width = 400
    max_input_width = int(screen_width * 0.8)
    input_padding = 30
    input_rect = pygame.Rect(screen_width//2 - base_input_width//2, screen_height - 160, base_input_width, 50)
    
    # Glow effect variables
    glow_offset = 0
    glow_direction = 1
    
    # Splash screen variables - FULLSCREEN
    show_splash = True
    game_started = False
    
    # Splash screen dimensions - FULL SCREEN
    splash_x = 0
    splash_y = 0
    splash_width = screen_width
    splash_height = screen_height
    
    # Create a content area for splash screen with margins
    content_margin = 100
    content_width = splash_width - (content_margin * 2)
    content_x = content_margin
    
    # Start button dimensions - will be calculated dynamically
    start_button_text = "START INVESTIGATION"
    start_button_font = font_medium
    start_text_surface = start_button_font.render(start_button_text, True, COLORS['text'])
    button_padding = 40
    start_button_width = start_text_surface.get_width() + button_padding
    start_button_height = 60
    start_button_x = splash_x + splash_width//2 - start_button_width//2
    start_button_y = splash_y + splash_height - 150
    
    # Animation variables
    scan_line_y = 0
    scan_direction = 1
    
    # Background lightning effect variables (subtle only)
    background_lightning_timer = 0
    background_flash_intensity = 0
    
    # Background micro animation variables
    particles = []
    for _ in range(20):
        particles.append({
            'x': random.randint(0, screen_width),
            'y': random.randint(0, screen_height),
            'speed': random.uniform(10, 30),
            'size': random.randint(1, 3),
            'alpha': random.randint(30, 100)
        })
    
    class LightningBolt:
        def __init__(self, x, y, target_y, intensity_multiplier=1.0):
            self.x = x
            self.y = y
            self.target_y = target_y
            self.points = [(x, y)]
            self.branches = []
            self.generate_path()
            self.life = 1.0
            self.max_life = 1.0
            self.width = random.randint(2, 4) * intensity_multiplier
            self.color = (200, 220, 255)
        
        def generate_path(self):
            x = self.x
            y = self.y
            segments = random.randint(10, 15)
            
            for i in range(segments):
                x += random.randint(-30, 30)
                y += (self.target_y - self.y) // segments + random.randint(-10, 10)
                self.points.append((x, y))
            
            self.points.append((self.x + random.randint(-50, 50), self.target_y))
            
            # Generate a few branches
            num_branches = random.randint(0, 2)
            for _ in range(num_branches):
                branch_point_idx = random.randint(len(self.points) // 3, len(self.points) - 2)
                branch_x, branch_y = self.points[branch_point_idx]
                branch = []
                branch_length = random.randint(2, 4)
                bx, by = branch_x, branch_y
                for j in range(branch_length):
                    bx += random.randint(-20, 20)
                    by += random.randint(10, 30)
                    branch.append((bx, by))
                self.branches.append(branch)
        
        def update(self, dt):
            self.life -= dt * 1.0
            return self.life > 0
        
        def draw(self, surface):
            if len(self.points) < 2:
                return
            
            alpha = int(self.life * 150)  # Lower alpha for subtle effect
            
            # Draw main bolt
            for i in range(len(self.points) - 1):
                pygame.draw.line(surface, (*self.color, alpha),
                               self.points[i], self.points[i + 1],
                               int(self.width))
            
            # Draw branches
            for branch in self.branches:
                for i in range(len(branch) - 1):
                    pygame.draw.line(surface, (*self.color, alpha),
                                   branch[i], branch[i + 1],
                                   int(self.width * 0.6))
    
    # Main game loop
    while running:
        dt = clock.tick(60) / 1000.0
        glow_offset += glow_direction * dt * 50
        if glow_offset > 20 or glow_offset < -20:
            glow_direction *= -1
        
        # Update scan line
        scan_line_y += scan_direction * 80 * dt
        if scan_line_y > screen_height or scan_line_y < 0:
            scan_direction *= -1
        
        if game_started and not game_over:
            elapsed_seconds = int(time.time() - start_time)
        
        # Update background lightning (subtle only)
        background_lightning_timer += dt
        if background_lightning_timer > random.uniform(3, 6):
            background_lightning_timer = 0
            background_flash_intensity = random.randint(3, 8)
            # Very occasional subtle lightning bolts in background
            if random.random() < 0.2:
                bolt = LightningBolt(
                    random.randint(0, screen_width),
                    0,
                    screen_height,
                    intensity_multiplier=0.5
                )
                # Note: lightning_bolts list not used, just background flash
        
        background_flash_intensity = max(0, background_flash_intensity - dt * 10)
        
        mouse_pos = pygame.mouse.get_pos()
        link_hover = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if game_started and not game_over:
                    if event.key == pygame.K_RETURN:
                        if user_input:
                            attempts -= 1
                            if user_input == scenario['password']:
                                message = "ACCESS GRANTED! Password cracked!"
                                message_color = COLORS['text']
                                game_over = True
                                success = True
                                # No lightning effects on success
                            else:
                                if attempts > 0:
                                    message = f"ACCESS DENIED! {attempts} attempts remaining."
                                    message_color = COLORS['text_red']
                                else:
                                    message = "ACCESS DENIED! No attempts remaining. Investigator failed."
                                    message_color = COLORS['text_red']
                                    game_over = True
                                    success = False
                            user_input = ""
                    
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                        # Update input box width
                        if user_input:
                            text_width = font_medium.size(user_input)[0] + input_padding * 2
                            new_width = max(min_input_width, min(text_width, max_input_width))
                            input_rect.width = new_width
                            input_rect.x = screen_width//2 - new_width//2
                        else:
                            input_rect.width = min_input_width
                            input_rect.x = screen_width//2 - min_input_width//2
                    
                    elif event.key == pygame.K_h and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if current_hint_index < 3 and not hint_locked[current_hint_index]:
                            displayed_hints.append(hint_list[current_hint_index])
                            hint_locked[current_hint_index] = True
                            if current_hint_index < 2:
                                current_hint_index += 1
                            show_hint = True
                            hint_timer = 5
                    
                    else:
                        if len(user_input) < 30 and event.unicode.isprintable():
                            user_input += event.unicode
                            # Update input box width
                            if user_input:
                                text_width = font_medium.size(user_input)[0] + input_padding * 2
                                new_width = max(min_input_width, min(text_width, max_input_width))
                                input_rect.width = new_width
                                input_rect.x = screen_width//2 - new_width//2
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if show_splash:
                        start_button_rect = pygame.Rect(start_button_x, start_button_y, start_button_width, start_button_height)
                        if start_button_rect.collidepoint(mouse_pos):
                            show_splash = False
                            game_started = True
                            start_time = time.time()
                    
                    elif game_started and not game_over:
                        if link_rect and link_rect.collidepoint(mouse_pos):
                            webbrowser.open(scenario['link'])
        
        if hint_timer > 0:
            hint_timer -= dt
            if hint_timer <= 0:
                show_hint = False
        
        # Clear screen with background image or color
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill(COLORS['bg'])
        
        # Draw background micro animations (floating particles)
        for particle in particles:
            particle['y'] += particle['speed'] * dt
            if particle['y'] > screen_height:
                particle['y'] = 0
                particle['x'] = random.randint(0, screen_width)
            
            particle_surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (*COLORS['text_blue'][:3], particle['alpha']), 
                             (particle['size'], particle['size']), particle['size'])
            screen.blit(particle_surf, (particle['x'], particle['y']))
        
        # Apply subtle background flash
        if background_flash_intensity > 0:
            flash_surf = pygame.Surface((screen_width, screen_height))
            flash_surf.set_alpha(int(background_flash_intensity))
            flash_surf.fill((220, 230, 255))
            screen.blit(flash_surf, (0, 0))
        
        if game_started:
            # Draw investigation panel with clean borders
            pygame.draw.rect(screen, COLORS['panel_bg'], main_panel_rect)
            pygame.draw.rect(screen, COLORS['text_blue'], main_panel_rect, 3)
            
            # Panel title
            title_text = font_medium.render(f"=== {scenario['title']} ===", True, COLORS['text'])
            screen.blit(title_text, (main_panel_rect.x + 20, main_panel_rect.y + 10))
            
            # Wrap paragraph text and handle link
            words = scenario['paragraph'].split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                if font_small.size(test_line)[0] < main_panel_rect.width - 40:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            y_offset = main_panel_rect.y + 45
            link_rect = None
            
            for line in lines:
                x_pos = main_panel_rect.x + 20
                if scenario['link_text'] in line:
                    parts = line.split(scenario['link_text'])
                    for i, part in enumerate(parts):
                        if part:
                            text_surface = font_small.render(part, True, COLORS['text_dim'])
                            screen.blit(text_surface, (x_pos, y_offset))
                            x_pos += text_surface.get_width()
                        
                        if i < len(parts) - 1:
                            link_color = COLORS['link_hover'] if link_rect and link_rect.collidepoint(mouse_pos) else COLORS['text_blue']
                            link_surface = font_small.render(scenario['link_text'], True, link_color)
                            link_rect = pygame.Rect(x_pos, y_offset, link_surface.get_width(), link_surface.get_height())
                            
                            pygame.draw.line(screen, link_color, 
                                            (x_pos, y_offset + link_surface.get_height() - 2),
                                            (x_pos + link_surface.get_width(), y_offset + link_surface.get_height() - 2), 2)
                            
                            screen.blit(link_surface, (x_pos, y_offset))
                            x_pos += link_surface.get_width()
                else:
                    text_surface = font_small.render(line, True, COLORS['text_dim'])
                    screen.blit(text_surface, (x_pos, y_offset))
                y_offset += 24
            
            # Draw hint panel with clean borders
            pygame.draw.rect(screen, COLORS['hint_panel_bg'], hint_panel_rect)
            pygame.draw.rect(screen, COLORS['text_blue'], hint_panel_rect, 2)
            
            hint_title = font_tiny.render("=== HINT SYSTEM (CTRL+H) ===", True, COLORS['text_blue'])
            screen.blit(hint_title, (hint_panel_rect.x + 20, hint_panel_rect.y + 5))
            
            hint_status = ""
            for i in range(3):
                if hint_locked[i]:
                    hint_status += f"[HINT {i+1} 🔓] "
                else:
                    hint_status += f"[HINT {i+1} 🔒] "
            hint_status_text = font_tiny.render(hint_status, True, COLORS['text_gold'])
            screen.blit(hint_status_text, (hint_panel_rect.x + 20, hint_panel_rect.y + 25))
            
            hint_y = hint_panel_rect.y + 50
            for i, hint in enumerate(displayed_hints):
                hint_words = hint.split()
                hint_lines = []
                hint_line = []
                for word in hint_words:
                    test_line = ' '.join(hint_line + [word])
                    if font_tiny.size(test_line)[0] < hint_panel_rect.width - 60:
                        hint_line.append(word)
                    else:
                        hint_lines.append(' '.join(hint_line))
                        hint_line = [word]
                if hint_line:
                    hint_lines.append(' '.join(hint_line))
                
                for line in hint_lines:
                    hint_display = font_tiny.render(f"HINT {i+1}: {line}", True, COLORS['text_blue'])
                    screen.blit(hint_display, (hint_panel_rect.x + 20, hint_y))
                    hint_y += 20
                
                hint_y += 8
            
            # Draw stopwatch timer
            minutes = elapsed_seconds // 60
            seconds = elapsed_seconds % 60
            timer_text = font_medium.render(f"⏱️ {minutes:02d}:{seconds:02d}", True, COLORS['text_blue'])
            screen.blit(timer_text, (20, 15))
            
            # Draw attempts counter
            attempts_color = COLORS['text'] if attempts > 1 else COLORS['text_red']
            attempts_text = font_medium.render(f"ATTEMPTS: {attempts}/5", True, attempts_color)
            screen.blit(attempts_text, (screen_width - 200, 15))
            
            # Draw password input box with dynamic width
            pygame.draw.rect(screen, COLORS['input_bg'], input_rect)
            pygame.draw.rect(screen, COLORS['input_border'], input_rect, 3)
            
            input_display = user_input if user_input else "ENTER PASSWORD..."
            input_color = COLORS['text'] if user_input else COLORS['text_dim']
            input_text = font_medium.render(input_display, True, input_color)
            
            if not game_over and pygame.time.get_ticks() % 1000 < 500:
                cursor = font_medium.render("_", True, COLORS['text'])
                cursor_x = input_rect.x + 10 + min(font_medium.size(user_input)[0], input_rect.width - 40)
                screen.blit(cursor, (cursor_x, input_rect.y + 10))
            
            text_y = input_rect.y + (input_rect.height - input_text.get_height()) // 2
            screen.blit(input_text, (input_rect.x + 10, text_y))
            
            label_text = font_small.render("PASSWORD CRACKER", True, COLORS['text_dim'])
            screen.blit(label_text, (input_rect.x, input_rect.y - 25))
            
            if message:
                msg_text = font_medium.render(message, True, message_color)
                msg_rect = msg_text.get_rect(center=(screen_width//2, screen_height - 100))
                screen.blit(msg_text, msg_rect)
            
            inst1 = font_tiny.render("Press ENTER to submit | BACKSPACE to delete | ESC to abort mission", True, COLORS['text_dim'])
            inst2 = font_tiny.render("Press CTRL+H for hints (hints accumulate and lock)", True, COLORS['text_dim'])
            screen.blit(inst1, (screen_width//2 - inst1.get_width()//2, screen_height - 55))
            screen.blit(inst2, (screen_width//2 - inst2.get_width()//2, screen_height - 40))
            
            if game_over:
                # Draw overlay
                overlay = pygame.Surface((screen_width, screen_height))
                overlay.set_alpha(120)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                
                final_minutes = elapsed_seconds // 60
                final_seconds = elapsed_seconds % 60
                
                if success:
                    result_text = font_large.render("PASSWORD CRACKED!", True, COLORS['text_gold'])
                    time_text = font_small.render(f"Investigation time: {final_minutes:02d}:{final_seconds:02d}", True, COLORS['text'])
                    sub_text = font_medium.render("Press ESC to return to main game", True, COLORS['text'])
                    
                    screen.blit(time_text, (screen_width//2 - time_text.get_width()//2, screen_height//2 - 60))
                    screen.blit(result_text, (screen_width//2 - result_text.get_width()//2, screen_height//2 - 30))
                    screen.blit(sub_text, (screen_width//2 - sub_text.get_width()//2, screen_height//2 + 20))
                    
                else:
                    result_text = font_large.render("MISSION FAILED!", True, COLORS['text_red'])
                    sub_text = font_medium.render("Press ESC to return to main game", True, COLORS['text_red'])
                    screen.blit(result_text, (screen_width//2 - result_text.get_width()//2, screen_height//2 - 30))
                    screen.blit(sub_text, (screen_width//2 - sub_text.get_width()//2, screen_height//2 + 20))
        
        if show_splash:
            # Full screen splash with clean design
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(220)
            overlay.fill((10, 10, 20))
            screen.blit(overlay, (0, 0))
            
            # Draw main panel with margins
            pygame.draw.rect(screen, (20, 20, 40), (content_x - 20, splash_y + 30, content_width + 40, splash_height - 120))
            pygame.draw.rect(screen, COLORS['text_blue'], (content_x - 20, splash_y + 30, content_width + 40, splash_height - 120), 4)
            
            splash_title = font_large.render("🔐 PASSWORD CRACKER CHALLENGE", True, COLORS['text'])
            screen.blit(splash_title, (splash_x + splash_width//2 - splash_title.get_width()//2, splash_y + 50))
            
            splash_subtitle = font_medium.render("OSINT Investigation Training Module", True, COLORS['text_blue'])
            screen.blit(splash_subtitle, (splash_x + splash_width//2 - splash_subtitle.get_width()//2, splash_y + 100))
            
            instructions = [
                "INVESTIGATION PROTOCOL:",
                "• You are an OSINT investigator tasked with cracking",
                "  a password from digital footprints.",
                "• The panel contains a case file with a clickable",
                "  link to online evidence (blog, GitHub, tweet).",
                "• Click the blue link to open in your browser.",
                "• Password is constructed from clues on the page.",
                "• You have 5 attempts to enter correct password.",
                "• Use CTRL+H to reveal 3 hints (lock permanently).",
                "• Stopwatch tracks your investigation time.",
                "• Good luck, Investigator!"
            ]
            
            y_offset = splash_y + 150
            line_spacing = 28
            
            for line in instructions:
                if line.startswith("•") or line.startswith("INVESTIGATION"):
                    text = font_small.render(line, True, COLORS['text'] if line.startswith("INVESTIGATION") else COLORS['text_gold'])
                    screen.blit(text, (content_x + 20, y_offset))
                else:
                    text = font_small.render(line, True, COLORS['text_dim'])
                    screen.blit(text, (content_x + 40, y_offset))
                
                y_offset += line_spacing
            
            start_button_rect = pygame.Rect(start_button_x, start_button_y, start_button_width, start_button_height)
            
            if start_button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, COLORS['text_blue'], start_button_rect)
                pygame.draw.rect(screen, COLORS['text'], start_button_rect, 3)
                start_text_color = (10, 10, 20)
            else:
                pygame.draw.rect(screen, (30, 30, 50), start_button_rect)
                pygame.draw.rect(screen, COLORS['text_blue'], start_button_rect, 3)
                start_text_color = COLORS['text']
            
            start_text = font_medium.render("START INVESTIGATION", True, start_text_color)
            screen.blit(start_text, (start_button_x + start_button_width//2 - start_text.get_width()//2, start_button_y + 15))
            
            footer_text = font_tiny.render("Click the button above to begin your mission", True, COLORS['text_dim'])
            screen.blit(footer_text, (splash_x + splash_width//2 - footer_text.get_width()//2, splash_y + splash_height - 70))
        
        pygame.display.flip()
    
    return success if success else False


# Test harness - ONLY FOR STANDALONE TESTING
if __name__ == "__main__":
    print("Starting Password Cracker Challenge in test mode...")
    print("(This is only for testing - the game will run in fullscreen mode)")
    
    pygame.init()
    display_info = pygame.display.Info()
    test_screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Password Cracker Challenge - FULLSCREEN MODE")
    
    result = run(test_screen)
    
    print(f"Game returned: {result}")
    pygame.time.wait(1000)
    pygame.quit()
    sys.exit()