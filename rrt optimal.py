import math, sys, pygame, random
from math import *
from pygame import *



class Node(object):
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent



XDIM = 720
YDIM = 500
windowSize = [XDIM, YDIM]
delta = 10.0
GAME_LEVEL = 1
GOAL_RADIUS = 10
MIN_DISTANCE_TO_ADD = 1.0
NUMNODES = 5000
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 255, 0
green = 0, 0, 255
cyan = 0, 180, 105

count = 0
rectObs = []


def dist(p1, p2):  # distance between two points
    return sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))


def point_circle_collision(p1, p2, radius):
    distance = dist(p1, p2)
    if (distance <= radius):
        return True
    return False


def step_from_to(p1, p2):
    Vbx = p2[0] - p1[0]
    Vby = p2[1] - p1[1]
    Vcx = goalPoint.point[0] - p1[0]
    Vcy = goalPoint.point[1] - p1[1]
    angle_line = (Vbx * Vcx + Vby * Vcy) / sqrt((Vbx * Vbx + Vby * Vby) * (Vcx * Vcx + Vcy * Vcy) + 1e-10)
    omega = acos(angle_line) * 180.0 / pi
    k = 2 - 1 / 90 * omega
    if dist(p1, p2) < delta:
        return p2

    else:
        theta = atan2(p2[1] - p1[1], p2[0] - p1[0])
        return p1[0] + k * delta * cos(theta),  p1[1] + k * delta * sin(theta)


def collides(p):  # check if point collides with the obstacle
    for rect in rectObs:
        if rect.collidepoint(p) == True:
            return True
    return False


def get_random_clear():
    while True:
        p = random.random() * XDIM, random.random() * YDIM
        noCollision = collides(p)
        if noCollision == False:
            return p


def init_obstacles(configNum):  # initialized the obstacle
    global rectObs
    rectObs = []
    print("config " + str(configNum))
    if (configNum == 0):
        rectObs.append(pygame.Rect((XDIM / 2.0 - 50, YDIM / 2.0 - 100), (100, 200)))
    if (configNum == 1):
        rectObs.append(pygame.Rect((100, 50), (200, 150)))
        rectObs.append(pygame.Rect((400, 200), (200, 100)))
    if (configNum == 2):
        rectObs.append(pygame.Rect((100, 50), (200, 150)))
    if (configNum == 3):
        rectObs.append(pygame.Rect((100, 50), (200, 150)))

    for rect in rectObs:
        pygame.draw.rect(screen, black, rect)


def reset():
    global count
    screen.fill(white)
    init_obstacles(GAME_LEVEL)
    count = 0

###############
def pathopti(q1,q2,q3):   #q1 randomselectionnode(keypoints) q2 q1.parent q3 q1.child
    while True:
        pa=0.2
        pb=0.5 #pa,pb????
        p=random.random()
        if p<pa:
            a = pathopti_a(q1,q2,q3)
        elif p>pb:
            a = pathopti_b(q1,q2,q3)
        else:
            a = pathopti_c(q1,q2,q3)
        return a

def pathopti_a(q1,q2,q3):
    global length
    s = get_random_clear()
    if collide_optia(s)==True:
        q=s
    length_old=dist(q1,q2)+dist(q1,q3)
    length_new=dist(q,q2)+dist(q,q3)
    if length_new<length_old:
            q2=q
            length=length-length_old+length_new
            return q2,length

def pathopti_b(q1,q2,q3):
    global length
    s = get_random_clear()
    o=[0]*2
    o[0]=(q1[0]+q3[0])/2
    o[1]=(q1[1]+q3[1])/2
    if dist(o,s)<=dist(o,q2):
        q=s
    length_old = dist(q1, q2) + dist(q1, q3)
    length_new = dist(q, q2) + dist(q, q3)
    if length_new < length_old:
            q2 = q
            length = length - length_old + length_new
            return q2, length
def pathopti_c(q1,q2,q3):
    global length
    r=1
    s=get_random_clear()
    if dist(s,q2)<=r:
        q=s
    while True:
        length_old = dist(q1,q2) + dist(q1,q3)
        length_new = dist(q,q2) + dist(q,q3)
    if length_new < length_old:
            q2 = q
            length = length - length_old + length_new
            return q2, length
global rect_opti
def collide_optia(p):  # check if point collides with the obstacle
    for rect in rect_opti:
        if rect.collidepoint(p) == True:
            return True
    return False

def opti_recta(q1,q2,q3):
    w=max(abs(q1[0]-q2[0]),abs(q1[0]-q3[0]),abs(q2[0]-q3[0]))
    h=max(abs(q1[1]-q2[1]),abs(q1[1]-q3[1]),abs(q2[1]-q3[1]))
    l1=min(q1[0],q2[0],q3[0])
    l2=max(q1[1],q2[1],q3[1])
    rect_opti = []
    rect_opti.append(pygame.Rect((l1,l2), (w,h)))
#############


def main():
    global count

    initPoseSet = False
    initialPoint = Node(None, None)
    goalPoseSet = False
    global goalPoint
    goalPoint = Node(None, None)
    currentState = 'init'

    nodes = []
    reset()

    while True:
        if currentState == 'init':
            print('goal point not yet set')
            pygame.display.set_caption('Select Starting Point and then Goal Point')
            fpsClock.tick(10)
        elif currentState == 'goalFound':
            currNode = goalNode.parent
            pygame.display.set_caption('Goal Reached')
            print('Goal Reached')
            break

            while currNode.parent != None:
                pygame.draw.line(screen, red, currNode.point, currNode.parent.point)
                currNode = currNode.parent
            optimizePhase = True
        elif currentState == 'optimize':
            fpsClock.tick(0.5)
            pass
        elif currentState == 'buildTree':
            count = count + 1
            pygame.display.set_caption('Performing RRT')
            if count < NUMNODES:
                foundNext = False
                while foundNext == False:
                    rand = get_random_clear()
                    parentNode = nodes[0]
                    for p in nodes:
                        if dist(p.point, rand) <= dist(parentNode.point, rand):
                            newPoint = step_from_to(p.point, rand)
                            if collides(newPoint) == False:
                                parentNode = p
                                foundNext = True

                newnode = step_from_to(parentNode.point, rand)
                nodes.append(Node(newnode, parentNode))
                pygame.draw.line(screen, cyan, parentNode.point, newnode)

                if point_circle_collision(newnode, goalPoint.point, GOAL_RADIUS):
                    currentState = 'goalFound'

                    goalNode = nodes[len(nodes) - 1]


            else:
                print("Ran out of nodes... :(")
                return;

        # handle events
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Exiting")
            if e.type == MOUSEBUTTONDOWN:
                print('mouse down')
                if currentState == 'init':
                    if initPoseSet == False:
                        nodes = []
                        if collides(e.pos) == False:
                            print('initiale point set: ' + str(e.pos))

                            initialPoint = Node(e.pos, None)
                            nodes.append(initialPoint)  # Start in the center
                            initPoseSet = True
                            pygame.draw.circle(screen, red, initialPoint.point, GOAL_RADIUS)
                    elif goalPoseSet == False:
                        print('goal point set: ' + str(e.pos))
                        if collides(e.pos) == False:
                            goalPoint = Node(e.pos, None)
                            goalPoseSet = True
                            pygame.draw.circle(screen, green, goalPoint.point, GOAL_RADIUS)
                            currentState = 'buildTree'
                else:
                    currentState = 'init'
                    initPoseSet = False
                    goalPoseSet = False
                    reset()

        pygame.display.update()
        fpsClock.tick(10000)
        
#####################
        global length #????
        for i in range(0,len(nodes)-1):
            q1 = nodes[i].parent
            q3 = nodes[i + 1]
            q2,L = pathopti(q1,nodes[i],q3)
            print (q1[0])
            nodes[i] = q2

######################
if __name__ == '__main__':
    main()


        
