import os.path
import pygame
from random import random, randint
import time

def main():
	pygame.init()
	surface = pygame.display.set_mode((1200, 800))
	pygame.display.set_caption('The /g/ame')

	player = Player()
	spells = []
	enemies = [Enemy(), Enemy()]
	explosions = [] 

	fps_clock = pygame.time.Clock()

	bg_sprite = Sprite('background.png')
	player_sprite = Sprite('player.png')
	spell1_sprite = Sprite('spell1.png')
	explosion_sprite = Sprite('explosion.png')
	enemy_sprites = [
		Sprite('enemy_gates.png'),
		Sprite('enemy_jobs.png'),
		Sprite('enemy_davis.png'),
	]

	pygame.mixer.music.load(os.path.join('assets', 'bg_music.wav'))
	pygame.mixer.music.play()
	death_sound = pygame.mixer.Sound(os.path.join('assets', 'enemy_death.wav'))
	
	font = pygame.font.Font(None, 100)

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				speed = 7
				key = event.key
				if key == pygame.K_LEFT:
					player.pos.dx = -speed
				elif key == pygame.K_RIGHT:
					player.pos.dx = speed
				elif key == pygame.K_UP:
					player.pos.dy = -speed
				elif key == pygame.K_DOWN:
					player.pos.dy = speed
				elif key == pygame.K_SPACE:					
					spells.append(Spell(player.pos))
			elif event.type == pygame.KEYUP:
				key = event.key				
				if key == pygame.K_LEFT:
					player.pos.dx = 0
				elif key == pygame.K_RIGHT:
					player.pos.dx = 0
				elif key == pygame.K_UP:
					player.pos.dy = 0
				elif key == pygame.K_DOWN:
					player.pos.dy = 0

		player.pos.update()
		for spell in spells:
			spell.pos.update()

		for enemy in enemies[:]:
			enemy.update(player.pos)

			for spell in spells:
				if enemy.was_hit(spell.pos):
					enemies.remove(enemy)
					spells.remove(spell)
					explosions.append(Explosion(enemy.pos))
					death_sound.play()
					break
			if enemy.was_hit(player.pos):
				player.dead = True

		for explosion in explosions[:]:
			if explosion.should_delete():
				explosions.remove(explosion)

		if random() < 0.2:
			enemies.append(Enemy())

		bg_sprite.draw(surface, Pos())
		
		if not player.dead:
			player_sprite.draw(surface, player.pos)
			for spell in spells:
				spell1_sprite.draw(surface, spell.pos)
			for enemy in enemies:
				enemy_sprites[enemy.sprite].draw(surface, enemy.pos)
			for explosion in explosions:
				explosion_sprite.draw(surface, explosion.pos)
		else:
			gamer_over = font.render("Game Over!", True, (255, 0, 0))
			stallman = font.render("Stallman is dead", True, (255, 0, 0))
			surface.blit(gamer_over, (400, 250))
			surface.blit(stallman, (320, 350))

		pygame.display.update()
		fps_clock.tick(30)
	pygame.quit()
			
class Sprite:
	def __init__(self, file):
		self.image = pygame.image.load(os.path.join('assets', file))

	def draw(self, surface, pos):
		surface.blit(self.image, pygame.Rect(pos.x, pos.y, 100, 100))

LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3

class Pos:
	def __init__(self, x = 0, y = 0, dx = 0, dy = 0):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.dir = LEFT

	def update(self):
		self.x += self.dx
		self.y += self.dy

		if self.dx < 0:
			self.dir = LEFT
		elif self.dx > 0:
			self.dir = RIGHT
		elif self.dy < 0:
			self.dir = TOP
		elif self.dy > 0:
			self.dir = BOTTOM
	
	def __str__(self):
		return 'pos: ({},{}), speed: ({},{})'.format(self.x, self.y, self.dx, self.dy)

class Explosion:
	def __init__(self, pos):
		self.pos = pos
		self.time = time.time()

	def should_delete(self):
		return time.time() - self.time > 0.25

class Enemy:
	def __init__(self):
		self.pos = Pos()
		self.sprite = randint(0, 2)
		if random() > 0.5:
			self.pos.y = randint(0, 800)
			if random() > 0.5:
				self.pos.x = 0
			else:
				self.pos.x = 1200
		else:
			self.pos.x = randint(0, 1200)
			if random() > 0.5:
				self.pos.y = 0
			else:
				self.pos.y = 800
	
	def update(self, player):
		speed = 1
		dx = self.pos.x - player.x
		dy = self.pos.y - player.y
		if dx > 0:
			self.pos.dx = -speed
		else:
			self.pos.dx = speed
		if dy > 0:
			self.pos.dy = -speed
		else:
			self.pos.dy = speed
		self.pos.update()


	def was_hit(self, pos):
		width = 100
		height = 100
		return self.pos.x < pos.x + 50 < self.pos.x + width and self.pos.y < pos.y + 50 < self.pos.y + height

class Player:
	def __init__(self):
		self.pos = Pos(1200/2, 800/2)
		self.dead = False

class Spell:
	def __init__(self, pos):
		self.pos = Pos(pos.x, pos.y)
		speed = 20
		if pos.dir == LEFT:
			self.pos.dx = -speed
		elif pos.dir == RIGHT:
			self.pos.dx = speed
		elif pos.dir == TOP:
			self.pos.dy = -speed
		else:
			self.pos.dy = speed


main()