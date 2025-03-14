# импортируем библиотеки
import pygame
import random
import time
import threading
import sys


WIDTH = 800
HEIGHT = 600
pygame.init() # инициализмруем pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаем экран
clock = pygame.time.Clock() # создаём переменную времени

# импортируем шрифты и изображения
font = pygame.font.Font('ARCADECLASSIC.TTF', 36)
font1 = pygame.font.Font('ARCADECLASSIC.TTF', 50)
font2 = pygame.font.Font('pico-8.TTF', 10)

asteroid1 = pygame.image.load('asteroid.png').convert_alpha()
asteroid2 = pygame.image.load('asteroid (1).png').convert_alpha()
asteroid3 = pygame.image.load('asteroid (2).png').convert_alpha()
heart_pic = pygame.image.load('life.png').convert_alpha()
player_pic = pygame.image.load('space-shuttle.png').convert_alpha()
surface = pygame.image.load('pixil-frame-0.png').convert_alpha()
logo = pygame.image.load('1.png').convert_alpha()

start_surface = surface
quit_surface = surface
again_surface = surface
quit_again_surface = surface

# изменяем размер
start_surface = pygame.transform.scale(start_surface, (250, 85))
logo = pygame.transform.scale(logo, (512, 288))
again_surface = pygame.transform.scale(start_surface, (250, 85))

# надпись о создателе
production_text = font2.render('timofei production', True,(148, 0, 211))
production_rect = production_text.get_rect(centerx = 700, centery = 570)
def production_blit():
	screen.blit(production_text,production_rect)

# создаём класс кнопки
class Button():
	def __init__(self, image, x, y, text_input): # свойства
		self.image = image
		self.x = x
		self.y = y
		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.text_input = text_input
		self.text = font.render(self.text_input, True, (0, 255 ,34))
		self.text_rect = self.text.get_rect(center=(self.x, self.y))
	def button_blit(self): # отрисовка кнопки
		screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position): # функция проверки на нажатие
		if position[0] in range(self.rect.left, self.rect.right) and \
		position[1] in range(self.rect.top, self.rect.bottom):
			return True



# создаём две кнопки
start = Button(start_surface, WIDTH/2, 370, 'START')
quit = Button(quit_surface, WIDTH/2, 470, 'QUIT')

# функция отрисовки логотипа
logo_rect = logo.get_rect(centerx = WIDTH/2, centery = 180)
def logo_blit():
	screen.blit(logo, logo_rect)

# функция запускающая сцену меню
def main_menu():
	running = True
	while running:
		
		clock.tick(60) # частота кадров
		for event in pygame.event.get():
			if event.type== pygame.QUIT: # если нажали на крестик, выходим из программы
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if start.checkForInput(pygame.mouse.get_pos()): # если нажали на "старт", запускаем функцию play
					play()
					running = False
				if quit.checkForInput(pygame.mouse.get_pos()): # если нажали на выход, выходим
					sys.exit()
		screen.fill((0, 0 ,0)) # очищаем экран
		# всё отрисовываем
		logo_blit()
		start.button_blit()
		quit.button_blit()
		production_blit()


		pygame.display.flip() # обновляем экран


# основная функция запуска сцены игры
def play():
	running = True
	
	# функция отрисовки счёта
	def score_blit(score):
		score_text = font.render(str(score), True,(180, 180, 180))
		screen.blit(score_text, (725, 25))

	# увеличение сложности
	def diff():
		
		global speed_e
		speed_e = 5 # скорость падения астероидов
		global spawns
		spawns = 0.2 # время между появлением астероидов
		while running:
			time.sleep(5)
			
			speed_e += 0.3
			spawns = spawns - 0.03*spawns	
	# создаём и запускаем отдельный поток для функции diff
	thr2 = threading.Thread(target = diff, daemon = True)
	thr2.start()




	# создаём класс игрока
	class Player(pygame.sprite.Sprite):
		def __init__(self):
			self.image = player_pic
			self.change = 0 # скорость игрока
			self.rect = pygame.Rect(370, 500, 64, 64)
	player = Player()
	# отрисовка
	def player_blit(x, y):
		screen.blit(player.image, (player.rect.x, player.rect.y))




	# список с каринками астероидов
	meteor_pics = [asteroid1, asteroid2, asteroid3]
	num_of_enemies = 10000

	# класс врагов (астероидов)
	class Enemy(pygame.sprite.Sprite):
		def __init__(self, image, speed):
			self.image = image
			self.change = speed
			self.rect = pygame.Rect(random.randint(0, 736), -64, 50, 50)
	
	# словарь для хранения списка врагов
	enemies = dict()

	# создание врагов
	def create_enemy():
		
		while running:
			for i in range(num_of_enemies):
				# создаем врагов путём добавления их в словарь, ключи - цифры
				enemies[i] = Enemy(meteor_pics[random.randint(0,2)], speed_e)
				time.sleep(spawns)
	# отдельный поток для функции create_enemy
	thr1 = threading.Thread(target = create_enemy, daemon = True)
	thr1.start()
	# отрисовка
	def enemy(x, y, image):
		screen.blit(image,(x, y))

	# класс жизни 
	class Life():
		def __init__(self, x, y):
			self.image = heart_pic
			self.x = x
			self.y = y
	# создаём 3 жизни, объединяем в список
	life1 = Life(50, 50)
	life2 = Life(100, 50)
	life3 = Life(150, 50)
	lifes = [life1, life2, life3]

	# отрисовка
	def life_blit(i):
		screen.blit(lifes[i].image, (lifes[i].x, lifes[i].y))

	# функция для проверки столкновения объектов
	def isCollision(enemy_rect, player_rect):
		if player_rect.colliderect(enemy_rect):
			return True
	
	global numb1 # для счёта
	numb1 = 1
	count_lifes = 3
	
	while running:
		clock.tick(60)
		# передвижение игрока
		for event in pygame.event.get():
			if event.type== pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.change = -5
					if event.key == pygame.K_RIGHT:
						player.change = 5
				if event.key == pygame.K_RIGHT:
					player.change = 5
					if event.key == pygame.K_LEFT:
						player.change = -5
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					player.change = 0
		player.rect.x = player.rect.x + player.change
		# ограничитель
		if player.rect.x <= 0:
			player.rect.x = 0
		elif player.rect.x >= 736:
			player.rect.x = 736

		# очищаем экран
		screen.fill((0, 0, 0))

		# отрисовка
		player_blit(player.rect.x, player.rect.x)

		# i принимает все значения от первого ключа в словаре с врагами до последнего
		for i in list(enemies.keys()): 
			
				
			if enemies[i].rect.y > 600: # если враг вылетел за пределы экрана, удаляем его и увеличиваем счёт
				numb1 += 1
				enemies.pop(i)
			elif isCollision(enemies[i].rect, player.rect): # если игрок стлокнулся с врагом, удалить врага и жизнь
				enemies.pop(i)
				lifes.pop()
			else: # отрисовываем и перемещаем врагов
				enemy(enemies[i].rect.x,enemies[i].rect.y, enemies[i].image)
				enemies[i].rect.y += enemies[i].change
		# отрисовываем счёт
		score_blit(list(enemies.keys())[0])

		# отрисовываем жизни
		for i in range(0,len(lifes)):
			life_blit(i)

		# если кол-во жизней = 0, переключаемся на меню повтора
		if len(lifes) == 0:
			running = False
			again_menu()
		# отрисовывем надпись 
		production_blit()

		# обновляем экран
		pygame.display.flip()
		print(speed_e, spawns)

# создаём кнопки
again = Button(start_surface, WIDTH/2, 350, 'Play again')
quit_again = Button(quit_surface, WIDTH/2, 450, 'QUIT')

# функция меню повтора
def again_menu():
	# отрисовываем счёт
	def score_blit(score):
		score_text = font1.render(str(score), True,(180, 180, 180))
		score_rect = score_text.get_rect(centerx = WIDTH/2, centery = 200)	
		result_text = font1.render('Your  score', True, (180,180,180))
		result_rect = result_text.get_rect(centerx = WIDTH/2, centery = 100)
		screen.blit(score_text, score_rect)
		screen.blit(result_text, result_rect)
	
	running = True
	while running:
		
		clock.tick(60)
		for event in pygame.event.get():
			if event.type== pygame.QUIT: # если нажали на крестик, выходим из программы
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if again.checkForInput(pygame.mouse.get_pos()): # если нажали на "играть снова", запускаем функцию play
					play()
					running  = False
				if quit_again.checkForInput(pygame.mouse.get_pos()): # если нажали на выход, выходим
					sys.exit()
		# очищаем экран, отрисовываем
		screen.fill((0, 0 ,0))
		again.button_blit()
		quit_again.button_blit()
		score_blit(numb1-1)
		production_blit()

		pygame.display.flip()




main_menu()



