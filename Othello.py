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
        self.cannotPlace=0
        self.canvas=Draw()
        self.canvas.Grid()
        self.setTile(3,4,1)
        self.setTile(4,3,1)
        self.setTile(4,4,2)
        self.setTile(3,3,2)
        
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
        
        if self.turn==2 and self.cannotPlace<2:
            self.cannotPlace=0
            f=self.Search(2)
            if f[0]==0:
                print("opponent cannot place")
                self.cannotPlace+=1
            else:
                self.Placement(f[2],f[3],2,f)
            f=self.Search(1)
            if f[0]==0:
                print("you cannot place")
                self.cannotPlace+=1
            else:
                self.turn=self.turn%2+1
            f=self.Count()
            print("{} empty, {} green, {} blue".format(f[0],f[1],f[2]))
        if self.cannotPlace==2:
            self.cannotPlace=3
            f=self.Count()
            if f[1]<f[2]:
                print("you lose")
            else:
                if f[1]==f[2]:
                    print("draw")
                else:
                    print("you win")

        # if self.turn==1:
        #     f=self.Search(1)
        #     self.Placement(f[2],f[3],1,f)
        #     self.turn=self.turn%2+1
        if self.pressed and self.turn==1:
            if self.Placement(self.x,self.y,1):
                self.turn=self.turn%2+1
            self.pressed=False
        self.canvas.Update()
    def ValidPlacement(self,x,y,side):
        potential=0
        out=[]
        if self.getTile(x,y)==0:
            for i in range(8):
                f=self.Scan(x,y,self.directions[i],side)
                out.append(f)
                potential+=f
        return potential,out.copy(),x,y
    def Placement(self,x,y,side,scan=None):
        if scan==None:
            scan=self.ValidPlacement(x,y,side)
        if scan[0]>0:
            self.setTile(x,y,side)
            for i in range(8):
                self.ScannotPlace(x,y,self.directions[i],scan[1][i],side)
            return True
        else:
            return False
    def Scan(self,x,y,d,side):
        dx,dy=d
        L=1
        while self.getTile(x+dx*L,y+dy*L)==side%2+1:
            L+=1
        if self.getTile(x+dx*L,y+dy*L)==side:
            return L-1
        else:
            return 0
    def ScannotPlace(self,x,y,d,L,side):
        if L>0:
            dx,dy=d
            for i in range(L):
                self.setTile(x+dx*(i+1),y+dy*(i+1),side)
    def Search(self,side):
        a=0,0,0,0
        for iy in range(8):
            for ix in range(8):
                b=self.ValidPlacement(ix,iy,side)
                if b[0]>a[0]:
                    a=b
        return a
    def Count(self):
        out=[0,0,0]
        for iy in range(8):
            for ix in range(8):
                out[self.getTile(ix,iy)]+=1
        return out



            


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
    pygame.time.delay(300)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==5:
            a=event.__dict__['pos']
            MyBoard.x=int(a[0]/100)
            MyBoard.y=int(a[1]/100)
            MyBoard.pressed=True
    MyBoard.Update()