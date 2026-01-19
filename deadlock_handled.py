import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
ROAD_WIDTH = 200
CAR_SIZE = 70
CAR_SPEED = 3 

COLOR_BG = (34, 139, 34)  
COLOR_ROAD = (50, 50, 50) 
COLOR_INTERSECTION = (40, 40, 40)
COLOR_LINE = (255, 255, 255)
COLOR_TEXT = (255, 255, 255)

COLOR_NORTH = (255, 0, 0)    
COLOR_SOUTH = (0, 0, 255)   
COLOR_EAST = (255, 255, 0) 
COLOR_WEST = (0, 255, 0)   

COLOR_WAITING = (255, 0, 0)   
COLOR_MOVING = (0, 255, 0)   


try:
    IMG_RED = pygame.transform.scale(pygame.image.load('car_red.png'), (CAR_SIZE, CAR_SIZE))
    IMG_BLUE = pygame.transform.scale(pygame.image.load('car_blue.png'), (CAR_SIZE, CAR_SIZE))
    IMG_YELLOW = pygame.transform.scale(pygame.image.load('car_yellow.png'), (CAR_SIZE, CAR_SIZE))
    IMG_GREEN = pygame.transform.scale(pygame.image.load('car_green.png'), (CAR_SIZE, CAR_SIZE))
except pygame.error as e:
    print(f"Error loading images: {e}")
    sys.exit()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Traffic Deadlock Handled Simulation")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

class Car:
    def __init__(self, name, x, y, width, height, image, direction, priority):
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.direction = direction
        self.speed = CAR_SPEED
        self.priority = priority
        self.waiting = False
        self.crossed = False
        
        if self.direction == 'S':
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == 'E':
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.direction == 'W':
            self.image = pygame.transform.rotate(self.image, 90)

    def move(self, allowed_to_enter_intersection):
        next_rect = self.rect.copy()
        if self.direction == 'S':
            next_rect.y += self.speed
        elif self.direction == 'N':
            next_rect.y -= self.speed
        elif self.direction == 'W':
            next_rect.x -= self.speed
        elif self.direction == 'E':
            next_rect.x += self.speed

        int_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        int_right = (SCREEN_WIDTH + ROAD_WIDTH) // 2
        int_top = (SCREEN_HEIGHT - ROAD_WIDTH) // 2
        int_bottom = (SCREEN_HEIGHT + ROAD_WIDTH) // 2

        entering = False
        if self.direction == 'S' and self.rect.bottom <= int_top and next_rect.bottom > int_top:
            entering = True
        elif self.direction == 'N' and self.rect.top >= int_bottom and next_rect.top < int_bottom:
            entering = True
        elif self.direction == 'W' and self.rect.left >= int_right and next_rect.left < int_right:
            entering = True
        elif self.direction == 'E' and self.rect.right <= int_left and next_rect.right > int_left:
            entering = True

        if entering and not allowed_to_enter_intersection:
            self.waiting = True
            return 

        self.waiting = False
        self.rect = next_rect
        
        if self.direction == 'S' and self.rect.top > SCREEN_HEIGHT: self.crossed = True
        if self.direction == 'N' and self.rect.bottom < 0: self.crossed = True
        if self.direction == 'W' and self.rect.right < 0: self.crossed = True
        if self.direction == 'E' and self.rect.left > SCREEN_WIDTH: self.crossed = True

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

    car_n = Car("North", (SCREEN_WIDTH - CAR_SIZE) // 2 - 40, 50, CAR_SIZE, CAR_SIZE, IMG_RED, 'S', 1)

    car_e = Car("East", SCREEN_WIDTH - 100, (SCREEN_HEIGHT - CAR_SIZE) // 2 - 40, CAR_SIZE, CAR_SIZE, IMG_YELLOW, 'W', 2)

    car_s = Car("South", (SCREEN_WIDTH - CAR_SIZE) // 2 + 40, SCREEN_HEIGHT - 100, CAR_SIZE, CAR_SIZE, IMG_BLUE, 'N', 3)

    car_w = Car("West", 50, (SCREEN_HEIGHT - CAR_SIZE) // 2 + 40, CAR_SIZE, CAR_SIZE, IMG_GREEN, 'E', 4)

    cars = [car_n, car_e, car_s, car_w] 

    intersection_busy = False
    current_car = None

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_car and current_car.crossed:
            intersection_busy = False
            current_car = None
        
        if not intersection_busy:
            waiting_cars = [c for c in cars if c.waiting and not c.crossed]
            if waiting_cars:
                waiting_cars.sort(key=lambda c: c.priority)
                current_car = waiting_cars[0]
                intersection_busy = True

        for car in cars:
            allowed = False
            if car == current_car:
                allowed = True
            
            car.move(allowed)

        draw_roads()
        
        for car in cars:
            if car.waiting:
                pygame.draw.rect(screen, (255, 0, 0), car.rect.inflate(10, 10), 3)
            elif car == current_car:
                pygame.draw.rect(screen, (0, 255, 0), car.rect.inflate(10, 10), 3)
            
            screen.blit(car.image, car.rect)

        if all(c.crossed for c in cars):
            text = font.render("DEADLOCK AVOIDED", True, (0, 255, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            pygame.draw.rect(screen, (0,0,0), text_rect.inflate(20, 20))
            screen.blit(text, text_rect)
        else:
            if current_car:
                status = f"Moving: {current_car.name}"
                col = (0, 255, 0)
            else:
                status = "Waiting..."
                col = (255, 255, 255)
            
            s_text = small_font.render(status, True, col)
            screen.blit(s_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
