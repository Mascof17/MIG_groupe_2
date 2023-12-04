
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import numpy as np
import math as m
from masse_variation import f


T=293  #K


n_stockage=3
Pstockage=350e5
l_m_stock=[350]*3
v_in = l_m_stock[0]/cp.PropsSI('Dmass' ,'T', 293,'P', Pstockage, 'H2')


l_m_MP=[50]*4
l_P_MP=[450e5]*4
V_MP = l_m_MP[0]/cp.PropsSI('Dmass' ,'T', 293,'P', l_P_MP, 'H2')


l_m_LP=[50]*4
l_P_LP=[300e5]*4
V_LP = l_m_LP[0]/cp.PropsSI('Dmass' ,'T', T,'P', l_P_LP[0], 'H2')

print(v_in, V_MP)

nb_passages_bus= 7    #par jour
nb_passages_trains=  0     #par an

reservoirs_bus =  35    #en kg
reservoir_train =  215    #en kg
V_bus =
#le compresseur ne fontionne que pour les middle pressure storages
#Je vais donc faire à la main pour les low pressure storage


#REMPLISSAGE DES LP TANKS
def kg_a_la_fin(T, l_m_stock, l_m_LP, v_in, V_LP):
    P_fin = cp.PropsSI('P' ,'T', T,'Dmass', (l_m_stock[0] + l_m_LP[0])/(v_in + V_LP), 'H2')
    mass_LP = cp.PropsSI('Dmass' ,'T', T,'P', P_fin, 'H2') * V_LP
    mass_stock = cp.PropsSI('Dmass' ,'T', T,'P', P_fin, 'H2') * v_in
    return mass_LP, mass_stock 

print(f"c'est{l_m_LP[0]/V_LP}")


#étudions désormais une fonction qui suit la quantité d'hydrogène dans le LP tank

def remplissage_LP(T, l_m_LP, l_m_stock, v_in, V_LP):
    dt = 0.0000003
    t = 0
    sum_P=0
    for i in range (len(l_m_LP)):  #on parcourt le stck LP
        for n in range (len(l_m_stock)):   #on parcourt les stocks livrés
            kp = 0.035  #pas important on considérera le chargement inférieur à 15 min
            pressure = cp.PropsSI('P' ,'T', T,'Dmass', l_m_stock[n]/v_in, 'H2')
            while l_m_LP[i]< 50 and l_m_stock[n] > 60 and pressure - cp.PropsSI('P' ,'T', T,'Dmass', l_m_LP[i]/V_LP, 'H2')) > 0:
                rho = cp.PropsSI('Dmass' ,'T', T, 'P', pressure, 'H2')  
                dm = dt*rho*m.sqrt((cp.PropsSI('P' ,'T', T,'Dmass', l_m_stock[n]/v_in, 'H2') - cp.PropsSI('P' ,'T', T,'Dmass', l_m_LP[i]/V_LP, 'H2'))*2/kp*rho) #formule du débit mais ne fonctionne pas bien
                l_m_LP[i] += dm
                l_m_stock[n] -= dm
                #sum_P += 
                

    return (l_m_stock,l_m_LP)

t=np.linspace(4*24, 4*24)    #on découpe la journée en quarts d'heure
stock_tab = np.zeros(4*24, 3)   #tableau des données dans les stockages en f(t)
stock_tab[0] = l_m_stock
LP_tab = np.zeros(4*24, 4) #idem pour LP
LP_tab[0] = l_m_LP
MP_tab = np.zeros(4*24, 4) #idem pour MP
MP_tab[0] = l_m_MP
for i in range (1, len(t)):
    if t % 8 == 7:
        l_m_stock,l_m_LP, l_m_MP = remplissage_bus(T, l_m_LP, l_m_MP, V_bus, v_in, V_LP, V_MP, reservoirs_bus)
    else:
        l_m_stock,l_m_LP = remplissage_LP(T, l_m_LP, l_m_stock, v_in, V_LP)
        l_m_stock, l_m_MP = l_m_stock - f(l_m_stock, 15*3600), l_m_MP + f(l_m_stock, 15*3600)
    LP_tab[i] = l_m_LP
    MP_tab[i] = l_m_MP
    stock_tab[i] = l_m_stock

#l_m_stock,l_m_LP = remplissage_LP(T, l_m_LP, l_m_stock, v_in, V_LP)

Minit_LP1 = cp.PropsSI('Dmass' ,'T', T,'P', 50e5, 'H2') * V_LP
l_m_LP = [Minit_LP1]*4

print(l_m_LP)

print (f"l_m_stock={remplissage_LP(T, l_m_LP, l_m_stock, v_in, V_LP)[0]} et l_m_LP={remplissage_LP(T, l_m_LP, l_m_stock, v_in, V_LP)[1]}") #attention le débit est bcp trop important


print (f"pour la f de louis:{f(l_m_LP[0], 15*60)} ")



#Création des subplots pour visualiser la quantité
fig, axs = plt.subplots(2, 4, figsize=(12, 6))

# Sous-plot 1
axs[0, 0].plot(t, l_m_stock[::, 0])
axs[0, 0].set_title('Sin(x)')

# Sous-plot 2
axs[0, 1].plot(t, l_m_stock[::, 1])
axs[0, 1].set_title('Cos(x)')

# Sous-plot 3
axs[0, 2].plot(t, l_m_stock[::, 2])
axs[0, 2].set_title('Tan(x)')

# Sous-plot 4
axs[0, 3].plot(t, l_m_LP[::, 0])
axs[0, 3].set_title('x^2')

# Sous-plot 5
axs[1, 0].plot(t, l_m_LP[::, 1])
axs[1, 0].set_title('exp(x)')

# Sous-plot 6
axs[1, 1].plot(t, l_m_LP[::, 2])
axs[1, 1].set_title('log(x+1)')

# Sous-plot 7
axs[1, 2].plot(t, l_m_LP[::, 3])
axs[1, 2].set_title('sqrt(x)')

# Supprimer le huitième sous-plot (il n'y a pas assez de sous-plots pour 2x4)
fig.delaxes(axs[1, 3])

# Ajuster automatiquement les espacements pour éviter le chevauchement
plt.tight_layout()

# Afficher le graphique
plt.show()