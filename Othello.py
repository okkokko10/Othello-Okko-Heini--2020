import pygame

class Board:
    grid:list
    x=1
    y=1
    pressed=False
    updated=True
    directions=[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    winner=0
    turned=False
    text=False
    def __init__(self,AItypes=(0,1),showPossible=False,showConsequence=False):
        self.showPossible=showPossible
        self.showConsequence=showConsequence
        self.AItype=AItypes
        self.canvas=Draw()
        self.Reset()
    def Reset(self):
        self.grid=[]
        f=[]
        for _ in range(8):
            f.append(0)
        for _ in range(8):
            self.grid.append(f.copy())
        self.setTile(3,4,1)
        self.setTile(4,3,1)
        self.setTile(4,4,2)
        self.setTile(3,3,2)
        self.turn=1
        self.cannotPlace=0
        
        
    def getTile(self,x,y):
        if 0<=x<=7 and 0<=y<=7:
            return self.grid[y][x]
        else:
            return 7
    def setTile(self,x,y,side):
        self.updated=True
        self.grid[y][x]=side
        #self.canvas.place(x,y,side)
    def printSelf(self):
        for i in self.grid:
            print(i)
    def Update(self):
        
        if self.turned:
            if self.text:
                f=self.Count()
                print("{} empty, {} white, {} black".format(f[0],f[1],f[2]))
            self.turned=False
            self.turn=self.turn%2+1
            self.updated=True
        if self.cannotPlace<2:
            f=self.Search(self.turn)
            if f[0]==0:
                if self.text:
                    if self.turn==1:
                        a="white"
                    else:
                        a="black"
                    print(a+" cannot place")
                self.cannotPlace+=1
                self.turned=True
            else:
                self.cannotPlace=0
                if self.AItype[self.turn-1]==1:
                    self.Placement(f[2],f[3],self.turn,f)
                    self.turned=True
                elif self.pressed and self.AItype[self.turn-1]==0:
                    if self.Placement(self.x,self.y,self.turn):
                        self.turned=True
                    self.pressed=False
            
        if self.cannotPlace==2:
            self.cannotPlace=3
            f=self.Count()
            self.updated=True
            if f[1]<f[2]:
                if self.text:
                    print("black wins")
                self.winner=2
            else:
                if f[1]==f[2]:
                    if self.text:
                        print("draw")
                    self.winner=7
                else:
                    if self.text:
                        print("white wins")
                    self.winner=1



        if self.updated:
            self.canvas.Clear()
            self.Count(True)
            self.canvas.Grid(self.winner)
            if self.AItype[self.turn-1]==0 and self.winner==0 and not self.turned:
                self.canvas.place(self.x,self.y,self.turn,2,self.getTile(self.x,self.y))
                if self.showConsequence:
                    self.ScanDraw(self.x,self.y,self.turn)
                if self.showPossible:
                    self.Search(self.turn,True)
            self.canvas.Update()
            self.updated=False
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
                self.ScanPlace(x,y,self.directions[i],scan[1][i],side)
            return True
        else:
            return False
    def ScanDraw(self,x,y,side):
        self.updated=True
        scan=self.ValidPlacement(x,y,side)
        if scan[0]>0:
            for i in range(8):
                if scan[1][i]>0:
                    for k in range(scan[1][i]):
                        self.canvas.place(x+self.directions[i][0]*(k+1),y+self.directions[i][1]*(k+1),side,1,self.getTile(x+self.directions[i][0]*(k+1),y+self.directions[i][1]*(k+1)))

    def Scan(self,x,y,d,side):
        dx,dy=d
        L=1
        while self.getTile(x+dx*L,y+dy*L)==side%2+1:
            L+=1
        if self.getTile(x+dx*L,y+dy*L)==side:
            return L-1
        else:
            return 0
    def ScanPlace(self,x,y,d,L,side):
        if L>0:
            dx,dy=d
            for i in range(L):
                self.setTile(x+dx*(i+1),y+dy*(i+1),side)
    def Search(self,side,showPossible=False):
        a=[(0,0,0,0)]
        m=0
        for iy in range(8):
            for ix in range(8):
                b=self.ValidPlacement(ix,iy,side)
                if b[0]>m:
                    a.clear()
                    m=b[0]
                if b[0]==m:
                    a.append(b)
                if b[0]>0 and showPossible:
                    self.canvas.place(ix,iy,side,3)
        import random
        return random.choice(a)
    def Count(self,redraw=False):
        out=[0,0,0]
        for iy in range(8):
            for ix in range(8):
                a=self.getTile(ix,iy)
                out[a]+=1
                if redraw and a!=0:
                    self.canvas.place(ix,iy,a,0)
        return out


class Draw:
    def __init__(self,size=(600,600)):
        self.dimensions=(8,8)
        self.size=size
        self.margins=(50,50,50,50)
        self.canvas=pygame.display.set_mode((self.size[0]+self.margins[0]+self.margins[2],self.size[1]+self.margins[1]+self.margins[3]))
    def Clear(self):
        self.canvas.fill(self.color(0))
    def Update(self):
        pygame.display.update()
    def color(self,side):
        out=(0,50,0),(200,200,200),(0,0,0)
        return out[side]
    def mix(self,A,B,ratio):
        m = lambda a,b,r : int(a*r + b*(1-r))
        out=[]
        for i in (0,1,2):
            out.append(m(A[i],B[i],ratio))
        return out[0],out[1],out[2]
            
    def Grid(self,side=0):
        if side!=7:
            if side==0:
                col=(100,100,100)
            else:
                col=self.color(side)
            wid=5
            for i in range(9):
                pygame.draw.line(self.canvas,col,(self.margins[0],self.margins[1]+(i)*self.size[1]//self.dimensions[1]),(self.size[0]+self.margins[0],self.margins[1]+(i)*self.size[1]//self.dimensions[1]),wid)
            for i in range(9):
                pygame.draw.line(self.canvas,col,(self.margins[0]+(i)*self.size[0]//self.dimensions[0],self.margins[1]),(self.margins[0]+(i)*self.size[0]//self.dimensions[0],self.size[1]+self.margins[1]),wid)
    def place(self,x,y,side,t,behind=0):
        f=(0.4, 0.2, 0.15,0.1 )[t]
        g=(1,   1,   0.75,0.5 )[t]
        col=self.mix(self.color(side),self.color(behind),g)

        s=int(f*self.size[0]/self.dimensions[0])
        pygame.draw.circle(self.canvas,col,(int(self.margins[0]+(x+0.5)*self.size[0]/self.dimensions[0]),int(self.margins[1]+(y+0.5)*self.size[1]/self.dimensions[1])),s)

    def getTile(self,point):
        a=(point[0]-self.margins[0])/self.size[0]*self.dimensions[0]
        b=(point[1]-self.margins[1])/self.size[1]*self.dimensions[1]
        return max(min(int(a),7),0),max(min(int(b),7),0)

def MainLoop(board):
    run=True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==4:
                a=event.__dict__['pos']
                b=board.canvas.getTile(a)
                board.x=b[0]
                board.y=b[1]
                board.updated=True
            if event.type==5 and event.__dict__['button']==1:
                board.pressed=True
            if event.type==2:                   # toggles: f: show valid moves, g: show result, h: AI for white, j: AI for black, k: reset
                #a={'f':0,'g':1,'h':2,'j':3}[]
                a=event.__dict__['unicode']
                if a=='f':
                    board.showPossible=not board.showPossible
                elif a=='g':
                    board.showConsequence=not board.showConsequence
                elif a=='h':
                    board.AItype=(board.AItype[0]+1)%2,board.AItype[1]
                elif a=='j':
                    board.AItype=board.AItype[0],(board.AItype[1]+1)%2
                elif a=='k':
                    board.Reset()
                board.updated=True
        board.Update()


if __name__ == "__main__":
    MyBoard=Board((0,0),1,1)
    MainLoop(MyBoard)