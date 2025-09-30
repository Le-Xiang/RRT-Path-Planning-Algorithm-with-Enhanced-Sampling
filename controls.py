import time
from mainwindow import MainWindow, pygame
from obstacles import Obstacles
from calculates import Datas, Calculates


class Controls:
    """
    游戏控制类，负责游戏流程控制，统筹整个项目
    """

    def __init__(self, game_level: int = 1, XDIM: int = 720, YDIM: int = 500):
        """
        全局初始化
        :param game_level: 游戏等级
        :param XDIM: 画布宽度
        :param YDIM: 画布高度
        """
        self.game_level = game_level
        self.window = MainWindow(XDIM, YDIM)
        self.obstacles = Obstacles(game_level, XDIM, YDIM)
        self.window.draw_obstacles(self.obstacles)
        self.state = 0  # 0:初始状态 1:已确定起始点 2:已确定结束点 3:RRT执行完毕 4:修剪执行完毕 5:A类优化算法执行完毕 6:B类优化算法执行完毕 7:C类优化算法执行完毕
        self.datas = Datas()
        self.calculates = Calculates(self.obstacles, XDIM, YDIM)

    def global_init(self):
        """
        全局重置
        :return: 无
        """
        self.datas.global_init()
        self.window.global_init()
        self.obstacles.global_init(self.game_level, self.window.windowSize[0], self.window.windowSize[1])
        self.window.draw_obstacles(self.obstacles)
        self.state = 0

    def event_loop(self):
        """
        pygame事件循环
        :return: 无
        """
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE):
                exit(0)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if self.state == 0:
                    if self.calculates.collides(e.pos) == False:
                        self.datas.set_init_point(e.pos)
                        self.state = 1
                        pygame.display.set_caption("goal point set:")
                        pygame.draw.circle(self.window.screen, self.window.colors.red
                                           , self.datas.initNode.point, 10)
                elif self.state == 1:
                    if self.calculates.collides(e.pos) == False:
                        self.datas.set_goal_point(e.pos)
                        self.state = 2
                        pygame.draw.circle(self.window.screen, self.window.colors.green
                                           , self.datas.goalNode.point, 10)
                        pygame.display.set_caption("Performing C-RRT")
                        if self.calculates.performRRT(self.window.screen, 10, self.datas) == True:
                            self.window.draw_lines(self.datas.pointTrace, (255, 0, 0))
                            pygame.display.set_caption("Goal reached, click to start Path pruning")
                            self.state = 3
                elif self.state == 3:
                    pygame.display.set_caption("Performing Path pruning")
                    self.calculates.performTRIM(self.datas)
                    start_time = time.time()
                    pygame.display.set_caption("Path pruning success,click to start Path optimization A")
                    end_time = time.time()
                    print(f"Time of Path pruning:{end_time - start_time}s")
                    print("Length of Path pruning:" + str(Calculates.getDistance(self.datas.pointTrace)))
                    self.window.draw_lines(self.datas.pointTrace, (0, 0, 255))
                    self.state = 4
                elif self.state == 4:
                    self.window.global_init()
                    self.window.draw_obstacles(self.obstacles)
                    self.window.draw_lines(self.datas.pointTrace, (0, 0, 0))
                    pygame.display.set_caption("Performing Path optimization A")
                    start_time = time.time()
                    self.calculates.performOptimizeA(self.window.screen, self.datas)
                    end_time = time.time()
                    print(f"Time of Path optimization A:{end_time - start_time}s")
                    print("Length of Path optimization A:" + str(Calculates.getDistance(self.datas.optAPoints)))
                    pygame.display.set_caption("Path optimization A success,click to start Path optimization B")
                    self.window.draw_lines(self.datas.optAPoints, (255, 0, 0))
                    self.state = 5
                elif self.state == 5:
                    self.window.global_init()
                    self.window.draw_obstacles(self.obstacles)
                    self.window.draw_lines(self.datas.pointTrace, (0, 0, 0))
                    pygame.display.set_caption("Performing Path optimization B")
                    start_time = time.time()
                    self.calculates.performOptimizeB(self.window.screen, self.datas)
                    end_time = time.time()
                    print(f"Time of Path optimization B:{end_time - start_time}s")
                    print("Length of Path optimization B:" + str(Calculates.getDistance(self.datas.optBPoints)))
                    pygame.display.set_caption("Path optimization B success, click to start Path optimization C")
                    self.window.draw_lines(self.datas.optBPoints, (255, 0, 0))
                    self.state = 6
                elif self.state == 6:
                    self.window.global_init()
                    self.window.draw_obstacles(self.obstacles)
                    self.window.draw_lines(self.datas.pointTrace, (0, 0, 0))
                    pygame.display.set_caption("Performing Path optimization C")
                    start_time = time.time()
                    self.calculates.performOptimizeC(self.window.screen, self.datas, 100)
                    end_time = time.time()
                    print(f"Time of Path optimization C:{end_time - start_time}s")
                    print("Length of Path optimization C:" + str(Calculates.getDistance(self.datas.optCPoints)))
                    pygame.display.set_caption("Path optimization C success, click to generate new start point")
                    self.window.draw_lines(self.datas.optCPoints, (255, 0, 0))
                    self.state = 7
                else:
                    self.global_init()
                    print("----------")
