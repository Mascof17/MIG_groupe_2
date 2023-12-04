import CoolProp.CoolProp as cp
import matplotlib.pyplot as plt
T = 293
R = 8.314
a=0.00244
b=0.0000266
Vcyl=1 # Cylindree du compresseur
n=1 # piston stroke / seconde
efficacite_volumique =1#
P= 300*101300 #pression initialement à 300 bars
p_in=cp.PropsSI('Dmass' ,'T', T,'P', P , 'H2')
print(p_in)
 # KG/METRE Cube masse volumique de l'H2 entrant qui est à 300 bars au debut, on s'arrete de vider à 20 bars
V= 1#volume dans le reservoir 
debit = Vcyl*p_in*efficacite_volumique*n
X =[]
X.append(p_in)
Temps = [0]
dt=0.001
print(P)
Pression = [P/1013]

# +
while P>20*101300: #on s'arrete quand P est à 20 bars
    debit = Vcyl*X[-1]*efficacite_volumique*n
    X.append(X[-1]-debit*dt/V)  # derivee de la masse vaut -debit, m[i+1]=m[i]-debit*dt
    P= cp.PropsSI('P', 'T', T, 'Dmass', X[-1], 'H2')
    Pression.append(P/101300)
    Temps.append(Temps[-1]+dt)
print(Temps[-1])
print((X[0]-X[-1])*V)


# -

plt.plot(Temps,Pression)
plt.xlabel('temps')
plt.ylabel(" pression d'H2 dans le stockage")
plt.show()

Masse=[]
for i in range(len(X)):
    Masse.append(V*X[i])
plt.plot(Temps,Masse)
plt.xlabel('temps')
plt.ylabel(" Masse d'H2 dans le stockage")
plt.show()


