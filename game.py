# int joyX = A0;
# int joyY = A1;
# int joyZ = A2;  // if your joystick has one
# void setup() {
#   Serial.begin(9600);
# }
# void loop() {
#   int xVal = analogRead(joyX);
#   int yVal = analogRead(joyY);
#   int zVal = analogRead(joyZ);
#   int pitch = map(yVal, 0, 1023, -90, 90);
#   int yaw   = map(xVal, 0, 1023, -90, 90);
#   int roll  = map(zVal, 0, 1023, -90, 90);
#   Serial.print(pitch); Serial.print(",");
#   Serial.print(yaw);   Serial.print(",");
#   Serial.println(roll);
#   delay(60);
# }
# 7:56
import game, serial, random
# ---------------- Serial Setup ----------------
ser = serial.Serial("COM4", 9600, timeout=1)  # Replace with your COM port
# ---------------- Pygame Setup ----------------
game.init()
W, H = 800, 600
screen = game.display.set_mode((W, H))
game.display.set_caption("2D Drone Dodger")
clock = game.time.Clock()
# ---------------- Drone ----------------
drone_radius = 20
drone_x, drone_y = W//2, H - 100  # start near bottom
drone_speed = 5
# ---------------- Obstacles ----------------
obstacle_radius = 20
obstacles = []
spawn_timer = 0
spawn_interval = 30  # frames
# ---------------- Score ----------------
score = 0
font = game.font.SysFont(None, 36)
# ---------------- Main Loop ----------------
running = True
while running:
    screen.fill((30,30,50))  # background
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    # ---------------- Read Joystick Data ----------------
    if ser.in_waiting:
        try:
            line = ser.readline().decode().strip()
            if line:
                pitch, yaw, roll = map(float, line.split(","))
                # map pitch/yaw to x/y movement
                dx = int(yaw/10)  # adjust sensitivity
                dy = int(-pitch/10)
                drone_x += dx
                drone_y += dy
        except:
            pass
    # Clamp drone inside screen
    drone_x = max(drone_radius, min(W - drone_radius, drone_x))
    drone_y = max(drone_radius, min(H - drone_radius, drone_y))
    # ---------------- Spawn Obstacles ----------------
    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        spawn_timer = 0
        obs_x = random.randint(obstacle_radius, W - obstacle_radius)
        obs_y = -obstacle_radius
        color = random.choice([(255,0,0),(0,255,0),(0,0,255),(255,255,0)])
        speed = random.randint(3,7)
        obstacles.append({'x': obs_x, 'y': obs_y, 'color': color, 'speed': speed})
    # ---------------- Move Obstacles ----------------
    for obs in obstacles:
        obs['y'] += obs['speed']
    # ---------------- Collision Check ----------------
    for obs in obstacles:
        if (drone_x - obs['x'])**2 + (drone_y - obs['y'])**2 < (drone_radius + obstacle_radius)**2:
            running = False  # game over
    # Remove off-screen obstacles
    obstacles = [obs for obs in obstacles if obs['y'] < H + obstacle_radius]
    # ---------------- Draw Obstacles ----------------
    for obs in obstacles:
        game.draw.circle(screen, obs['color'], (obs['x'], int(obs['y'])), obstacle_radius)
    # ---------------- Draw Drone ----------------
    game.draw.circle(screen, (0,255,150), (drone_x, drone_y), drone_radius)
    # ---------------- Update Score ----------------
    score += 1
    text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(text, (10,10))
    game.display.flip()
    clock.tick(60)
ser.close()
game.quit()