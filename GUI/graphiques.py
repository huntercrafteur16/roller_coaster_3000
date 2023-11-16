from pylab import *
from matplotlib import *
 
### On veut afficher le graphe en direct, pendant l'animation du wagon.
### Pour cela on modélise la courbe par sa liste des vitesses discrétisée par dt
### et on affiche 


def graphe_vitesse(List_speeds,tf):
    ion() # début animation
    t=linspace(0,tf,len(List_speeds)) # axe des temps discrétisé comme la liste des vitesses
    line, = plot(t, List_speeds) # une reference a la courbe est mise dans line

    xlim(-0.5, tf+0.5)                         
    xlabel('temps')                  
    ylim(-1,5)                          # mise en forme
    ylabel('vitesse')         
    plt.grid()          
    plt.title("Graphe des vitesses")    
    
    for i in range(len(List_speeds)):
        line.set_xdata(t[:i]) # actualise les valeurs de t
        line.set_ydata(List_speeds[:i]) # actualise les valeurs de v
        draw() # force le dessin de la figure
        pause(0.05)
    ioff()
    show()

graphe_vitesse([0.02*x**4-x**2+3*x for x in linspace(0,5,50)],5)


    

