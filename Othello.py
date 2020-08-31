import pygame

class Board:
    grid:list
    x=1
    y=1
    pressed=False
    directions=[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    def __init__(self):
        self.grid=[]
        f=[]
        for _ in range(8):
            f.append(0)
        for _ in range(8):
            self.grid.append(f.copy())
        self.turn=1
        self.canvas=Draw()
        self.canvas.Grid()
        
    def getTile(self,x,y):
        if 0<=x<=7 and 0<=y<=7:
            return self.grid[y][x]
        else:
            return 7
    def setTile(self,x,y,side):
        self.grid[y][x]=side
        self.canvas.place(x,y,side)
    def printSelf(self):
        for i in self.grid:
            print(i)
    def Update(self):
        if self.pressed:
            self.Place()
            self.pressed=False
        self.canvas.Update()
    def Place(self):
        print(self.ValidPlacement(self.x,self.y))
        self.setTile(self.x,self.y,self.turn)
        self.turn=self.downSide()
    def downSide(self):
        return self.turn%2 +1
    def ValidPlacement(self,x,y):
        potential=0
        out=[]
        if self.getTile(x,y)==0:
            for i in range(8):
                f=self.Scan(x,y,self.directions[i])
                out.append(f)
                potential+=f
        return potential,out.copy()
    def Placement(self,x,y):
        pass                    #in progress
    def Scan(self,x,y,d):
        dx,dy=d
        L=1
        while self.getTile(x+dx*L,y+dy*L)==self.downSide():
            L+=1
        if self.getTile(x+dx*L,y+dy*L)==self.turn:
            return L-1
        else:
            return 0
            


class Draw:
    def __init__(self):
        self.canvas=pygame.display.set_mode((800,800))
    def Clear(self):
        self.canvas.fill((0,0,0))
    def Update(self):
        pygame.display.update()
    def Grid(self):
        col=(100,100,100)
        wid=5
        for i in range(7):
            pygame.draw.line(self.canvas,col,(0,(1+i)*100),(800,(1+i)*100),wid)
        for i in range(7):
            pygame.draw.line(self.canvas,col,((1+i)*100,0),((1+i)*100,800),wid)
    def place(self,x,y,side):
        col=(100,200,100*side)
        pygame.draw.circle(self.canvas,col,(x*100+50,y*100+50),40)



MyBoard=Board()
run=True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==5:
            a=event.__dict__['pos']
            MyBoard.x=int(a[0]/100)
            MyBoard.y=int(a[1]/100)
            MyBoard.pressed=True
    MyBoard.Update()