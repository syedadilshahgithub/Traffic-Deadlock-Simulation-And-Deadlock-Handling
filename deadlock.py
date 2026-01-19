import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
ROAD_WIDTH = 200
CAR_SIZE = 70
CAR_SPEED = 2

COLOR_BG = (34, 139, 34)  
COLOR_ROAD = (50, 50, 50) 
COLOR_INTERSECTION = (40, 40, 40) 
COLOR_LINE = (255, 255, 255)
COLOR_TEXT = (255, 255, 255)

COLOR_NORTH = (255, 0, 0)    
COLOR_SOUTH = (0, 0, 255)   
COLOR_EAST = (255, 255, 0)   
COLOR_WEST = (0, 255, 0)    

try:
    IMG_RED = pygame.transform.scale(pygame.image.load('car_red.png'), (CAR_SIZE, CAR_SIZE))
    IMG_BLUE = pygame.transform.scale(pygame.image.load('car_blue.png'), (CAR_SIZE, CAR_SIZE))
    IMG_YELLOW = pygame.transform.scale(pygame.image.load('car_yellow.png'), (CAR_SIZE, CAR_SIZE))
    IMG_GREEN = pygame.transform.scale(pygame.image.load('car_green.png'), (CAR_SIZE, CAR_SIZE))
except pygame.error as e:
    print(f"Error loading images: {e}")
    sys.exit()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Traffic Deadlock Simulation")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)

class Car:
    def __init__(self, x, y, width, height, image, direction):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.direction = direction 
        self.speed = CAR_SPEED
        self.stopped = False
        
        if self.direction == 'S':
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == 'E':
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.direction == 'W':
            self.image = pygame.transform.rotate(self.image, 90)

    def move(self, other_cars):
        if self.stopped:
            return

        next_rect = self.rect.copy()
        if self.direction == 'S': 
            next_rect.y += self.speed
        elif self.direction == 'N': 
            next_rect.y -= self.speed
        elif self.direction == 'W': 
            next_rect.x -= self.speed
        elif self.direction == 'E': 
            next_rect.x += self.speed

        blocked = False
        for car in other_cars:
            if car != self:
                if next_rect.colliderect(car.rect):
                    blocked = True
                    break

        int_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        int_right = (SCREEN_WIDTH + ROAD_WIDTH) // 2
        int_top = (SCREEN_HEIGHT - ROAD_WIDTH) // 2
        int_bottom = (SCREEN_HEIGHT + ROAD_WIDTH) // 2
        
        in_intersection = (
            self.rect.centerx > int_left and self.rect.centerx < int_right and
            self.rect.centery > int_top and self.rect.centery < int_bottom
        )

        if blocked:
            self.stopped = True
        else:
            self.rect = next_rect

def draw_roads():
    screen.fill(COLOR_BG)

    pygame.draw.rect(screen, COLOR_ROAD, ((SCREEN_WIDTH - ROAD_WIDTH) // 2, 0, ROAD_WIDTH, SCREEN_HEIGHT))

    pygame.draw.rect(screen, COLOR_ROAD, (0, (SCREEN_HEIGHT - ROAD_WIDTH) // 2, SCREEN_WIDTH, ROAD_WIDTH))

    pygame.draw.rect(screen, COLOR_INTERSECTION, ((SCREEN_WIDTH - ROAD_WIDTH) // 2, (SCREEN_HEIGHT - ROAD_WIDTH) // 2, ROAD_WIDTH, ROAD_WIDTH))
    
    center_x = SCREEN_WIDTH // 2
    for y in range(0, SCREEN_HEIGHT, 40):
        if not ((SCREEN_HEIGHT - ROAD_WIDTH) // 2 <= y <= (SCREEN_HEIGHT + ROAD_WIDTH) // 2):
            pygame.draw.line(screen, COLOR_LINE, (center_x, y), (center_x, y + 20), 2)

    center_y = SCREEN_HEIGHT // 2
    for x in range(0, SCREEN_WIDTH, 40):
        if not ((SCREEN_WIDTH - ROAD_WIDTH) // 2 <= x <= (SCREEN_WIDTH + ROAD_WIDTH) // 2):
            pygame.draw.line(screen, COLOR_LINE, (x, center_y), (x + 20, center_y), 2)

def main():

    car_n = Car((SCREEN_WIDTH - CAR_SIZE) // 2 - 40, 50, CAR_SIZE, CAR_SIZE, IMG_RED, 'S')

    car_s = Car((SCREEN_WIDTH - CAR_SIZE) // 2 + 40, SCREEN_HEIGHT - 100, CAR_SIZE, CAR_SIZE, IMG_BLUE, 'N')

    car_e = Car(SCREEN_WIDTH - 100, (SCREEN_HEIGHT - CAR_SIZE) // 2 - 40, CAR_SIZE, CAR_SIZE, IMG_YELLOW, 'W')

    car_w = Car(50, (SCREEN_HEIGHT - CAR_SIZE) // 2 + 40, CAR_SIZE, CAR_SIZE, IMG_GREEN, 'E')

    cars = [car_n, car_s, car_e, car_w]

    running = True
    deadlock_detected = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for car in cars:
            car.move(cars)

        if all(car.stopped for car in cars):
            deadlock_detected = True

        draw_roads()
        
        for car in cars:
            screen.blit(car.image, car.rect)

        if deadlock_detected:
            text = font.render("DEADLOCK OCCURRED", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            pygame.draw.rect(screen, (0,0,0), text_rect.inflate(20, 20)) 
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
