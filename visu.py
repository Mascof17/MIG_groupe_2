
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





#étudions désormais une fonction qui suit la quantité d'hydrogène dans le LP tank 

    #on fait donc des programmes de modélisation de la recharge
def remplissage_LP(l_m_stock, l_m_LP, t, i, debit_normo =500/3600,volume_stockage = 14.8,T = 293):
    print("lp")
    Temps = [0]
    dt =0.1
    debit_massique = debit_normo*cp.PropsSI('Dmass', 'T', T, 'P', 1e5,'H2')
    for k in range (len(l_m_LP)):  #on parcourt le stock LowPressure

        for n in range (len(l_m_stock)): #on parcourt le stock
            pressure = cp.PropsSI('P' ,'T', T,'Dmass', l_m_stock[n]/v_in, 'H2')
                #si on a une delta P favorable, on fait un remplissage naturel

            if pressure - cp.PropsSI('P' ,'T', T,'Dmass', l_m_LP[k]/V_LP, 'H2') > 0:   
                Dmass= (l_m_LP[k] + l_m_stock[n])/(V_LP + v_in)
                l_m_LP[k], l_m_stock[n] = V_LP*cp.PropsSI('Dmass' ,'T', T,'P', cp.PropsSI('P' ,'T', T,'Dmass', Dmass, 'H2'), 'H2'), v_in*cp.PropsSI('Dmass' ,'T', T,'P', cp.PropsSI('P' ,'T', T,'Dmass',Dmass, 'H2'), 'H2')
                Temps.append(Temps[-1]+1)

                #sinon on fait avec le compresseur
            else:
                while l_m_MP[k] < 50 and l_m_stock[n] > 60 : 
                    l_m_stock[n] -= debit_massique*dt  # derivee de la masse vaut -debit, m[i+1]=m[i]-debit*dt
                    l_m_MP[k] += debit_massique*dt
    if i + int(Temps[-1]) < len(t):
        i += int(Temps[-1]) 
    else:
        i = len(t)-1
    return l_m_stock, l_m_MP, i



def remplissage_MP(l_m_stock, l_m_MP, t, i, debit_normo =500/3600,volume_stockage = 14.8,T = 293):   #on définit ce débit à partir de ceux présents dans le commerce https://www.atlascopco.com/fr-fr/compressors/products/gas-compressors/h2y-high-pressure-hydrogen-compressor
    print("mp")
    Temps = [0]   #on veut se limiter à 1/4 d'heure, mais c'est inutile
    dt =0.1
    debit_massique = debit_normo*cp.PropsSI('Dmass', 'T', T, 'P', 1013e2,'H2') #par définition du normomètre cube
    for k in range (len(l_m_MP)):  #on parcourt le stck LP

        for n in range (len(l_m_stock)): #le procesus dure pendant temps secondes
            while l_m_MP[k] < 50 and l_m_stock[n] > 60:
                  #on se limite au pas de temps de 15min
                l_m_stock[n] -= debit_massique*dt  # derivee de la masse vaut -debit, m[i+1]=m[i]-debit*dt
                l_m_MP[k] += debit_massique*dt
                Temps.append(Temps[-1]+dt)
    if i + int(Temps[-1]) < len(t):
        i += int(Temps[-1]) 
    else:
        i = len(t)-1
    return l_m_stock, l_m_MP, i



##### ICI IL FAUT RENTRER LES CONDITIONS INITIALES
Minit_LP1 = cp.PropsSI('Dmass' ,'T', T,'P', 300e5, 'H2') * V_LP
l_m_LP = [Minit_LP1]*4


t=np.arange(3600*6)    #on découpe la journée en quarts d'heure
stock_tab = np.empty((len(t), 3))   #tableau des données dans les stockages en f(t)
stock_tab[0] = l_m_stock
LP_tab = np.empty((len(t), 4)) #idem pour LP
LP_tab[0] = l_m_LP
MP_tab = np.empty((len(t), 4)) #idem pour MP
MP_tab[0] = l_m_MP



i=0
while i < len(t)-1:
    print(i)
    if i % 3600*2 == 3600*1.75:   #####toutes les 2h + 1h45
        l_m_LP, l_m_MP = [l_m_LP[i]-5 for i in range(len(l_m_LP))],  [l_m_MP[i]-3 for i in range(len(l_m_MP))] #remplissage_bus(T, l_m_LP, l_m_MP, V_bus, v_in, V_LP, V_MP, reservoirs_bus)
        i += 1
    elif i % 3600*3 == 0 or i == 0: #Tous les combien de temps on recharge?
        l_m_stock,l_m_LP, i = remplissage_LP(l_m_stock, l_m_LP, t, i)
        l_m_stock, l_m_MP, i = remplissage_MP(l_m_stock, l_m_MP, t, i)
    else:
        i += 1
    
    LP_tab[i] = l_m_LP
    MP_tab[i] = l_m_MP
    stock_tab[i] = l_m_stock

    

LP_tab[i] = l_m_LP
MP_tab[i] = l_m_MP
stock_tab[i] = l_m_stock


t=t/3600#on remet en heures
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
axs[1, 0].plot(t, LP_tab[:, 3])
axs[1, 0].set_title('LP4')

# Sous-plot 6
axs[1, 1].plot(t, MP_tab[:, 0])
axs[1, 1].set_title('MP1')

# Sous-plot 7
axs[1, 2].plot(t, MP_tab[:, 3])
axs[1, 2].set_title('MP4')

# Supprimer le huitième sous-plot (il n'y a pas assez de sous-plots pour 2x4)
fig.delaxes(axs[1, 3])

# Ajuster automatiquement les espacements pour éviter le chevauchement
plt.tight_layout()

# Afficher le graphique
plt.show()

