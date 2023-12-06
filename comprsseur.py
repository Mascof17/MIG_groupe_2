import CoolProp.CoolProp as cp
import matplotlib.pyplot as plt
T = 293
debit_normo =300/3600 #300Nm^3/h  donc 300/3600 par seconde source: https://fr.wikipedia.org/wiki/Compresseur_d%27hydrog%C3%A8ne
P= 300*101300 #pression initialement à 300 bars
p_in=cp.PropsSI('Dmass' ,'T', T,'P', P , 'H2')
print(p_in)
V= 14.8 #volume dans le reservoir 
X =[]
X.append(p_in)
Temps = [0]
dt=0.1
print(P)
Pression = [P/101300]
P_out = [50] #Pression dans le reservoir de Casacade
V_out = 1.7 #volume en metre cube dans le reservoir   de cascade 2.4 LP, 1.7 MP
masse_volumique_out = [cp.PropsSI('Dmass' ,'T', T,'P', P_out[0]*101300 , 'H2')]
masse_out = [masse_volumique_out[0]*V_out]

while P_out[-1]<500 : #on s'arrete à MP a 500bars
    debit_volumique = (debit_normo*1.01325*(T+273))/(Pression[-1]*273) #source pour la formule https://www.detendeur.fr/m3h.normo.m3h.p.html
    debit_massique = X[-1]*debit_volumique
    X.append(X[-1]-debit_massique*dt/V)  # derivee de la masse vaut -debit, m[i+1]=m[i]-debit*dt
    P= cp.PropsSI('P', 'T', T, 'Dmass', X[-1], 'H2')
    masse_out.append(masse_out[-1]+debit_massique*dt)
    masse_volumique_out.append(masse_out[-1]/V_out)
    P_out.append((cp.PropsSI('P', 'T', T, 'Dmass', masse_volumique_out[-1], 'H2'))/101300)
    Pression.append(P/101300)
    Temps.append(Temps[-1]+dt)
    
"""
print(Temps[-1])
print((X[0]-X[-1])*V)
plt.plot(Temps,Pression)
plt.xlabel('temps')
plt.ylabel(" pression d'H2 dans le stockage")
plt.show()
"""
Masse=[]
for i in range(len(X)):
    Masse.append(V*X[i])
plt.plot(Temps,Masse)
plt.xlabel('temps')
plt.ylabel(" Masse d'H2 dans le stockage")
plt.show()

"""
plt.plot(Temps, P_out)
plt.xlabel('temps (en secondes)')
plt.ylabel(" pression d'H2 dans la cascade (en bar)")
plt.show()
"""

plt.plot(Temps,masse_out)
plt.xlabel('temps')
plt.ylabel(" Masse d'H2 dans la cascade")
plt.show()



