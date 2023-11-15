#Montagnes Russes
import sys, random
random.seed(1) # make the simulation the same each time, easier to debug
import pygame
import pymunk
import pymunk.pygame_util


from geomdl import BSpline

# Create a 3-dimensional B-spline Curve
curve = BSpline.Curve()
# Set degree
curve.degree = 3
# Set control points
curve.ctrlpts = [[10, 5, 10], [10, 20, -30], [40, 10, 25], [-10, 5, 0]]
# Set knot vector
curve.knotvector = [0, 0, 0, 0, 1, 1, 1, 1]
# Set evaluation delta (controls the number of curve points)
curve.delta = 0.05
# Get curve points (the curve will be automatically evaluated)
curve_points = curve.evalpts

def add_rails(space):
    rails = pymunk.Body(body_type = pymunk.Body.STATIC)
    rails.position = (300, 300)
    rail_simple = pymunk.Segment(rails, (-150, 0), (255, 0), 5)
    rail_simple.friction = 1
    
    space.add(rails, rail_simple)
    return rail_simple

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Maybe an Attraction")
    clock = pygame.time.Clock()

    space = pymunk.Space() 
    space.gravity = (0.0, 900.0)

    add_rails(space)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        space.step(1/50.0) 

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    sys.exit(main())