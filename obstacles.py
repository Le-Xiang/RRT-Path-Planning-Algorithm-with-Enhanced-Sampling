import pygame


class Obstacles:
    """
    障碍物类，主要负责障碍物相关操作
    """
    def __init__(self, game_level: int, XDIM: int, YDIM: int):
        """
        初始化障碍物列表
        :param game_level: 游戏等级
        :param XDIM: 画布宽度
        :param YDIM: 画布高度
        """
        self.rect_list = None
        self.global_init(game_level, XDIM, YDIM)

    def global_init(self, game_level: int, XDIM: int, YDIM: int):
        """
        根据游戏等级，初始化障碍物列表
        :param game_level: 游戏等级
        :param XDIM: 画布宽度
        :param YDIM: 画布高度
        :return: 无
        """
        self.rect_list = []
        if (game_level == 0):
            self.rect_list.append(pygame.Rect((XDIM / 2.0 - 50, YDIM / 2.0 - 100), (100, 200)))
        if (game_level == 1):
            self.rect_list.append(pygame.Rect((100, 50), (200, 150)))
            self.rect_list.append(pygame.Rect((400, 200), (200, 100)))
        if (game_level == 2):
            self.rect_list.append(pygame.Rect((100, 50), (200, 150)))
        if (game_level == 3):
            self.rect_list.append(pygame.Rect((50, 50), (140, 60)))
            self.rect_list.append(pygame.Rect((400, 50), (150, 70)))
            self.rect_list.append(pygame.Rect((50, 200), (300, 50)))
            self.rect_list.append(pygame.Rect((350, 150), (60, 110)))
            self.rect_list.append(pygame.Rect((0, 300), (600, 60)))
            self.rect_list.append(pygame.Rect((200, 400), (150, 70)))
            self.rect_list.append(pygame.Rect((400, 420), (100, 70)))
