import pygame, sys
import pygame.font
import math
import game_functions as gf
from hero import Hero
from enemy import Enemy
from bullets import Bullet
from settings import Settings
from pygame.sprite import Group
from start_button import Play_button
from scoreboard import Scoreboard
from pygame.sprite import Sprite
pygame.init()

win = pygame.display.set_mode ((800, 600))

pygame.display.set_caption("Os Monstros fofos!")

def check_events(hero, bullet, game_settings, screen, play_button):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			
			if play_button.rect.collidepoint(mouse_x, mouse_y):
				game_settings.game_active = True

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:	
				hero.moving_right = True

			elif event.key == pygame.K_LEFT:
				hero.moving_left = True

			elif event.key == pygame.K_SPACE:
				new_bullet = Bullet(hero, game_settings, screen)
				bullet.add(new_bullet)	

			elif event.key == pygame.K_UP: 	
				hero.moving_up = True 

			elif event.key == pygame.K_DOWN: 	
				hero.moving_down = True 

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				hero.moving_right = False

			elif event.key == pygame.K_LEFT: 
				hero.moving_left = False

			elif event.key == pygame.K_UP: 
				hero.moving_up = False

			elif event.key == pygame.K_DOWN: 
				hero.moving_down = False				

while 1:
 gf.check_events(hero, bullets, game_settings, screen, play_button)
 gf.update_screen(game_settings, screen, hero, bullets, enemies, play_button, scoreboard)
 if game_settings.game_active:
    hero.update()
    enemies.update(hero, game_settings.enemy_speed)
    tick += 1
 if tick % 50 == 0:
    enemies.add(Enemy(screen, game_settings))
    bullets.update() 
				
 for enemy in enemies:
  for bullet in bullets:
      if bullet.rect.bottom <= 0:
         bullet.remove(bullet)
      if len(bullets) >= 10:
         bullets.remove(bullet)
      if enemy.rect.colliderect(bullet.rect):
         count += 1
         count_update = "Monstros Mortos: %d" %count
         scoreboard = Scoreboard(screen, count_update)
                                                            
         enemies.remove(enemy)
         bullets.remove(bullet)
         pygame.mixer.music.load('sounds/win.wav')
         pygame.mixer.music.play(0)
      if enemy.rect.colliderect(heroi.rect):
         print ("O Monstro deu-te uma coça!")
         pygame.mixer.music.load('sounds/lose.wav')
         pygame.mixer.music.play(0)

def update_screen(settings, screen, hero, bullets, enemies, play_button, scoreboard):

	screen.fill(settings.bg_color)
	hero.draw_me()
	for enemy in enemies.sprites():
		enemy.draw_enemy()
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	if not settings.game_active:	
		play_button.draw_button()
	scoreboard.draw_scoreboard()	

	pygame.display.flip()

class Settings():
	def __init__(self):
		self.screen_size = (800,600)
		self.bg_color = (153,170,1)
		self.bullet_speed = 8
		self.bullet_width = 5
		self.bullet_height = 10
		self.bullet_color = 0,0,0
		self.enemy_speed = 4
		self.game_active = False
class Bullet(Sprite):
	def __init__(self, hero, game_settings, screen):
		super(Bullet, self).__init__()
		self.screen = screen

		self.rect = pygame.Rect(0,0, game_settings.bullet_width, game_settings.bullet_height)
		self.rect.centerx = hero.rect.centerx
		self.rect.top = hero.rect.top
		self.color = game_settings.bullet_color
		self.speed = game_settings.bullet_speed
		self.y = self.rect.y

	def update(self):
		self.y -= self.speed
		self.rect.y = self.y

	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)
def run_game():
	pygame.init()
	game_settings = Settings()
	screen = pygame.display.set_mode(game_settings.screen_size)
	pygame.display.set_caption("Ataque Monstruoso")
	hero = Hero(screen)
	
	pygame.mixer.music.load('sounds/music.wav')
	pygame.mixer.music.play(-1)

	play_button = Play_button(screen, 'Pressiona para começar')

	count = 0
	count_update = "Monatros mortos: %d" %count
	scoreboard = Scoreboard(screen, count_update)

	enemies = Group()
	bullets = Group()
	enemies.add(Enemy(screen, game_settings))

	tick = 0


class Enemy(Sprite):
	def __init__(self, screen, game_settings):
		super(Enemy, self).__init__()
		self.screen = screen

		self.enemy_image = pygame.image.load('Imagens/Monster.jpg')
		self.rect = self.enemy_image.get_rect()
		self.screen_rect = screen.get_rect()

		self.rect.centerx = randint(self.screen_rect.left, self.screen_rect.right)
		self.rect.top = self.screen_rect.top

	def update(self, hero, speed = 3):
		dx, dy = self.rect.x - hero.rect.x, self.rect.y - hero.rect.y
		dist = math.hypot(dx, dy)
		dx, dy = dx / dist, dy / dist

		self.rect.x -= dx * speed
		self.rect.y -= dy * speed

	def draw_enemy(self):
		self.screen.blit(source = self.enemy_image, dest = self.rect)

	def __exit__(self, *err):
		self.remove(self)

class Hero(object):
  def __init__(self, screen):
   super(Hero, self).__init__()
   self.screen = screen 

   self.image = pygame.image.load('Imagens/heroi.jpg')
   self.rect = self.image.get_rect() 
   self.screen_rect = screen.get_rect()

   self.rect.centerx = self.screen_rect.centerx
   self.rect.bottom = self.screen_rect.bottom

   self.moving_right = False
   self.moving_left = False
   self.moving_up = False
   self.moving_down = False

  def update(self):
   if self.moving_right and self.rect.right < self.screen_rect.right:
    self.rect.centerx += 10
   elif self.moving_left and self.rect.left > self.screen_rect.left:
    self.rect.centerx -= 10
   elif self.moving_up and self.rect.top > self.screen_rect.top:
    self.rect.y -= 10
   elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
    self.rect.y += 10

  def draw_me(self):
    self.screen.blit(source = self.image, dest = self.rect)

class Play_button(object):
 def __init__(self, screen, button_text):
  self.screen = screen
  self.screen_rect = screen.get_rect()

  self.width = 250
  self.height = 100
  self.button_color = 0,200,150
  self.text_color = 255,255,255
  self.font = pygame.font.Font(None, 52)
  self.rect = pygame.Rect(0,0, self.width, self.height)
  self.rect.center = self.screen_rect.center
  self.setup_message(button_text)
		

 def setup_message(self, button_text):
  self.image_message =  self.font.render(button_text, True, self.text_color)
  self.image_message_rect = self.image_message.get_rect()
  self.image_message_rect.center = self.rect.center
		
 def draw_button(self):		
  self.screen.fill(self.button_color, self.rect)
  self.screen.blit(self.image_message, self.image_message_rect)


class Scoreboard(object):
 def __init__(self, screen, scoreboard_text):
  self.screen = screen
  self.screen_rect = screen.get_rect()

  self.width = 250
  self.height = 100
  self.scoreboard_color = 5, 2, 2
  self.text_color = 255,255,255
  self.font = pygame.font.Font(None, 40)
  self.rect = pygame.Rect(0,0, self.width, self.height)
  self.rect.centerx = self.screen_rect.centerx
  self.rect.top = self.screen_rect.top
  self.scoreboard_message(scoreboard_text)

 def scoreboard_message(self, scoreboard_text):
  self.image_message = self.font.render(scoreboard_text, True, self.text_color)
  self.image_message_rect = self.image_message.get_rect()
  self.image_message_rect.center = self.rect.center

 def draw_scoreboard(self):
  self.screen.fill(self.scoreboard_color, self.rect)
  self.screen.blit(self.image_message, self.image_message_rect)

pygame.mixer.init()
win_sound = pygame.mixer.Sound('sounds/win3.wav')
lose_sound = pygame.mixer.Sound('sounds/lose.wav')
lose_sound.play()
while True:
    pass

pygame.mixer.quit()
