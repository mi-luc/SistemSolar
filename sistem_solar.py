import numpy as np
import math,random,pygame,sys

pygame.init()
width=1200
height=800
win=pygame.display.set_mode((width,height))
pygame.display.set_caption("Planete")

font = pygame.font.SysFont(None, 15)
##
time=0

'''10'''
factor=1.471e8
zoom=1
G=6.67e-11
N=9000
dt=10000
lista=[]
soften=0
##
class Planet():
    position=np.array([0,0]);
    def __init__(self,mass,x,y,vx,vy,c,u,sun,fact,name):
        self.position=np.array([0,0], dtype = float);
        self.fake_position=np.array([0,0], dtype = float);
        self.mass=mass
        self.position[0]=x*factor
        self.position[1]=y*factor
        self.ax=0.0
        self.ay=0.0
        self.vx=vx
        self.vy=vy
        self.Radius=math.log10(self.mass)+5
        self.T=0
        self.dU=0
        self.U=u
        self.c=c
        self.facts=fact
        self.sun=sun
        self.axc=0
        self.ayc=0
        self.name=name
    def temperature(self):
        self.T=self.U/(self.mass*self.c)
    def get_zero(self):
        self.ax=0.0
        self.ay=0.0
    def get_acc(self,x,y,mass,soft):
        dx=self.position[0]-x
        dy=self.position[1]-y
        invers=(dx**2+dy**2+soft**2)**(-1.5)
        #print(math.sqrt(dx**2+dy**2))
        self.ax-=G*mass*dx*invers
        self.ay-=G*mass*dy*invers
        
    def get_pos(self):
        global zoom
        #EUler
        
        self.vx+=self.axc*dt/2.0
        self.vy+=self.ayc*dt/2.0
        self.temperature()
        self.position[0]+=self.vx*dt
        self.position[1]+=self.vy*dt
        self.fake_position[0]=self.position[0]*zoom
        self.fake_position[1]=self.position[1]*zoom
        #print(self.vx**2+self.vy**2,self.position)
        self.radiate()
        self.collision()
        for item in lista:
            if item is not self:
                self.get_acc(item.position[0],item.position[1],item.mass,soften)
        
        self.vx+=self.ax*dt/2.0
        self.vy+=self.ay*dt/2.0
        
        self.axc=self.ax
        self.ayc=self.ay
        '''
        #Verlet
        self.position[0]+=(self.vx*dt+1/2*self.ax*dt**2)
        self.position[1]+=(self.vy*dt+1/2*self.ay*dt**2)
        
        c_ax=self.ax
        c_ay=self.ay
        for item in lista:
            if item is not self:
                self.get_acc(item.position[0],item.position[1],item.mass,soften)
        self.vx+=1/2*(c_ax+self.ax)*dt
        self.vy+=1/2*(c_ay+self.ay)*dt
        
        self.fake_position[0]=self.position[0]*zoom
        self.fake_position[1]=self.position[1]*zoom
        '''
    def radiate(self):
        if self.sun==1:
            self.U+=1000000000000000000000000000*dt
        else:
            self.U+=math.log10(self.mass/100)*dt
        if self.U>0:
            if dt>0:    
                self.U-=(self.T*self.facts*dt)**4 
                self.dU=(self.T*self.facts*dt)**4 
            else:
                self.U+=(self.T*self.facts*dt)**4 
                self.dU=-(self.T*self.facts*dt)**4 
        else:
            self.dU=0
        if self.U<0:
            self.U=0
        for item in lista:
            if item is not self:    
                dx=self.position[0]-item.position[0]
                dy= self.position[1]-item.position[1]
                self.U+=item.U/(dx**2+dy**2)
        
    def collision(self):
        for item in lista:
            if item is not self:
                dx=self.position[0]-item.position[0]
                dy= self.position[1]-item.position[1]
                d=math.sqrt((dx**2+dy**2))
                if item.Radius>d or self.Radius>d:
                    heat=1/2*(self.mass*item.mass)/(self.mass+item.mass)*((self.vx-item.vx)**2+(self.vy-item.vy)**2)
                    print(str(heat)+"H")
                    if item.mass>=self.mass:
                        item.vx=(item.mass*item.vx+self.mass*self.vx)/(self.mass+item.mass)
                        item.vy=(item.mass*item.vy+self.mass*self.vy)/(self.mass+item.mass)
                        item.c=(item.c*item.mass+self.c*self.mass)/(self.mass+item.mass)
                        item.facts=(item.facts*item.mass+self.facts*self.mass)/(self.mass+item.mass)
                        
                        item.mass+=self.mass
                        item.Radius=item.mass**(1/3)*0.5+2
                        item.U+=self.U
                        item.U+=heat
                        lista.remove(self)
                    else:
                        self.vx=(item.mass*item.vx+self.mass*self.vx)/(self.mass+item.mass)
                        self.vy=(item.mass*item.vy+self.mass*self.vy)/(self.mass+item.mass)
                        self.c=(item.c*item.mass+self.c*self.mass)/(self.mass+item.mass)
                        self.facts=(item.facts*item.mass+self.facts*self.mass)/(self.mass+item.mass)
                        self.mass+=item.mass
                        self.Radius=self.mass**(1/3)*0.5+2
                        self.U+=item.U
                        self.U+=heat
                        lista.remove(item)
    def show(self,win):
        masa=self.mass
        T=self.T
        c=self.c
        dU=self.dU
        U=self.U
        masa=round(masa, 2)
        T=round(T, 2)
        c=round(c, 2)   
        dU=round(dU, 2)
        U=round(U, 2)
        #print(U)
        img1 = font.render('Masa: '+str(masa), True, (250,250,250))
        img2 = font.render('T: '+str(T)+' K', True, (250,250,250))
        img3 = font.render('c: '+str(c)+' J/kg*K', True, (250,250,250))
        img4 = font.render('dU: '+str(dU)+' J', True, (250,250,250))
        img5 = font.render('U: '+str(U)+' J', True, (250,250,250))
        img6 = font.render(self.name, True, (250,250,250))
        win.blit(img1, (self.fake_position[0]/factor, self.fake_position[1]/factor+self.Radius*zoom+7))
        win.blit(img2, (self.fake_position[0]/factor, self.fake_position[1]/factor+self.Radius*zoom+17))
        win.blit(img3, (self.fake_position[0]/factor, self.fake_position[1]/factor+self.Radius*zoom+27))
        win.blit(img4, (self.fake_position[0]/factor, self.fake_position[1]/factor+self.Radius*zoom+37))
        win.blit(img5, (self.fake_position[0]/factor, self.fake_position[1]/factor+self.Radius*zoom+47))
        win.blit(img6, (self.fake_position[0]/factor, self.fake_position[1]/factor+self.Radius*zoom+57))
        color=(204, 255, 255)
        if self.T>-150+273.1:
            color=(0, 255, 255)
        if self.T>20+273.1:
            color=(0, 255, 0)
        if self.T>100+273.1:
            color=(255, 255, 153)
        if self.T>300+273.1:
            color=(255, 204, 0)
        if self.T>800+273.1:
            color=(255, 102, 0)
        if self.T>3000+273.1:
            color=(255, 252, 250)
        pygame.draw.circle(win,color,(self.fake_position[0]/factor,self.fake_position[1]/factor),self.Radius*zoom)
        
 
def energy():
    Ec=0.0
    Pot=0.0
    for p in lista:
        Ec+=p.mass*p.vx**2/2.0+p.mass*p.vy**2/2.0
    for p in lista:
        for rest in lista:
         if rest is not p:
            dx=p.position[0]-rest.position[0]
            dy=p.position[1]-rest.position[1]
            Raza=(dx**2+dy**2)**(0.5)
            if Raza<0.01:
                Raza=0.01
            Pot+=G*rest.mass*p.mass/abs(Raza)
    print(Ec-Pot)

lista.append(Planet(1.989e30,0,0,0,0,0.5,0,1,0,'Soare'))
lista.append(Planet(5.972e24,1000,0,0,30280,0.5,0,0,0,'Pamant'))
lista.append(Planet(0.33011e24,-312.726,0,0,-58980,0.5,0,0,0,'Mercur'))
lista.append(Planet(4.8675e24,0,730.6719,-35260,0,0.5,0,0,0,'Venus'))
lista.append(Planet(0.64171e24,0,1405,-26500,0,0.5,0,0,0,'Marte'))
lista.append(Planet(1898.19e24,5037.56,0,0,13720,0.5,0,0,0,'Jupiter'))
lista.append(Planet(102.413e24,0,30234.7,-5500,0,0.5,0,0,0,'Neptun'))

start=True
FPS = 1500
fpsClock = pygame.time.Clock()


lx=1000*factor
ly=0
while start:
   
    if abs(lista[1].vx)<10:
        print(str(lista[1].position[0])+"  "+str(time))
    fpsClock.tick(FPS)
    #print(math.sqrt(lista[1].vx**2+lista[1].vy**2))
    img1 = font.render('dt: '+str(dt), True, (250,250,250))
    img2 = font.render(str(time/31557600)+'years', True, (250,250,250))
    time+=dt
    
    win.fill((0, 0, 20))
    
    pygame.draw.circle(win,(250,0,120),(lx*zoom/factor,ly*zoom/factor),2*zoom)
    win.blit(img1, (20,20))
    win.blit(img2, (30,30))
    keys= pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            start=False
    if keys[pygame.K_q]:
        dt=0.01
    if keys[pygame.K_s]:
        dt=0
    if keys[pygame.K_a]:
        dt=-0.01
    if keys[pygame.K_t]:
        for items in lista:
            items.position[1]+=1000000000
        ly+=1000000000
    if keys[pygame.K_g]:
         for items in lista:
            items.position[1]-=1000000000
         ly-=1000000000
    if keys[pygame.K_f]:
        for items in lista:
            items.position[0]+=1000000000
        lx+=1000000000
    if keys[pygame.K_h]:
        for items in lista:
            items.position[0]-=1000000000
        lx-=1000000000
    if keys[pygame.K_z]:
        zoom*=1.01
    if keys[pygame.K_x]:
        zoom*=0.99
    for item in lista:
        item.get_pos()
        item.show(win)
       
    for item in lista:
        item.get_zero()
    #energy()
    #print(time)
    pygame.display.update() 
    
    
        
pygame.quit()
sys.exit()
