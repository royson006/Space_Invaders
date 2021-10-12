class Settings():
    def __init__(self):
        """Initialize de game settings"""

        #Audio Settings
        self.music = "sounds/musica_fondo.mp3"
        self.music_volume = 0.4
        self.shot_sound ="sounds/shot.wav"
        self.alien_explosion ="sounds/alien_explosion.wav"
        self.alien_shot ="sounds/alien_shot.wav"

        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        self.full_screen = True

        #Aliens settings
        self.fleet_drop_speed = 5
        self.aliens_points = 50
        self.score_scale = 1.5
        self.alien_vertical_space = 2
        self.alien_bullet_color = (255,87,51)
        self.alien_bullet_size = 7
        self.alien_bullet_speed = 1


        #Bullets config
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 5
        self.bullet_power = 50

        #Ship settings
        self.ship_limit = 3

        #How quickly the game speeds up
        self.speedup_scale = 1.1        #1.5 to play normal
        self.initialize_dynamic_settings()

        #Boss settings
        self.boss_speed_x = 0.5
        self.boss_speed_y = 0.5
        self.boss_bullets = 6 #must a even number
        self.boss_level = 4

    def initialize_dynamic_settings(self):
        """Initialize  the settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.5
        #fleet_direction = 1 represents right and fleet_direction = -1 represents left
        self.fleet_direction = 1
        self.aliens_points = 50
        self.alien_bullets_allowed = 5
        self.number_alien_2 = 0
        self.number_alien_3 = 0
    
    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.aliens_points += int(self.aliens_points * self.score_scale)
        self.alien_bullets_allowed += 2
        self.number_alien_2 += 1
        self.number_alien_3 += 0.5
        

