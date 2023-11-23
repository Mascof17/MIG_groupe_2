import numpy as np
import scipy.integrate as integr



Cx=1.05
m = (120 + 90*(int(300/19)))*1000 #masse 120 pour la loco, 90T par wagon de 19m de long, le train fais 300m de long
S= 4.280*3.150 #surface max d'un train qui peut circuler
g=9.81
a=30/(3.6*60) #acceleration de 0 à 30km/h en 1 minute
T=30/(3.6*a) #aT=30km/h, a T l'accelaration finie
Crr=0.001 #frotement rail roue
p = 1 # masse volumique de l'air

# +
def f(t):
    return (m*a + 0.5*p*S*Cx*((a*t)*(a*t)) + Crr*m*g)*a*t

P,e =integr.quad(f, 0, T)
# -

print(P)



