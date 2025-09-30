import time
import pygame
from obstacles import Obstacles

class Colors:
    """
    颜色类，负责控制绘图颜色
    """
    def __init__(self):
        self.white = 255, 255, 255
        self.black = 0, 0, 0
        self.red = 255, 0, 0
        self.blue = 0, 0, 255
        self.green = 0, 255, 0
        self.cyan = 0, 180, 105

class MainWindow:
    """
    主窗口类负责可视化部分，包括窗口绘制、窗口清除、障碍物绘制、点的绘制和清除
    """

    def __init__(self, XDIM: int, YDIM: int):
        """
        初始化一个窗口
        :param XDIM: 画布宽度
        :param YDIM: 画布高度
        """
        pygame.init()
        self.colors = Colors()
        self.windowSize = [XDIM, YDIM]
        self.screen = pygame.display.set_mode(self.windowSize)
        self.fpsClock = pygame.time.Clock()
        self.global_init()
    def global_init(self):
        """
        窗口重置函数
        :return: 无
        """
        self.screen.fill(self.colors.white)
        pygame.display.set_caption("请输入起始节点:")
    def draw_obstacles(self,objtacles:Obstacles):
        """
        根据障碍物列表，绘制障碍物
        :param objtacles: 障碍物列表
        :return: 无
        """
        for rect in objtacles.rect_list:
            pygame.draw.rect(self.screen, self.colors.black, rect)

    def draw_lines(self,point_list:list,color=None):
        """
        根据点列表，绘制连线
        :param point_list: 绘图点组成的列表
        :param color: 颜色
        :return: 无
        """
        if color==None:
            color=self.colors.red
        for i in range(len(point_list)-1):
            pygame.draw.line(self.screen,color,point_list[i],point_list[i+1],2)
            time.sleep(0.0001)
            pygame.display.update()

