from src.levels import level_1, level_2, level_3

def game_screen(screen, level):
    if level == 1:
        return level_1.run(screen)
    elif level == 2:
        return level_2.run(screen)
    elif level == 3:
        return level_3.run(screen)