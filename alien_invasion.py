
import sys
import pygame
import random
from pygame.mixer import music
from pygame.mixer import Sound
from time         import sleep

from bullet         import Bullet
from settings       import Settings
from ship           import Ship
from bullet         import Bullet
from alien          import Alien
from game_stats     import GameStats
from button         import Button
from scoreboard     import Scoreboard
from alien_bullet   import AlienBullet
from boss           import Boss

class AlienInvasion:
    """Overall class to manage game assets and behaivor"""
    def __init__(self):
        """Initialize the game, and crete de resources"""

        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()

        #Enable Music
        music.load(self.settings.music)
        self.shot_sound = Sound(self.settings.shot_sound)
        self.alien_explosion = Sound(self.settings.alien_explosion)
        self.alien_shot = Sound(self.settings.alien_shot)
        music.set_volume(self.settings.music_volume)
        music.play(-1) # to repeat the song  in a infinite loop


        if ( self.settings.full_screen):
            self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width,self.settings.screen_height)
                )
        pygame.display.set_caption("Alien Invasion")

        #Instance from statics and ScoreBoard
        self.stats=GameStats(self)
        self.scoreboard = Scoreboard(self)


        self.ship=Ship(self)
        self.bullets    = pygame.sprite.Group()
        self.aliens     = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.boss       =Boss(self)


        #setting background color
        self.bg_color=(230,230,230)

        #Make a play button
        self.play_button=Button(self,"Let´s Play")

    def run_game(self):
        """Start the main loop for the game"""

        while True:
            self._check_events()
            if(self.stats.game_active):
                self.ship.update()
                self._check_is_level_enemy(action='U')
                self._update_bullets()
                self._update_aliens_bullets()
            self._update_screen()

    def _check_events(self):
        #Respond the key press and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif (event.type == pygame.KEYDOWN):
                self._check_keydown_events(event)
            elif (event.type == pygame.KEYUP):
                self._check_keyup_events(event)
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_buttom(mouse_pos)

    def _check_play_buttom(self,mouse_pos):
        #Check if the click is in the button and so, start the game
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_keydown_events(self,event):
        """Respond to key presses"""
        if(event.key == pygame.K_RIGHT):
            #move the ship to the right
            self.ship.moving_right = True
        elif(event.key == pygame.K_LEFT):
            #move the ship to the left
            self.ship.moving_left = True
        elif(event.key == pygame.K_SPACE):
            #Shot a bullet
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """Respond to key realeses"""
        if(event.key == pygame.K_RIGHT):
            #stop to moving the ship
            self.ship.moving_right = False
        elif(event.key == pygame.K_LEFT):
            #stop to moving the ship
            self.ship.moving_left = False
        elif(event.key == pygame.K_q):
            sys.exit()
        elif(event.key == pygame.K_p and not self.stats.game_active):
            self._start_game()

    def _start_game(self):
        #Reset the speed settings
        self.settings.initialize_dynamic_settings()
        #Reset statics
        self.stats.reset_stats()
        self.stats.game_active=True
        #Prepare all the Scoreboard
        self.scoreboard.prep_images()


        #Get ride any of reamining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        #Create a new flee and recenter the ship
        self._check_is_level_enemy('C')
        self.ship.center_ship()

        #Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if(len(self.bullets) < self.settings.bullets_allowed):
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
            self.shot_sound.play()
    
    def _update_aliens_bullets(self):
        """Update the alien,s bullets"""
        self._check_is_level_enemy('F')
        self.alien_bullets.update()
        self._check_collid_alien_bullet_ship()
        
    def _fire_allien_bullets(self):
        """Create alien bullets"""

        #Condition to check that number of bulles been less than aliens
        if (len(self.aliens) < self.settings.alien_bullets_allowed ):
            bullets_allowed = len(self.aliens)
        else:
            bullets_allowed = self.settings.alien_bullets_allowed

        if(len(self.alien_bullets) <  bullets_allowed):
            for alien in  random.sample(self.aliens.sprites(),
                    bullets_allowed-len(self.alien_bullets)):
                current_bullet = AlienBullet(self,
                    {"x":alien.rect.midbottom[0],"y":alien.rect.midbottom[1]})
                current_bullet.draw()
                self.alien_bullets.add(current_bullet)
                self.alien_shot.play()

    def _fire_boss_bullets(self):
        """Create the boss bullets"""
        if(random.choice(range(0,100)) == 1):
            for nb in range(0,self.settings.boss_bullets):
                bullet1 = AlienBullet(self,
                                {"x":self.boss.rect.bottomleft[0],
                                "y":self.boss.rect.bottomleft[1]
                            })
                bullet2 = AlienBullet(self,
                                {"x":self.boss.rect.bottomright[0],
                                "y":self.boss.rect.bottomright[1]
                            })

                bullet1.draw()
                bullet2.draw()
                self.alien_bullets.add(bullet1)
                self.alien_bullets.add(bullet2)
                self.alien_shot.play()




    def _update_bullets(self):
        """Update the position of the bullets and get ride old bullets"""
        self.bullets.update()
        #Removing all the bullets out of screen (SHIP)
        for bullet in self.bullets.copy():
            if(bullet.rect.bottom <=0):
                self.bullets.remove(bullet)

        self._check_is_level_enemy('CH')

        #Removing all the bullets out of screen (Aliens)
        for bullet in self.alien_bullets.copy():
            if(bullet.y >= self.screen.get_rect().bottom):
                self.alien_bullets.remove(bullet)
    
    def _check_collid_alien_bullet_ship(self):
        """Check if some alien's bullet hit the ship"""
        if(pygame.sprite.spritecollideany(self.ship,self.alien_bullets)
            #or pygame.sprite.collide_rect(self.ship,self.boss)
            ):
            self._ship_hit()

    def _check_collide_bullet_alien(self):
        #Check for any bullets that have hit aliens
        # if so, get rid the bullet and the alien
        collisions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,False)
        if (collisions):
            for aliens in collisions.values():
                self.stats.score += self.settings.aliens_points * len (aliens)
                #Check the health of each alien hitted by a bullet
                for alien in aliens:
                    alien.health -= self.settings.bullet_power
                    if(alien.health <= 0):
                        self.alien_explosion.play()
                        alien.kill()
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            # and not self.boss:
            #Destroy existing aliens and create a new fleet
            self._next_level()

    def _check_collid_boss_bullet_ship(self):
        """Check if some ship's bullet hits the boss"""
        bullet_on_target=pygame.sprite.spritecollideany(self.boss,self.bullets)
        if(bullet_on_target):
            self.alien_explosion.play()
            bullet_on_target.kill()
            self.boss.life_points-=10
            if(self.boss.life_points == 0):
                self.boss.kill()
                self._next_level()


    def _next_level(self):
        """Put all the variables for the next level"""
        self.bullets.empty()
        self.settings.increase_speed()
        self.stats.level += 1
        self._check_is_level_enemy('C')
        self.scoreboard.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an Edge
            Update the position of the aliens fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        #Look for a ship an alien colision
        if(pygame.sprite.spritecollideany(self.ship,self.aliens)):
            self._ship_hit()
        #Check if an alien hits came to the bottom
        self._check_aliens_bottom()
        pygame.mouse.set_visible(True)
        
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        #Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        #Draw a Ship
        self.ship.blitime()

        #Printing all the bullets
        for bullet in self.bullets:
            bullet.draw_bullet()

        #Printing all the aliens bullets
        for alien_bullet in self.alien_bullets:
            alien_bullet.draw()

        self._check_is_level_enemy('D')


        #Draw the score information
        self.scoreboard.show_score()

        #Draw the buttom to start the game
        if not self.stats.game_active:
            self.play_button.draw_button()

        #Make the most recently drawn screen visible
        pygame.display.flip()

    def _create_alien(self,alien_number,row_number,level):
        """Create an alien and place it in a row"""
        alien = Alien(self,level)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        #Multiply by 2 to leave space in top
        alien.y = (alien_height * 2) + (self.settings.alien_vertical_space * 
                                    alien_height * row_number)
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if(alien.check_edges()):
                self._check_fleet_direction()
                break

    def _check_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Drop the entire fleet and change the fleet's direction """

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        #Determine the nummber of aliens in the axis = y
        ship_height=self.ship.rect.height
        available_space_y = (self.settings.screen_height - (6 * alien_height)
                            -ship_height)
        number_rows_available = available_space_y // (2 * alien_height)

        #Determine the nummber of aliens in the axis = x
        available_space = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space // (2 * alien_width)



        for row_number in range(number_rows_available):
            #Get de aliens level
            no_aliens_level_2,no_aliens_level_3 = self._aliens_by_level(number_aliens_x)

            for alien_number in range(number_aliens_x):
                if (alien_number in no_aliens_level_3):
                    #Alien level 3
                    self._create_alien(alien_number,row_number,3)
                elif (alien_number in no_aliens_level_2):
                    #Alien level 2
                    self._create_alien(alien_number,row_number,2)
                else:
                    #Alien level 1
                    self._create_alien(alien_number,row_number,1)

    def _aliens_by_level(self,number_aliens_x):
        """Generate de level of each alien"""
        no_aliens_level_2 = random.sample(range(0,number_aliens_x),
                                        self.settings.number_alien_2)
        aliens_available = [cn for cn in range(0,number_aliens_x)
                                if cn not in no_aliens_level_2]
        no_aliens_level_3 = random.sample(aliens_available,
                                        int(self.settings.number_alien_3))
        return no_aliens_level_2,no_aliens_level_3

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if(alien.rect.bottom >= screen_rect.bottom):
                #Tret like the alien hits the ship
                self._ship_hit()
                break

    def _ship_hit(self):
        #Respond to the ship being hit by an alien
        if (self.stats.ships_left > 0):
            #Call the sound for destruction
            self.alien_explosion.play()

            #Drecrements de ships lef
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            #Get ride of any remaining bullet
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            #Create a new fleet and center the ship
            self._check_is_level_enemy('C')
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.stats.set_high_score()

    def _check_is_level_enemy(self,action):
        """Method to control enemy and fleet drawing and updating"""
        enemy= ((self.stats.level % self.settings.boss_level) == 0)
        if (enemy):
            if(action == 'U'):
                self.boss.update()
            elif(action == 'C' or action == 'D'):
                self.boss.blitime()
            elif(action == 'F'):
                self._fire_boss_bullets()
            elif(action == 'CH'):
                self._check_collid_boss_bullet_ship()
            elif(action == 'D'):
                self._check_collid_boss_bullet_ship()
        else:
            if(action == 'U'):
                self._update_aliens()
            elif(action == 'C'):
                self._create_fleet()
            elif(action == 'F'):
                self._fire_allien_bullets()
            elif(action == 'CH'):
                self._check_collide_bullet_alien()
            elif(action == 'D'):
                self.aliens.draw(self.screen)

if(__name__=="__main__"):
    #Make a game instance and run the game
    ai=AlienInvasion()
    ai.run_game()