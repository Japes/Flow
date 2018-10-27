from pyglet.window import key

consts = {
    "window": {
        "width": 1280,
        "height": 720,
        "vsync": True,
        "resizable": True
    },
    "world": {
        "width": 800,
        "height": 600,
        "rPlayer": 8.0,
        "wall_scale_min": 0.75,  # relative to player
        "wall_scale_max": 2.25,  # relative to player
        "topSpeed": 100.0,
        "angular_velocity": 240.0,  # degrees / s
        "accel": 85.0,

    },
    "view": {
        # as the font file is not provided it will decay to the default font;
        # the setting is retained anyway to not downgrade the code
        "font_name": 'Axaxax',
        "palette": {
            'bg': (0, 65, 133),
            'player': (237, 27, 36),
            'wall': (247, 148, 29),
            'gate': (140, 198, 62),
            'food': (140, 198, 62)
        }
    }
}

screenHeight = consts["window"]["height"]
screenWidth = consts["window"]["width"]
hitBoxHeight = screenHeight/5

keyBindings =       [key.D, key.F, key.J, key.K]     # the buttons in order from left to right
hitBoxPositions =   [screenWidth/4 - screenWidth/16, screenWidth/4 + screenWidth/16, screenWidth*3/4 - screenWidth/16, screenWidth*3/4 + screenWidth/16]     # x coords of hitboxes in order from left to right
hitboxLabels =      ['assets/font/d.png', 'assets/font/f.png', 'assets/font/j.png', 'assets/font/k.png']
hitboxSounds =      ['assets/sounds/a4.wav', 'assets/sounds/b4.wav', 'assets/sounds/e4.wav', 'assets/sounds/g4.wav']
hitboxMissSounds =  ['assets/sounds/a3.wav', 'assets/sounds/b3.wav', 'assets/sounds/e4.wav', 'assets/sounds/g3.wav']

script_startflying = 2000