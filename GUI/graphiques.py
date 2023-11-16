from pylab import *
from matplotlib import *

# exemple de propagation de courbe

def propagagation_sinus():
    ion() # mode interaction on

    x = linspace(0, 3, 100)
    k = 2*pi
    w = 2*pi
    dt = 0.01

    # courbe initiale
    t = 0
    y = cos(k*x - w*t)
    print(type(y))
    line, = plot(x, y) # une reference a la courbe est mise dans line

    # courbe en mouvement
    for i in range(25):
        t = t + dt
        y = cos(k*x + w*t)
        line.set_ydata(y) # modifie les valeurs de y
        draw() # force le dessin de la figure
        pause(0.05)

    ioff() # mode interaction off
    show()

#propagagation_sinus()

    ion() #début animation
    x=linspace(0,tf,len(Courbe))#axe des temps discrétisé comme la liste des vitesses
    t=array([])
    v=array([]) #liste des vitesses initiales
    line, = plot(t, v) # une reference a la courbe est mise dans line
    xlim(-0.5, tf+0.5)
    xlabel('temps')
    ylim(-1,5)
    ylabel('vitesse')
    plt.title("Graphe des vitesses")
    for i in range(len(Courbe)):
        t.append(x[i])
        v.append(Courbe[i])
        line, = plot(t, v)
        line.set_ydata(v)# modifie les valeurs de v
        draw() # force le dessin de la figure
        pause(0.05)
    print(v)
    
    ioff()
    show()
### On veut afficher le graphe en direct, pendant l'animation du wagon.
### Pour cela on modélise la courbe par sa liste des vitesses discrétisée par dt
### et on affiche 


def graphe_vitesse(Courbe,tf):
    ion() #début animation
    t=linspace(0,tf,len(Courbe)) #axe des temps discrétisé comme la liste des vitesses
    v=array([0.0 for i in range(len(Courbe))]) #liste des vitesses initiales
    line, = plot(t, v) # une reference a la courbe est mise dans line
    xlim(-0.5, tf+0.5)
    xlabel('temps')
    ylim(-1,5)
    ylabel('vitesse')
    plt.title("Graphe des vitesses")
    for i in range(len(Courbe)):
        v[i]=Courbe[i]
        line.set_xdata(t[:i])
        line.set_ydata(v[:i]) # modifie les valeurs de v
        draw() # force le dessin de la figure
        pause(0.05)
    print(v)
    
    ioff()
    show()

graphe_vitesse([0.02*x**4-x**2+3*x for x in linspace(0,5,50)],5)


    

