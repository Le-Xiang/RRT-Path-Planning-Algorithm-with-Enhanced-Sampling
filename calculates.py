import time
from math import *
from obstacles import Obstacles
import pygame
import random


class Node:
    def __init__(self, point: tuple, parent=None):
        self.point = point
        self.parent = parent


class Datas:
    """
    数据类，用于存放程序使用过程中的各种数据
    """
    def __init__(self):
        """
        初始化
        """
        # RRT算法生成的未修剪的路线点列表
        self.pointTrace = []
        # 以下是对原代码进行的封装，用法与之前的全局变量相同
        self.nodes = []
        self.initNode = Node((0, 0), None)
        self.goalNode = Node((0, 0), None)
        # 分别使用ABC三种方法进行路径优化后的路线点列表
        self.optAPoints=[]
        self.optBPoints=[]
        self.optCPoints = []

    def global_init(self):
        """
        重置数据
        :return:无
        """
        self.initNode = Node((0, 0), None)
        self.goalNode = Node((0, 0), None)
        self.nodes = []
        self.pointTrace = []
        self.optAPoints = []
        self.optBPoints = []
        self.optCPoints = []

    def set_init_point(self, point: tuple):
        """
        设置起始点
        :param point: 起始点
        :return: 无
        """
        self.initNode = Node(point, None)
        self.nodes.append(self.initNode)  # Start in the center

    def set_goal_point(self, point: tuple):
        """
        设置目标点
        :param point: 目标点
        :return: 无
        """
        self.goalNode = Node(point, None)


class Calculates:
    """
    计算类，用于实现各种大大小小的计算，公有方法用于调用，私有方法为公有方法服务
    """
    def __init__(self, obstacles: Obstacles, XDIM: int, YDIM: int):
        """
        初始化
        :param obstacles: 障碍物列表
        :param XDIM: 画布宽度
        :param YDIM: 画布高度
        """
        self.obstaclesList = obstacles.rect_list
        self.XDIM = XDIM
        self.YDIM = YDIM

    def performRRT(self, screen, radius: int, datas: Datas, delta=10.0, maxNodes=10000, color=(0, 180, 105)) -> bool:
        """
        执行RRT算法
        :param screen: 画布
        :param radius: 点的半径
        :param datas: 数据
        :param delta: 步长
        :param maxNodes: 最大节点数
        :param color: 颜色
        :return: 执行成功为TRUE，超过最大节点数为FALSE
        """
        count = 0
        time_start = time.time()
        while True:
            count += 1
            if count < maxNodes:
                foundNext = False
                while foundNext == False:
                    rand = self.get_random_clear()
                    parentNode = datas.nodes[0]
                    for p in datas.nodes:
                        if Calculates.dist(p.point, rand) <= Calculates.dist(parentNode.point, rand):
                            newPoint = Calculates.step_from_to(p.point, rand, datas.goalNode.point, delta)
                            if self.collides(newPoint) == False and self.collides_line(newPoint,p.point)==False:
                                parentNode = p
                                foundNext = True

                newnode = Calculates.step_from_to(parentNode.point, rand, datas.goalNode.point, delta)
                datas.nodes.append(Node(newnode, parentNode))
                pygame.draw.line(screen, color, parentNode.point, newnode)
                pygame.display.update()
                if Calculates.point_circle_collision(newnode, datas.goalNode.point, radius):
                    goalNode = datas.nodes[len(datas.nodes) - 1]
                    currNode = goalNode
                    print("C-RRT success")
                    distance = 0
                    while currNode.parent != None:
                        datas.pointTrace.append(currNode.point)
                        distance = distance + Calculates.dist(currNode.point, currNode.parent.point)
                        currNode = currNode.parent
                    datas.pointTrace.append(currNode.point)
                    time_end = time.time()
                    time_sum = time_end - time_start
                    print("Total length of path:" + str(distance))
                    print("Total number of path nodes:" + str(count))
                    print("Total time:" + str(time_sum) + "s")
                    datas.pointTrace.reverse()
                    return True
            else:
                print("not Found!")
                return False

    def performTRIM(self, datas: Datas):
        """
        进行修剪
        :param datas:数据
        """
        delete=1
        while delete>0:
            delete=0
            if len(datas.pointTrace)>=3:
                i=1
                curLen=len(datas.pointTrace)
                while (i+1)<curLen:
                    if self.collides_line(datas.pointTrace[i-1],datas.pointTrace[i+1])==False:
                        a = Calculates.dist(datas.pointTrace[i - 1], datas.pointTrace[i])
                        b = Calculates.dist(datas.pointTrace[i + 1], datas.pointTrace[i])
                        c = Calculates.dist(datas.pointTrace[i - 1], datas.pointTrace[i + 1])
                        if c < (a+b):
                            datas.pointTrace.pop(i)
                            delete+=1
                            curLen-=1
                            i-=1
                    i+=1
    def performOptimizeA(self,screen,datas:Datas,pointsNum:int=100):
        """
        使用A类型的边界进行路径优化
        :param screen: 画布
        :param datas: 数据
        :param pointsNum: 优化随机取的点数
        :return: 无
        """
        datas.optAPoints=datas.pointTrace.copy()
        for i in range(1,len(datas.optAPoints)-1):
            (xmin,xmax,ymin,ymax)=Calculates.getMinBox(datas.optAPoints[i-1],datas.optAPoints[i],datas.optAPoints[i+1])
            pygame.draw.rect(screen,(0,255,0),pygame.Rect(xmin,ymin,(xmax-xmin),(ymax-ymin)),1)
            minPoint=datas.optAPoints[i]
            minDist=Calculates.getDistance(datas.optAPoints)
            count=0
            while count<pointsNum:
                datas.optAPoints[i] = (random.uniform(xmin, xmax), random.uniform(ymin, ymax))
                max_tries=1000
                while self.collides_line(datas.optAPoints[i-1],datas.optAPoints[i])==True or self.collides_line(datas.optAPoints[i+1],datas.optAPoints[i])==True:
                    datas.optAPoints[i] = (random.uniform(xmin, xmax), random.uniform(ymin, ymax))
                    max_tries-=1
                    if max_tries<=0:
                        break
                if max_tries<=0:
                    break
                distance=Calculates.getDistance(datas.optAPoints)
                if distance<minDist:
                    minPoint=datas.optAPoints[i]
                    minDist=distance
                count+=1
            datas.optAPoints[i]=minPoint

    def performOptimizeB(self, screen, datas: Datas, pointsNum: int = 100):
        """
                使用B类型的边界进行路径优化
                :param screen: 画布
                :param datas: 数据
                :param pointsNum: 优化随机取的点数
                :return: 无
        """
        datas.optBPoints = datas.pointTrace.copy()
        for i in range(1, len(datas.optBPoints) - 1):
            (x,y,r)=Calculates.getCircleB(datas.optBPoints[i-1],datas.optBPoints[i],datas.optBPoints[i+1])
            pygame.draw.circle(screen,(0,255,0),(x,y),r,1)
            minPoint = datas.optBPoints[i]
            minDist = Calculates.getDistance(datas.optBPoints)
            count = 0
            while count < pointsNum:
                rou=random.uniform(0,r)
                theta=random.uniform(0,6.28)
                datas.optBPoints[i]=(x+rou*cos(theta),y+rou*sin(theta))
                max_tries = 1000
                while self.collides_line(datas.optBPoints[i-1],datas.optBPoints[i])==True or self.collides_line(datas.optBPoints[i+1],datas.optBPoints[i])==True:
                    rou = random.uniform(0, r)
                    theta = random.uniform(0, 6.28)
                    datas.optBPoints[i] = (x + rou * cos(theta), y + rou * sin(theta))
                    max_tries-=1
                    if max_tries<=0:
                        break
                if max_tries<=0:
                    break
                distance = Calculates.getDistance(datas.optBPoints)
                if distance < minDist:
                    minPoint = datas.optBPoints[i]
                    minDist = distance
                count += 1
            datas.optBPoints[i] = minPoint

    def performOptimizeC(self, screen, datas: Datas,r:int, pointsNum: int = 100):
        """
                使用C类型的边界进行路径优化
                :param screen: 画布
                :param datas: 数据
                :param r: 优化时所取圆的半径
                :param pointsNum: 优化随机取的点数
                :return: 无
        """
        datas.optCPoints = datas.pointTrace.copy()
        for i in range(1, len(datas.optCPoints) - 1):
            x=datas.optCPoints[i][0]
            y=datas.optCPoints[i][1]
            pygame.draw.circle(screen, (0, 255, 0), (x, y), r, 1)
            minPoint = datas.optCPoints[i]
            minDist = Calculates.getDistance(datas.optCPoints)
            count = 0
            while count < pointsNum:
                rou = random.uniform(0, r)
                theta = random.uniform(0, 6.28)
                datas.optCPoints[i] = (x + rou * cos(theta), y + rou * sin(theta))
                max_tries = 1000
                while self.collides_line(datas.optCPoints[i - 1], datas.optCPoints[i]) == True or self.collides_line(
                        datas.optCPoints[i + 1], datas.optCPoints[i]) == True:
                    rou = random.uniform(0, r)
                    theta = random.uniform(0, 6.28)
                    datas.optCPoints[i] = (x + rou * cos(theta), y + rou * sin(theta))
                    max_tries -= 1
                    if max_tries <= 0:
                        break
                if max_tries <= 0:
                    break
                distance = Calculates.getDistance(datas.optCPoints)
                if distance < minDist:
                    minPoint = datas.optCPoints[i]
                    minDist = distance
                count += 1
            datas.optCPoints[i] = minPoint
    # 以下均为私有方法
    @staticmethod
    def getCircleB(p1: tuple,p2: tuple,p3: tuple)->tuple:
        """
        获取B区域的圆形
        :param p1:点1
        :param p2:点2
        :param p3:点3
        :return: x,y,r
        """
        x=0.5*(p1[0]+p3[0])
        y=0.5*(p1[1]+p3[1])
        r=Calculates.dist((x,y),p2)
        return (x,y,r)

    @staticmethod
    def getMinBox(p1: tuple,p2: tuple,p3: tuple)->tuple:
        """
        获取最小包围盒
        :param p1:点1
        :param p2:点2
        :param p3:点3
        :return:(xmin,xmax,ymin,ymax)
        """
        xmin=min(p1[0],p2[0],p3[0])
        xmax=max(p1[0],p2[0],p3[0])
        ymin = min(p1[1], p2[1], p3[1])
        ymax = max(p1[1], p2[1], p3[1])
        return (xmin,xmax,ymin,ymax)
    @staticmethod
    def getDistance(pList:list)->float:
        """
        获取路线总距离
        :param pList:路线列表
        :return:总距离
        """
        distSum=0
        for i in range(len(pList)-1):
            distSum+=Calculates.dist(pList[i],pList[i+1])
        return distSum
    def collides_line(self,p1: tuple,p2: tuple,num:int=1000):
        """
        检测连线是否碰撞
        :param p1:点1
        :param p2:点2
        :param num:取点的数量
        :return:连线是否与障碍物相碰撞
        """
        dx=(p2[0]-p1[0])/num
        dy=(p2[1]-p1[1])/num
        for i in range(1,num):
            p=(p1[0]+dx*i,p1[1]+dy*i)
            for rect in self.obstaclesList:
                if rect.collidepoint(p) == True:
                    return True
        return False

    def get_random_clear(self):
        while True:
            p = random.random() * self.XDIM, random.random() * self.YDIM
            noCollision = self.collides(p)
            if noCollision == False:
                return p

    def collides(self, p: tuple):  # check if point collides with the obstacle
        for rect in self.obstaclesList:
            if rect.collidepoint(p) == True:
                return True
        return False

    @staticmethod
    def dist(p1: tuple, p2: tuple):
        return sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

    @staticmethod
    def point_circle_collision(p1, p2, radius):
        distance = Calculates.dist(p1, p2)
        if (distance <= radius):
            return True
        return False

    @staticmethod
    def step_from_to(p1, p2, p3, delta):
        Vbx = p2[0] - p1[0]
        Vby = p2[1] - p1[1]
        Vcx = p3[0] - p1[0]
        Vcy = p3[1] - p1[1]
        angle_line = (Vbx * Vcx + Vby * Vcy) / sqrt((Vbx * Vbx + Vby * Vby) * (Vcx * Vcx + Vcy * Vcy) + 1e-10)
        omega = acos(angle_line) * 180.0 / pi
        k = 2 - 1 / 90 * omega
        if Calculates.dist(p1, p2) < delta:
            return p2
        else:
            theta = atan2(p2[1] - p1[1], p2[0] - p1[0])
            return p1[0] + delta * cos(theta), p1[1] + delta * sin(theta)
