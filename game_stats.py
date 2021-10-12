class GameStats:
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.level = 1

        # Start Alien Invasion in an active state.
        self.game_active = False

        #Get the old high score if exists
        self.get_high_score()
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
    
    def get_high_score(self):
        try:
            with open ("high_score.txt") as f:
                old_high_score=f.readline()
        except:
            self.high_score = 0
        else:
            self.high_score = int(old_high_score)
    
    def set_high_score(self):
        if(self.score >= self.high_score):
            try:
                with open ("high_score.txt","w") as f:
                    f.write(str(self.score))
            except:
                print("We couldn't retrieve the old higher score")
