
import sys, pygame, math

class Node():
  def __init__(self,pos,fixed=False,color=(255,255,255),radius=5,w=5):
    self.pos=pos
    self.prev_pos=pos
    self.fixed=fixed
    self.color=color
    self.radius=radius
    self.w=w
    self.clicking=False
  def draw(self,screen):
    pygame.draw.circle(screen, self.color, self.pos, self.radius, self.w)
  def distance(self,pos):
    return math.sqrt((self.pos[0]-pos[0])**2+(self.pos[1]-pos[1])**2)
  def updatePos(self,pos,ignorePrev=False,ignoreFixed=False):
    if not self.fixed or ignoreFixed:
        if not ignorePrev:
            self.prev_pos=self.pos
        self.pos=pos

class Link():
  def __init__(self,a,b,color=(255,255,255),w=2):
    self.a=a #a is a node
    self.b=b
    self.color=color
    self.w=w
    x=self.a.pos[0]-self.b.pos[0]
    y=self.a.pos[1]-self.b.pos[1]
    self.length=math.sqrt(x*x+y*y)
  
  def draw(self,screen):
    pygame.draw.line(screen, self.color, self.a.pos, self.b.pos, self.w)
  def center(self):
    x=(self.a.pos[0]+self.b.pos[0])/2
    y=(self.a.pos[1]+self.b.pos[1])/2
    return (x,y)
  def direction(self):
    x=self.a.pos[0]-self.b.pos[0]
    y=self.a.pos[1]-self.b.pos[1]
    norm=math.sqrt(x*x+y*y)
    return (x/norm,y/norm)
  def updateKeepingLength(self):
      if not self.a.fixed:
        newPos=(self.center()[0]+self.direction()[0]*self.length/2,
                self.center()[1]+self.direction()[1]*self.length/2)
        self.a.updatePos(newPos,True)
      if not self.b.fixed:
        newPos=(self.center()[0]-self.direction()[0]*self.length/2,
                self.center()[1]-self.direction()[1]*self.length/2)
        self.b.updatePos(newPos,True)

pygame.init()

size = width, height = 640, 480

screen = pygame.display.set_mode(size)

points=[]
links=[]
FPS=30
isSimulating=False
creatingSequence=False
clickedAPoint=False
distCreateNew=20
LEFT = 1
RIGHT = 3
gravity=50
iter=10
getTicksLastFrame=pygame.time.get_ticks()
while 1:
    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: 
                isSimulating=True

        if not isSimulating:
            if not creatingSequence:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:                    
                    pos = pygame.mouse.get_pos() 
                    #newPoint=Node(pos,fixed=False)                    
                    #if not clicking a point...  
                    for p in points:
                        if p.distance(pos)<=2*p.radius:
                            clickedAPoint=True
                            lastPoint=p
                            creatingSequence=True
                    if not clickedAPoint:
                        lastPoint=Node(pos,fixed=False)
                        points.append(lastPoint)
                        creatingSequence=True
                    clickedAPoint=False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                    pos = pygame.mouse.get_pos() 
                    for p in points:
                        if p.distance(pos)<=p.radius:
                            p.color=(255,0,0)
                            p.fixed=True                    
                
            if creatingSequence:
                if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                    creatingSequence=False
                    pos = pygame.mouse.get_pos()            
                    newPoint=Node(pos,fixed=False)
                    points.append(newPoint)
                    links.append(Link(lastPoint,newPoint))
                    lastPoint=newPoint

                else:
                    #check distance from last point
                    pos = pygame.mouse.get_pos()
                    if lastPoint.distance(pos)>distCreateNew:
                        newPoint=Node(pos,fixed=False)
                        points.append(newPoint)
                        links.append(Link(lastPoint,newPoint))
                        lastPoint=newPoint
     
        #simulation
    if isSimulating:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            pos = pygame.mouse.get_pos() 
            for p in points:
                if p.distance(pos)<=p.radius:                    
                    if p.fixed==False: 
                        p.color=(255,0,0)
                        p.fixed=True 
                    else:
                        p.color=(255,255,255)
                        p.fixed=False 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            pos = pygame.mouse.get_pos() 
            for p in points:
                if p.fixed and p.distance(pos)<=p.radius:                    
                    p.clicking=True
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            for p in points:
                if p.clicking:
                    p.clicking=False

        #if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
        #    if
                

        for p in points:
            if not p.clicking:
                newPos=(p.pos[0]+p.pos[0]-p.prev_pos[0],
                        p.pos[1]+p.pos[1]-p.prev_pos[1]+gravity*deltaTime*deltaTime)
                p.updatePos(newPos)

            else: 
                newPos= pygame.mouse.get_pos() 
                p.updatePos(newPos,ignoreFixed=True)

        for i in range(iter):
            for l in links:
                l.updateKeepingLength()
                
    
    screen.fill((0,0,0))



    for l in links:
        l.draw(screen)
    
    for n in points:
        n.draw(screen)
    


    pygame.display.flip()
    pygame.time.wait(int(1000/FPS))