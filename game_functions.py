# --coding:utf-8 --
import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
	
	#响应被外星人撞到的飞船
	if stats.ships_left > 0:
		stats.ships_left -= 1
		
		sb.prep_ships()
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		
		#创建一群新的外星人，并将飞创放到屏幕底端中央来
		
		create_fleet(ai_settings,screen, ship,aliens)
		ship.center_ship()
		
		#暂停
		
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key == pygame.K_RIGHT:
		#向右移动
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		#创造一颗子弹添加到数组bullet
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()
	
def check_keyup_events(event,ship):
	
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	
	
	
	
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	
	#响应案件鼠标事件
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)	
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y =  pygame.mouse.get_pos()
			check_play_button(ai_settings, screen,stats,sb,play_button,ship
			,aliens,bullets,mouse_x , mouse_y)

def check_play_button(ai_settings,screen,stats, sb,play_button,ship,aliens,
		bullets,mouse_x,mouse_y):
	
	#在玩家单击PLay按钮时开始新游戏	
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		
		# 重置游戏设置
		ai_settings.initialize_dynamic_settings()
		
		#隐藏贯标
		pygame.mouse.set_visible(False)
		
		stats.reset_stats()
		stats.game_active = True
		#重置游戏统计信息
		
		#重置记分牌图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		
		# 创建一群新的外星人，并让飞船居中。
		create_fleet(ai_settings ,screen , ship, aliens)
		ship.center_ship()
		
		
				
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,
		play_button):
	#每次循环时重绘屏幕
	
	screen.fill(ai_settings.bgcolor)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	ship.blitme()
	aliens.draw(screen)
	# 显示得分
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	
	
	# 让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(ai_settings , screen, stats,sb,ship,aliens,bullets):
	
	bullets.update()
		
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullets_alien_collisions(ai_settings,screen,stats,sb,ship,
		aliens,bullets)

def check_bullets_alien_collisions(ai_settings,screen,stats,sb,
		ship,aliens,bullets):
	# 检查是否有子弹集中外星人
	# 如果试着好样的话，就删除相应的子弹和外星人
	collisions = pygame.sprite.groupcollide(bullets, aliens,True ,True)
	if len(aliens) ==0:
		# 删除现在所有子弹并创建的一圈外星人
		bullets.empty()
		ai_settings.increase_speed()
		stats.level +=1
		sb.prep_level()
		create_fleet(ai_settings,screen,ship,aliens)
		
	if collisions:
		
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		
		stats.score +=ai_settings.alien_points
		sb.prep_score()
		check_high_score(stats,sb)


		
def fire_bullet(ai_settings,screen,ship,bullets):
	
	
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def get_number_rows(ai_settings,ship_height,alien_height):
	# 计算屏幕可容纳多少行外星人
	
	available_space_y = (ai_settings.screen_height -
	                        (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows	
		

	
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2* alien.rect.height * row_number
	aliens.add(alien)
	
	
		
def create_fleet(ai_settings,screen,ship,aliens):
	
	#创建一个外星人群
	#创建一个外星人，并计算一行课容纳多少外星人
	#外星人的间距为外星人的宽度
	
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
	    alien.rect.height)
	
	
	#创建第一排外星人
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			#创建一个外星人，并加入该行
			create_alien(ai_settings,screen,aliens,alien_number,row_number)
	


def get_number_aliens_x(ai_settings,alien_width):
	
	#计算每行可容纳多少个外星人
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / ( 2 * alien_width) )
	return number_aliens_x
	
	

	
	
	
	
def check_fleet_edges(ai_settings,aliens):
	#外星人触碰到边缘时采取的相应的措施
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	#将外星人下移并改变他们的方向
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
	
	#检查是否有外星人处于屏幕边缘，整理并更新外星人的位置
	
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	#检查外星人和飞虎藏之间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
	check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)


def check_high_score(stats,sb):
	#检查是否产生最高分
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()


def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
	
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings,screen,stast,sb,ship,aliens,bullets)
			break




















	
	
	
	
	
	
