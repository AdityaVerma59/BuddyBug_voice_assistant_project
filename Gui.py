import pygame
import sys
import math
import time
import threading
import queue
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Screen dimensions - will be set to fullscreen
WIDTH, HEIGHT = 0, 0  # Will be set based on display

# Colors
DARK_BG = (10, 15, 30)
NEON_BLUE = (0, 195, 255)
NEON_PURPLE = (180, 0, 255)
NEON_GREEN = (0, 255, 180)
NEON_RED = (255, 50, 50)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (40, 40, 50)
USER_TEXT_COLOR = (220, 220, 240)  # Light blue-gray for user messages
AI_TEXT_COLOR = (0, 230, 230)     # Cyan for AI responses

# Set up display for fullscreen
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("BuddyBug AI Assistant")

# Load high-quality fonts with bold style
try:
    # Try to load premium fonts - replace with your preferred font files
    title_font = pygame.font.Font("fonts/Roboto-Bold.ttf", int(HEIGHT * 0.07))
    main_font = pygame.font.Font("fonts/Roboto-Bold.ttf", int(HEIGHT * 0.032))  # Bold
    small_font = pygame.font.Font("fonts/Roboto-Bold.ttf", int(HEIGHT * 0.026))  # Bold
    conversation_font = pygame.font.Font("fonts/Roboto-Bold.ttf", int(HEIGHT * 0.026))  # Bold, smaller font size
except:
    # Fallback to system fonts if custom fonts aren't available
    print("Custom fonts not found. Using system fonts.")
    title_font = pygame.font.SysFont("arial", int(HEIGHT * 0.07), bold=True)
    main_font = pygame.font.SysFont("arial", int(HEIGHT * 0.032), bold=True)  # Bold
    small_font = pygame.font.SysFont("arial", int(HEIGHT * 0.026), bold=True)  # Bold
    conversation_font = pygame.font.SysFont("arial", int(HEIGHT * 0.026), bold=True)  # Bold, smaller font size

# Animation variables
pulse_radius = 0
pulse_growing = True
last_pulse_time = time.time()
wave_offset = 0

# Assistant state
listening = False
processing = False
conversation = []  # List to store conversation history
scroll_offset = 0  # For scrolling the conversation
last_command_time = 0
command_queue = queue.Queue()
shutdown = False
conversation_height = 0  # Track total height of conversation
session_start_time = time.time()  # Track session start time
app_loaded = False  # Track if app has finished loading

# Text input variables
text_input = ""
input_active = False
input_rect = pygame.Rect(WIDTH * 0.02, HEIGHT * 0.9, WIDTH * 0.7 - WIDTH * 0.08, HEIGHT * 0.06)
send_button_rect = pygame.Rect(WIDTH * 0.7 - WIDTH * 0.05, HEIGHT * 0.9, WIDTH * 0.04, HEIGHT * 0.06)

# Background image
try:
    # Try to load a background image - replace 'background.jpg' with your image file
    background_image = pygame.image.load('background.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    has_background_image = True
    print("Background image loaded successfully")
except:
    # Fallback to a solid color if image loading fails
    has_background_image = False
    print("Background image not found. Using solid color background.")
    # Create a simple gradient background programmatically
    background_surface = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        color_value = 10 + int(5 * (y / HEIGHT))
        pygame.draw.line(background_surface, (color_value, color_value + 5, color_value + 10), (0, y), (WIDTH, y))

# Import your existing modules
modules_available = False
def load_modules():
    global modules_available, takeCommand, process, say
    try:
        from Head.Ear import takeCommand
        from Brain.processor import process
        from Head.Mouth import say
        modules_available = True
        print("All modules loaded successfully")
    except ImportError as e:
        print(f"Some modules could not be imported: {e}. Running in demo mode.")
        modules_available = False
        
        # Demo functions for testing the GUI
        def takeCommand(duration=7):
            # In demo mode, simulate listening with a timer
            time.sleep(2)  # Simulate listening time
            return "What is your name?"  # Return a simple command for demo
        
        def process(query):
            # Simulate processing
            time.sleep(1)  # Simulate processing time
            
            responses = {
                "what is your name": "You can call me BuddyBug, your personal assistant.",
                "hello": "Hello there! How can I assist you today?",
                "time": f"The current time is {time.strftime('%H:%M')}",
                "weather": "I'm checking the weather for your location... It looks sunny today!",
                "joke": "Why don't scientists trust atoms? Because they make up everything!",
                "": "I didn't catch that. Could you please repeat?"
            }
            
            query_lower = query.lower()
            for key in responses:
                if key in query_lower and key != "":
                    return responses[key]
            
            return "I'm processing your request. This might take a moment..."
        
        def say(text):
            # Simulate text-to-speech
            print(f"Assistant says: {text}")

# Add initial greeting to conversation
conversation.append(("BuddyBug", "Your personal assistant is ready, at your service, sir"))

# Format time function
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Format date function
def format_date():
    """Return formatted current date"""
    return time.strftime("%Y-%m-%d")

# Function to handle voice command processing
def command_processor():
    global listening, processing, conversation, scroll_offset, shutdown, conversation_height
    
    while not shutdown:
        try:
            # Wait for a command to process
            command_data = command_queue.get(timeout=0.1)
            if command_data == "SHUTDOWN":
                break
                
            if command_data.startswith("TEXT_INPUT:"):
                # Handle text input
                query = command_data[11:]  # Remove "TEXT_INPUT:" prefix
                
                # Add user message to conversation
                conversation.append(("You", query))
                
                query_lower = query.lower().strip()
                
                # Quit condition
                if query_lower in ["quit", "exit", "stop", "fuck off", "ok, fuck off"]:
                    say("Goodbye boss, see you again.")
                    shutdown = True
                    pygame.quit()
                    sys.exit()
                
                # Otherwise process normally
                processing = True
                response = process(query)
                processing = False
                
                # Add AI response to conversation
                conversation.append(("BuddyBug", response))
                say(response)
                
                # Auto-scroll to the bottom of the conversation
                scroll_offset = 0
                
            else:
                # Voice command processing (existing code)
                listening = True
                query = takeCommand(duration=7)
                listening = False
                
                if query:
                    # Add user message to conversation
                    conversation.append(("You", query))
                    
                    query_lower = query.lower().strip()
                    
                    # Quit condition
                    if query_lower in ["quit", "exit", "stop", "fuck off", "ok, fuck off"]:
                        say("Goodbye boss, see you again.")
                        shutdown = True
                        pygame.quit()
                        sys.exit()
                    
                    # Otherwise process normally
                    processing = True
                    response = process(query)
                    processing = False
                    
                    # Add AI response to conversation
                    conversation.append(("BuddyBug", response))
                    say(response)
                    
                    # Auto-scroll to the bottom of the conversation
                    scroll_offset = 0
                
            # Brief pause before next command
            time.sleep(0.5)
            
        except queue.Empty:
            # No command in queue, continue listening
            continue

# Function to show loading screen
def show_loading_screen():
    loading = True
    loading_start_time = time.time()
    loading_duration = 2  # seconds
    
    # Try to load and play startup sound
    try:
        startup_sound = pygame.mixer.Sound("startup.wav")
        startup_sound.play()
        print("Startup sound played successfully")
    except:
        print("Startup sound file not found. Continuing without sound.")
    
    while loading:
        current_time = time.time()
        elapsed = current_time - loading_start_time
        progress = min(elapsed / loading_duration, 1.0)
        
        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # Draw loading screen
        screen.fill(DARK_BG)
        
        # Draw title
        title_shadow = title_font.render("BuddyBug AI", True, (0, 0, 0))
        title_surface = title_font.render("BuddyBug AI", True, NEON_BLUE)
        screen.blit(title_shadow, (WIDTH // 2 - title_shadow.get_width() // 2 + 3, HEIGHT * 0.3 + 3))
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT * 0.3))
        
        # Draw loading text
        loading_text = main_font.render("Initializing...", True, WHITE)
        screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT * 0.5))
        
        # Draw animated loading circle
        center_x, center_y = WIDTH // 2, HEIGHT * 0.7
        radius = HEIGHT * 0.05
        
        # Outer rotating circle
        angle = elapsed * 5  # Rotation speed
        for i in range(8):
            dot_angle = angle + (i * math.pi / 4)
            dot_x = center_x + radius * math.cos(dot_angle)
            dot_y = center_y + radius * math.sin(dot_angle)
            dot_radius = HEIGHT * 0.01
            alpha = 255 - i * 30  # Decreasing alpha for trailing effect
            
            # Create a surface for the dot with alpha
            dot_surface = pygame.Surface((int(dot_radius * 2), int(dot_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(dot_surface, (*NEON_BLUE, alpha), (int(dot_radius), int(dot_radius)), int(dot_radius))
            screen.blit(dot_surface, (dot_x - dot_radius, dot_y - dot_radius))
        
        # Progress bar
        bar_width = WIDTH * 0.6
        bar_height = HEIGHT * 0.02
        bar_x = (WIDTH - bar_width) // 2
        bar_y = HEIGHT * 0.8
        
        # Background of progress bar
        pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height), border_radius=int(bar_height//2))
        
        # Progress fill
        fill_width = bar_width * progress
        pygame.draw.rect(screen, NEON_GREEN, (bar_x, bar_y, fill_width, bar_height), border_radius=int(bar_height//2))
        
        # Percentage text
        percent_text = small_font.render(f"{int(progress * 100)}%", True, WHITE)
        screen.blit(percent_text, (bar_x + bar_width + 20, bar_y - bar_height//2))
        
        pygame.display.flip()
        
        # Check if loading is complete
        if elapsed >= loading_duration:
            loading = False
            
        pygame.time.Clock().tick(60)

# Start the command processor thread
command_thread = threading.Thread(target=command_processor)
command_thread.daemon = True

# Main loop
clock = pygame.time.Clock()
running = True

# Show loading screen first
show_loading_screen()

# Now load modules after loading screen
load_modules()

# Add the first command to start the listening process
command_queue.put("LISTEN")

# Start the command processor thread after loading
command_thread.start()

# Set app as loaded
app_loaded = True

# Initial greeting
if modules_available:
    say("Your personal assistant is ready, at your service, sir")
print("🤖 BuddyBug is ready...")

while running and not shutdown:
    current_time = time.time()
    dt = clock.tick(60) / 1000  # Delta time in seconds
    session_duration = current_time - session_start_time
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown = True
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                shutdown = True
                running = False
            elif event.key == pygame.K_SPACE:
                # Manually trigger a new command
                if not processing and not listening:
                    command_queue.put("LISTEN")
            elif event.key == pygame.K_UP:
                # Scroll up
                scroll_offset = min(scroll_offset + 20, 0)
            elif event.key == pygame.K_DOWN:
                # Scroll down
                max_scroll = max(-(conversation_height - (HEIGHT - 150)), -1000)
                scroll_offset = max(scroll_offset - 20, max_scroll)
            elif event.key == pygame.K_RETURN and input_active and text_input.strip():
                # Send on Enter key
                command_queue.put("TEXT_INPUT:" + text_input.strip())
                text_input = ""
                input_active = False
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    # Add character to input (with some basic filtering)
                    if event.unicode.isprintable() and len(text_input) < 100:
                        text_input += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if text input box is clicked
            if input_rect.collidepoint(event.pos):
                input_active = True
            elif send_button_rect.collidepoint(event.pos) and text_input.strip():
                # Send text message
                command_queue.put("TEXT_INPUT:" + text_input.strip())
                text_input = ""
                input_active = False
            else:
                input_active = False
            # Mouse wheel scrolling
        elif event.type == pygame.MOUSEWHEEL:
            # Mouse wheel scrolling
            scroll_offset += event.y * 20
            if scroll_offset > 0:
                scroll_offset = 0
            max_scroll = max(-(conversation_height - (HEIGHT - 150)), -1000)
            if scroll_offset < max_scroll:
                scroll_offset = max_scroll

    # Automatically listen for commands when not busy
    if not listening and not processing and command_queue.empty():
        command_queue.put("LISTEN")
    
    # Update animations
    wave_offset += dt * 2
    if current_time - last_pulse_time > 0.05:
        if pulse_growing:
            pulse_radius += 1
            if pulse_radius > 30:
                pulse_growing = False
        else:
            pulse_radius -= 1
            if pulse_radius < 5:
                pulse_growing = True
        last_pulse_time = current_time
    
    # Draw background
    if has_background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.blit(background_surface, (0, 0))
    
    # Draw rounded transparent white background for chat area
    chat_bg_rect = pygame.Rect(WIDTH * 0.01, HEIGHT * 0.2, WIDTH * 0.7 - WIDTH * 0.02, HEIGHT * 0.7)
    chat_bg_surface = pygame.Surface((chat_bg_rect.width, chat_bg_rect.height), pygame.SRCALPHA)
    # Semi-transparent white background (adjust alpha as needed)
    pygame.draw.rect(chat_bg_surface, (255, 255, 255, 40), 
                    (0, 0, chat_bg_rect.width, chat_bg_rect.height),
                    border_radius=15)
    screen.blit(chat_bg_surface, (chat_bg_rect.x, chat_bg_rect.y))
    
    # Draw conversation area on left side
    conversation_y = HEIGHT * 0.21 + scroll_offset  # Increased to make space for top elements
    conversation_height = 0  # Reset for calculation
    
    # Calculate total conversation height
    for speaker, message in conversation:
        # Word wrapping for conversation text
        words = message.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = conversation_font.render(test_line, True, WHITE)
            if test_surface.get_width() < WIDTH * 0.65 - 50:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        conversation_height += len(lines) * 25 + 10
    
    # Draw conversation messages
    for speaker, message in conversation:
        if speaker == "You":
            text_color = USER_TEXT_COLOR
            prefix = "You: "
        else:
            text_color = AI_TEXT_COLOR
            prefix = "BuddyBug: "
        
        # Word wrapping for conversation text
        words = message.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = conversation_font.render(prefix + test_line, True, text_color)
            if test_surface.get_width() < WIDTH * 0.65 - 50:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw each line of the message
        for i, line in enumerate(lines):
            if i == 0:
                line_text = prefix + line
            else:
                line_text = "       " + line  # Indent wrapped lines
            
            text_surface = conversation_font.render(line_text, True, text_color)
            
            # Only draw if within visible area
            if conversation_y > HEIGHT * 0.21 and conversation_y < HEIGHT * 0.9:
                screen.blit(text_surface, (WIDTH * 0.03, conversation_y))
            
            conversation_y += 25
        
        conversation_y += 10  # Add spacing between messages

    # Draw text input box with rounded corners
    input_bg = pygame.Surface((input_rect.width, input_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(input_bg, (255, 255, 255, 40), 
                    (0, 0, input_rect.width, input_rect.height),
                    border_radius=10)
    screen.blit(input_bg, (input_rect.x, input_rect.y))

    # Draw input text
    input_surface = conversation_font.render(text_input, True, WHITE)
    screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10))

    # Draw send button with icon
    send_bg = pygame.Surface((send_button_rect.width, send_button_rect.height), pygame.SRCALPHA)
    send_color = NEON_BLUE if text_input.strip() else (100, 100, 100, 100)
    pygame.draw.rect(send_bg, send_color, 
                    (0, 0, send_button_rect.width, send_button_rect.height),
                    border_radius=8)
    screen.blit(send_bg, (send_button_rect.x, send_button_rect.y))

    # Draw send icon (simple arrow)
    pygame.draw.polygon(screen, WHITE, [
        (send_button_rect.x + send_button_rect.width * 0.3, send_button_rect.y + send_button_rect.height * 0.3),
        (send_button_rect.x + send_button_rect.width * 0.7, send_button_rect.y + send_button_rect.height * 0.5),
        (send_button_rect.x + send_button_rect.width * 0.3, send_button_rect.y + send_button_rect.height * 0.7)
    ])

    # Draw placeholder text when empty
    if not text_input and not input_active:
        placeholder = conversation_font.render("Type a message...", True, (200, 200, 200, 150))
        screen.blit(placeholder, (input_rect.x + 10, input_rect.y + 10))
    
    # Draw pulse ball at the TOP RIGHT
    center_x, center_y = int(WIDTH * 0.85), int(HEIGHT * 0.25)  # Positioned at top right
    
    # Outer pulsing circles
    for i in range(3):
        radius = int(HEIGHT * 0.05) + pulse_radius - i*8  # Slightly smaller for top position
        alpha = 120 - i*30  # More transparent
        
        # Create a surface for the transparent circle
        circle_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        color_with_alpha = (*NEON_BLUE, alpha)
        pygame.draw.circle(circle_surface, color_with_alpha, (radius, radius), radius)
        screen.blit(circle_surface, (center_x - radius, center_y - radius))
    
    # Main circle with different colors based on state
    circle_color = NEON_GREEN if listening else NEON_PURPLE if processing else NEON_BLUE
    pygame.draw.circle(screen, circle_color, (center_x, center_y), int(HEIGHT * 0.008))
    
    # Draw status text - WHITE and BOLD, below the pulse ball
    status_text = "Listening..." if listening else "Processing..." if processing else "Speaking"
    status_surface = main_font.render(status_text, True, WHITE)  # White color
    screen.blit(status_surface, (center_x - status_surface.get_width() // 2, center_y + int(HEIGHT * 0.1)))
    
    # Draw session timer and date at top left
    timer_text = f"Session: {format_time(session_duration)}"
    date_text = f"Date: {format_date()}"
    timer_surface = small_font.render(timer_text, True, WHITE)
    date_surface = small_font.render(date_text, True, WHITE)
    screen.blit(timer_surface, (WIDTH * 0.02, HEIGHT * 0.03))
    screen.blit(date_surface, (WIDTH * 0.02, HEIGHT * 0.06))  # Positioned below the timer
    
    # Draw title with shadow effect
    title_shadow = title_font.render("BuddyBug AI", True, (0, 0, 0))
    title_surface = title_font.render("BuddyBug AI", True, NEON_BLUE)
    screen.blit(title_shadow, (WIDTH // 2 - title_shadow.get_width() // 2 + 2, HEIGHT * 0.03 + 2))
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT * 0.03))
    
    # Draw instructions at the bottom
    instructions = [
        "Press SPACE to speak immediately",
        "Type message and click send or press ENTER",
        "Press ESC to exit",
        "Scroll with mouse wheel or UP/DOWN keys"
    ]
    
    for i, instruction in enumerate(instructions):
        inst_surface = small_font.render(instruction, True, WHITE)  # White color
        screen.blit(inst_surface, (WIDTH - inst_surface.get_width() - WIDTH * 0.02, 
                                  HEIGHT * 0.85 + i * int(HEIGHT * 0.03)))
    
    # Draw visualization bars (sound visualization simulation)
    if listening or processing:
        for i in range(10):  # Fewer bars for smaller circle
            bar_height = 6 + abs(math.sin(time.time() * 3 + i * 0.2)) * 25
            color = NEON_GREEN if listening else NEON_RED
            pygame.draw.rect(screen, color, 
                            (center_x - 60 + i * 12, center_y + 25 - bar_height/2, 6, bar_height),
                            border_radius=2)
    
    # Draw audio waves animation around the circle
    if listening:
        for i in range(4):  # Fewer waves for smaller circle
            wave_size = 12 + 6 * math.sin(time.time() * 4 + i * 0.5)
            # Create a surface for the transparent wave
            wave_surface = pygame.Surface((int(120 + wave_size*2), int(120 + wave_size*2)), pygame.SRCALPHA)
            wave_color = (*NEON_GREEN, 100)
            pygame.draw.circle(wave_surface, wave_color, 
                              (int(60 + wave_size), int(60 + wave_size)), 
                              int(60 + wave_size), 2)
            screen.blit(wave_surface, (center_x - 60 - wave_size, center_y - 60 - wave_size))
    
    pygame.display.flip()
    clock.tick(60)

# Clean up
shutdown = True
command_queue.put("SHUTDOWN")
command_thread.join(timeout=1.0)
pygame.quit()
sys.exit()