WIDTH, HEIGHT = 900, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
FPS = 60

# Colors
WHITE = (240, 240, 240)
BLACK = (15, 15, 18)
GRAY = (80, 85, 95)
ECHO_COLOR = (180, 150, 255)
PLAYER_COLOR = (255, 220, 80)
ENEMY_COLOR = (255, 80, 110)
ORB_COLOR = (80, 255, 160)
FOCUS_COLOR = (120, 200, 255)

# Player parameters
PLAYER_RADIUS = 10
PLAYER_SPEED = 240.0
DASH_SPEED = 540.0
DASH_COOLDOWN = 0.9  # seconds
DASH_DURATION = 0.12

# Focus (slow time) parameters
FOCUS_MAX = 100
FOCUS_REGEN = 18.0  # per second
FOCUS_DRAIN = 45.0  # per second while holding SHIFT
MIN_SLOW = 0.55     # slow factor when focusing

# Echo parameters
ECHO_RADIUS = 7
ECHO_LIFETIME = 6.5  # seconds
ECHO_SPAWN_DELAY = 0.6  # seconds between echoes at start (decreases with difficulty)

# Enemy parameters
ENEMY_RADIUS = 10
ENEMY_SPEED_MIN = 60.0
ENEMY_SPEED_MAX = 120.0
ENEMY_SPAWN_EVERY = 1.25  # seconds (decreases with difficulty)

# Orb parameters
ORB_RADIUS = 8
ORB_LIFETIME = 8.0
ORB_SPAWN_EVERY = 4.5

# Difficulty scaling
DIFF_EVERY = 8.0   # seconds between difficulty bumps
DIFF_ECHO_DELAY_MULT = 0.94
DIFF_ENEMY_RATE_MULT = 0.93
DIFF_ENEMY_SPEED_ADD = 0.1
DIFF_ORB_RATE_MULT = 0.98
