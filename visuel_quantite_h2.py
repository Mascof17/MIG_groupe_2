
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import numpy as np
import math as m


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



nb_passages_bus= 7    #par jour
nb_passages_trains=  0     #par an

reservoirs_bus =  35    #en kg
reservoir_train =  215    #en kg
V_bus = 0
#le compresseur ne fontionne que pour les middle pressure storages
#Je vais donc faire à la main pour les low pressure storage


#REMPLISSAGE DES LP TANKS
def kg_a_la_fin(T, l_m_stock, l_m_LP, v_in, V_LP):
    P_fin = cp.PropsSI('P' ,'T', T,'Dmass', (l_m_stock[0] + l_m_LP[0])/(v_in + V_LP), 'H2')
    mass_LP = cp.PropsSI('Dmass' ,'T', T,'P', P_fin, 'H2') * V_LP
    mass_stock = cp.PropsSI('Dmass' ,'T', T,'P', P_fin, 'H2') * v_in
    return mass_LP, mass_stock 



#étudions désormais une fonction qui suit la quantité d'hydrogène dans le LP tank




def remplissage_LP(T, l_m_LP, l_m_stock, v_in, V_LP):
    dt = 0.00000003
    t = 0
    sum_P=0
    for i in range (len(l_m_LP)):  #on parcourt le stck LP
        for n in range (len(l_m_stock)):   #on parcourt les stocks livrés
            kp = 0.035  #pas important on considérera le chargement inférieur à 15 min
            pressure = cp.PropsSI('P' ,'T', T,'Dmass', l_m_stock[n]/v_in, 'H2')
            while l_m_LP[i]< 50 and l_m_stock[n] > 60 and (pressure - cp.PropsSI('P' ,'T', T,'Dmass', l_m_LP[i]/V_LP, 'H2')) > 0:
                rho = cp.PropsSI('Dmass' ,'T', T, 'P', pressure, 'H2')  
                dm = 0.004
                l_m_LP[i] += dm
                l_m_stock[n] -= dm
                #sum_P += 
                

    return (l_m_stock,l_m_LP)





def remplissage_MP(l_m_stock, l_m_MP, debit_normo =300/3600,volume_stockage = 14.8,T = 293):
    Pression_stockage = [cp.PropsSI('P', 'T', T, 'Dmass',l_m_stock[i]/volume_stockage , 'H2') for i in range (len(l_m_stock))]
    Temps = [0]
    dt =0.1
    debit_massique = debit_normo*cp.PropsSI('Dmass', 'T', T, 'P', Pression_stockage[-1],'H2')
    for i in range (len(l_m_MP)):  #on parcourt le stck LP
        for n in range (len(l_m_stock)): #le procesus dure pendant temps secondes
            #source pour la formule https://www.detendeur.fr/m3h.normo.m3h.p.html
            while l_m_LP[i]< 50 and l_m_stock[n] > 60:
                debit_massique = debit_normo*cp.PropsSI('Dmass', 'T', T, 'P', Pression_stockage[n],'H2')
                if Temps[-1] < 15*60:
                    l_m_stock[n] -= debit_massique*dt  # derivee de la masse vaut -debit, m[i+1]=m[i]-debit*dt
                    l_m_MP[i] += debit_massique*dt
                    Pression_stockage.append(cp.PropsSI('P', 'T', T, 'Dmass', l_m_stock[n]/volume_stockage, 'H2'))
                    Temps.append(Temps[-1]+dt)

    return l_m_stock, l_m_MP






##### ICI IL FAUT RENTRER LES CONDITIONS INITIALES
Minit_LP1 = cp.PropsSI('Dmass' ,'T', T,'P', 50e5, 'H2') * V_LP
l_m_LP = [Minit_LP1]*4


t=np.arange(4*24)    #on découpe la journée en quarts d'heure
stock_tab = np.zeros((4*24, 3))   #tableau des données dans les stockages en f(t)
stock_tab[0] = l_m_stock
LP_tab = np.zeros((4*24, 4)) #idem pour LP
LP_tab[0] = l_m_LP
MP_tab = np.zeros((4*24, 4)) #idem pour MP
MP_tab[0] = l_m_MP

for i in range (1, len(t)):
    if t[i] % 8 == 7:   #####Le truc de TAHA
        l_m_LP, l_m_MP = [l_m_LP[i]-5 for i in range(len(l_m_LP))],  [l_m_MP[i]-3 for i in range(len(l_m_MP))] #remplissage_bus(T, l_m_LP, l_m_MP, V_bus, v_in, V_LP, V_MP, reservoirs_bus)
    elif t[i] % 14 == 0 or t[i] == 0:
        l_m_stock,l_m_LP = remplissage_LP(T, l_m_LP, l_m_stock, v_in, V_LP)
        l_m_stock, l_m_MP = remplissage_MP(l_m_stock, l_m_MP)
    LP_tab[i] = l_m_LP
    MP_tab[i] = l_m_MP
    stock_tab[i] = l_m_stock




#Création des subplots pour visualiser la quantité
fig, axs = plt.subplots(2, 4, figsize=(12, 6))
print(len(t),len(stock_tab))
# Sous-plot 1
axs[0, 0].plot(t, stock_tab[:, 0])
axs[0, 0].set_title('stock1')

# Sous-plot 2
axs[0, 1].plot(t, stock_tab[:, 1])
axs[0, 1].set_title('stock2')

# Sous-plot 3
axs[0, 2].plot(t, stock_tab[:, 2])
axs[0, 2].set_title('stock3')

# Sous-plot 4
axs[0, 3].plot(t, LP_tab[:, 0])
axs[0, 3].set_title('LP1')

# Sous-plot 5
axs[1, 0].plot(t, LP_tab[:, 1])
axs[1, 0].set_title('LP2')

# Sous-plot 6
axs[1, 1].plot(t, LP_tab[:, 2])
axs[1, 1].set_title('LP3')

# Sous-plot 7
axs[1, 2].plot(t, LP_tab[:, 3])
axs[1, 2].set_title('LP4')

# Supprimer le huitième sous-plot (il n'y a pas assez de sous-plots pour 2x4)
fig.delaxes(axs[1, 3])

# Ajuster automatiquement les espacements pour éviter le chevauchement
plt.tight_layout()

# Afficher le graphique
plt.show()