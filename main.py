from controls import Controls
if __name__ == "__main__":
    game_level = 1  # 设置游戏等级
    c = Controls(game_level)
    while True:
        c.event_loop()
