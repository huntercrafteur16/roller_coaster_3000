#Montagnes Russes
import sys, random
random.seed(1) # make the simulation the same each time, easier to debug
import pygame
import pymunk
import pymunk.pygame_util

from geomdl import BSpline

#Copier-coller aide d'internet
rails = BSpline.Curve()# Create a 3-dimensional B-spline Curve
rails.degree = 3# Set degree
rails.ctrlpts = [[10, 5, 10], [10, 20, -30], [40, 10, 25], [-10, 5, 0]]# Set control points
rails.knotvector = [0, 0, 0, 0, 1, 1, 1, 1]# Set knot vector
rails.delta = 0.05# Set evaluation delta (controls the number of curve points)
rails_points = rails.evalpts# Get curve points (the curve will be automatically evaluated)


class Physique():
    def __init__(self,screen):
        self.draw_option = pymunk.pygame_util.DrawOptions(screen)
        self.space = None
        self.new()
    
    def new(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, 200
    #creation d'un objet static + la courbe est decrite par la liste des points bspline
    #Question : comment definir bspline ?
    def add_rails(self,bspline):
        rails = pymunk.Body(body_type = pymunk.Body.STATIC)
        rails.position = (300, 300)
        for i,p in enumerate(bspline[:-1]):
            rails = pymunk.Segment(self.space.static_body,p, bspline[i+1], 1)
            rails.elasticity = 1
            self.space.add(rails)
    
    #Ajouter l'objet à l'espace
    def run(self):
        self.space.debug_draw(self.draw_option)
        self.space.step(0.01)



class Spline():
    def __init__(self,degree=2):
        self.degree=degree
        self.curve = BSpline.Curve()
        self.curve.degree = degree
        
        self.points = []

    def draw(self,points):
        self.curve.ctrlpts = points
        self.curve.knotvector = utilities.generate_knot_vector(self.curve.degree, len(self.curve.ctrlpts))
        #self.curve.vis = VisMPL.VisCurve3D()
        self.points=self.curve.evalpts
        
    def set_degree(self,d):
        self.curve.degree = d
        self.degree=d

class Canvas():
    def __init__(self,screen):
        self.screen = screen
        self.curve = Spline()
        self.physics = Physics(self.screen)
        #self.physics.add_circle(400,700)
        self.ctrl_points=[]
        self.count=0
        self.selected=None
        self.move_point=False
        self.add_mode=0
        
        self.add_button = (20,460,50,20)
        self.del_button = (90,460,50,20)
        self.sel_button = (160,460,50,20)
        self.hide_button = (230,460,50,20)
        self.play_button = (300,460,50,20)
        
        self.edit_button = (20,460,50,20)
        
    def add_points(self,xy):
        self.ctrl_points.append(xy)
    
    def render(self):
        if cfg.edit_mode:
            if cfg.show_points:
                if self.count>=2:
                    pygame.draw.lines(self.screen,(100,100,100),0,self.ctrl_points)
                for i,point in enumerate(self.ctrl_points):
                    if i==0:
                        pygame.draw.circle(self.screen,(0,140,200),point,5)
                    elif i==self.selected:
                        pygame.draw.circle(self.screen,(20,200,80),point,5)
                    else:
                        pygame.draw.circle(self.screen,(140,140,140),point,5)
            if self.count>=self.curve.degree+1:
                pygame.draw.lines(self.screen,cfg.color,0,self.curve.points,width=cfg.width)
        self.button_render()

def move(self,xy):
        if self.move_point:
            self.ctrl_points.pop(self.selected)
            self.ctrl_points.insert(self.selected,xy)
            if self.count>=self.curve.degree+1:
                self.curve.draw(self.ctrl_points)
                
            return True
    def simulate(self):
        self.physics.run()

if __name__=="__main__":
    screen = pygame.display.set_mode((500,500))
    canvas = Canvas(screen)
    def update():
        screen.fill(cfg.fill)
        canvas.simulate()
        canvas.render()
        pygame.display.update()
                    
    update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        update()
    