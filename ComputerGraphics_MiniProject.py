import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Initialize Pygame
pygame.init()

# Set up display
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, -1.0, -10)

# Load road texture
road_texture = pygame.image.load('ground.jpg')
road_texture_data = pygame.image.tostring(road_texture, "RGB", 1)
width = road_texture.get_width()
height = road_texture.get_height()

glEnable(GL_TEXTURE_2D)
glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, 1)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, road_texture_data)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

# Car properties
car_position = [0.0, 0.0, 0.0]
car_angle = 0.0
wheel_rotation = 0.0
velocity = 0.0
acceleration_rate = 0.001
brake_rate = 0.005
friction = 0.0007
turn_speed = 2.0
boundary = 8.0
max_velocity = 2

# Set up fonts
font = pygame.font.Font(None, 36)

# Function to draw a simple car
def draw_car():
    glPushMatrix()
    glTranslatef(car_position[0], car_position[1], car_position[2])
    glRotatef(car_angle, 0, 1, 0)
    
    # Draw car body
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)  # Front face
    glVertex3f(-0.5, -0.25, 1.0)
    glVertex3f(0.5, -0.25, 1.0)
    glVertex3f(0.5, 0.25, 1.0)
    glVertex3f(-0.5, 0.25, 1.0)
    
    glColor3f(0.0, 0.0, 1.0)  # Back face
    glVertex3f(-0.5, -0.25, -1.0)
    glVertex3f(0.5, -0.25, -1.0)
    glVertex3f(0.5, 0.25, -1.0)
    glVertex3f(-0.5, 0.25, -1.0)
    
    glColor3f(0.5, 0.0, 0.0)  # Left face
    glVertex3f(-0.5, -0.25, -1.0)
    glVertex3f(-0.5, -0.25, 1.0)
    glVertex3f(-0.5, 0.25, 1.0)
    glVertex3f(-0.5, 0.25, -1.0)
    
    glColor3f(0.5, 0.0, 0.0)  # Right face
    glVertex3f(0.5, -0.25, -1.0)
    glVertex3f(0.5, -0.25, 1.0)
    glVertex3f(0.5, 0.25, 1.0)
    glVertex3f(0.5, 0.25, -1.0)
    
    glColor3f(0.5, 0.0, 0.0)  # Bottom face
    glVertex3f(-0.5, -0.25, -1.0)
    glVertex3f(0.5, -0.25, -1.0)
    glVertex3f(0.5, -0.25, 1.0)
    glVertex3f(-0.5, -0.25, 1.0)
    
    glColor3f(0.5, 0.0, 0.0)  # Top face
    glVertex3f(-0.5, 0.25, -1.0)
    glVertex3f(0.5, 0.25, -1.0)
    glVertex3f(0.5, 0.25, 1.0)
    glVertex3f(-0.5, 0.25, 1.0)
    glEnd()
    
    # Draw wheels
    draw_wheel(0.4, -0.35, 0.7)  # Front right
    draw_wheel(-0.4, -0.35, 0.7)  # Front left
    draw_wheel(0.4, -0.35, -0.7)  # Back right
    draw_wheel(-0.4, -0.35, -0.7)  # Back left
    
    glPopMatrix()

# Function to draw a wheel with white-black-white pattern
def draw_wheel(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(wheel_rotation, 1, 0, 0)  # Rotate wheel based on movement
    glRotatef(90, 0, 1, 0)  # Rotate to make the cylinder vertical
    
    quad = gluNewQuadric()
    
    # Draw the tire with white-black-white pattern
    glBegin(GL_QUAD_STRIP)
    for angle in range(0, 361, 10):
        rad = math.radians(angle)
        x = 0.1 * math.cos(rad)
        y = 0.1 * math.sin(rad)
        if angle % 20 < 10:
            glColor3f(1.0, 1.0, 1.0)  # White
        else:
            glColor3f(0.0, 0.0, 0.0)  # Black
        glVertex3f(x, y, 0.0)
        glVertex3f(x, y, 0.2)
    glEnd()
    
    # Draw the wheel caps
    glColor3f(0.0, 0.0, 0.0)  # Black wheel caps
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for angle in range(0, 361, 10):
        glVertex3f(0.1 * math.cos(math.radians(angle)), 0.1 * math.sin(math.radians(angle)), 0)
    glEnd()
    
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0.2)
    for angle in range(0, 361, 10):
        glVertex3f(0.1 * math.cos(math.radians(angle)), 0.1 * math.sin(math.radians(angle)), 0.2)
    glEnd()
    
    glPopMatrix()

# Function to draw the road
def draw_road():
    glBindTexture(GL_TEXTURE_2D, 1)
    glColor3f(1.0, 1.0, 1.0)  # Ensure the road texture is not affected by color
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-10, -1, -10)
    glTexCoord2f(10.0, 0.0)
    glVertex3f(10, -1, -10)
    glTexCoord2f(10.0, 10.0)
    glVertex3f(10, -1, 10)
    glTexCoord2f(0.0, 10.0)
    glVertex3f(-10, -1, 10)
    glEnd()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        if keys[K_a]:
            acceleration = acceleration_rate * 20
        else:
            acceleration = acceleration_rate
    elif keys[K_DOWN]:
        acceleration = -acceleration_rate
    else:
        acceleration = 0.0

    if keys[K_b]:
        velocity = 0

    if keys[K_LEFT]:
        car_angle += turn_speed
    if keys[K_RIGHT]:
        car_angle -= turn_speed

    # Apply friction
    if velocity > 0:
        velocity -= friction
        if velocity < 0:
            velocity = 0
    elif velocity < 0:
        velocity += friction
        if velocity > 0:
            velocity = 0

    # Update velocity and position
    velocity += acceleration
    if velocity > max_velocity:
        velocity = max_velocity
    elif velocity < -max_velocity:
        velocity = -max_velocity

    car_position[0] += velocity * math.sin(math.radians(car_angle))
    car_position[2] += velocity * math.cos(math.radians(car_angle))

    # Update wheel rotation based on velocity
    wheel_rotation -= (velocity * 360) / (2 * math.pi * 0.1)  # Assuming wheel radius is 0.1

    # Enforce boundaries
    if car_position[0] > boundary:
        car_position[0] = boundary
    elif car_position[0] < -boundary:
        car_position[0] = -boundary
    if car_position[2] > boundary:
        car_position[2] = boundary
    elif car_position[2] < -boundary:
        car_position[2] = -boundary

    # Clear the screen and set the background color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.5, 0.5, 1.0)

    # Draw the road
    draw_road()

    # Draw the car
    draw_car()

    # Draw controls and buttons
    text = font.render("Controls:", True, (255, 255, 255))
    pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), (600, 10, 200, 120))
    pygame.display.get_surface().blit(text, (610, 20))
    text = font.render("Accelerate: Up Arrow", True, (255, 255, 255))
    pygame.display.get_surface().blit(text, (610, 50))
    text = font.render("Brake: B", True, (255, 255, 255))
    pygame.display.get_surface().blit(text, (610, 80))
    text = font.render("Turn Left: Left Arrow", True, (255, 255, 255))
    pygame.display.get_surface().blit(text, (610, 110))
    text = font.render("Turn Right: Right Arrow", True, (255, 255, 255))
    pygame.display.get_surface().blit(text, (610, 140))
    text = font.render("Move Backwards: Down Arrow", True, (255, 255, 255))
    pygame.display.get_surface().blit(text, (610, 170))
    text = font.render("Double Acceleration: A + Up Arrow", True, (255, 255, 255))
    pygame.display.get_surface().blit(text, (610, 200))

    # Swap the buffers
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
