import pygame
import sys
from os import path

from settings import *
from sprites import *
from tilemap import *


class Game:
    
    def __init__(self):
        """Initialize game."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        """Function to draw text to the screen."""
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        # Alignment attribute is point of text-rect to align
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)

        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        """Load all game data."""
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.map_folder = path.join(game_folder, 'maps')

        # load font
        self.title_font = path.join(img_folder, 'FROGGER.TTF')

        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))

    def new(self):
        """Initialize all variables and do all the setup for a new game."""
        self.map = TiledMap(path.join(self.map_folder, 'frogger_map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.homes = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.logs = pygame.sprite.Group()

        # place homes and players
        for x in HOME_LOCATIONS:
            x = x * TILESIZE
            Home(self, x)

        # spawn the cars
        self.create_cars()
        self.player = Player(self)


    def run(self):
        """Game Loop - set self.playing = False to end the game."""
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        """Function to quit game."""
        pygame.quit()
        sys.exit()

    def update(self):
        """Update portion of the game loop."""
        self.all_sprites.update()

        # frog reaches home
        arrivals = pygame.sprite.spritecollide(self.player, self.homes, True)
        for arrival in arrivals:
            self.player.reset_pos()
            self.map_img.blit(
                self.player.down_frames[0], (arrival.rect.centerx - 26, arrival.rect.centery - 18))

        # frog hits bush
        if self.player.in_bushes() and not arrivals:
            self.player.reset_pos()
            self.player.lives -= 1

        if pygame.sprite.spritecollideany(self.player, self.cars):
            self.player.reset_pos()
            self.player.lives -= 1

        if self.player.lives == 0:
            self.playing = False

    def draw(self):
        """Game Loop - draw"""
        # v DURING DEVELOPMENT: keep track of performance with fps! v
        #pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.map_rect)


        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def events(self):
        """Catch all events here."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_LEFT:
                    if self.player.rect.left - TILESIZE >= 0:
                        self.player.move_left()
                        self.player.moving = True
                if event.key == pygame.K_RIGHT:
                    if self.player.rect.right + TILESIZE <= WIDTH:
                        self.player.move_right()
                        self.player.moving = True
                if event.key == pygame.K_DOWN:
                    if self.player.rect.bottom + TILESIZE <= HEIGHT - TILESIZE:
                        self.player.move_down()
                        self.player.moving = True
                if event.key == pygame.K_UP:
                    self.player.move_up()
                    self.player.moving = True

    def show_start_screen(self):
        """Show the Start screen."""
        self.screen.fill(BLACK)
        self.draw_text("FROGGER", self.title_font, 105, GREEN,
                       int(WIDTH / 2), int(HEIGHT / 3), align="center")
        self.draw_text("Press any button to start", self.title_font, 40, WHITE,
                       int(WIDTH / 2), int(HEIGHT / 2), align="center")

        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        """Display the Game Over screen."""
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 105, GREEN,
                       int(WIDTH / 2), int(HEIGHT / 3), align="center")
        self.draw_text("Press any button to restart", self.title_font, 40, WHITE,
                       int(WIDTH / 2), int(HEIGHT / 2), align="center")
        self.draw_text("Press 'ESC' to quit", self.title_font, 40, WHITE,
                       int(WIDTH / 2), int((HEIGHT / 2) + 60), align="center")

        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        """Wait for keys while on start and g.o. screens."""
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def create_cars(self):
        """Create all the cars."""
        for lane in ROAD_LANES:
            for car_num in range(CARS_PER_LANE[lane]):
                self.create_car(car_num, lane)
    
    def create_car(self, car_num, lane):
        """Create a single car and place in lane."""
        car = Car(self, lane)
        car_width = car.rect.width
        # set spacing of cars
        if car.dir == 1:
            car.x = -(car_width + 3 * car_width * car_num)
        else:
            car.x = WIDTH + (car_width + 3 * car_width * car_num)
        car.rect.centerx = car.x
        car.rect.centery = int(lane * TILESIZE)

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

pygame.quit()
