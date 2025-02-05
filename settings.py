class Settings:
    """| A class to store all settings for An Adventure |"""

    def __init__(self):
        """| Initialize the game's settings |"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (234, 230, 230)

        # Human settings
        self.human_speed_factor = 4

        self.fps = 60 # FPS