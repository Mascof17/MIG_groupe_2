
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
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

print(v_in, V_MP)

nb_passages_bus= 22     #par jour
nb_passages_trains=  0     #par an

reservoir_bus=  35    #en kg
reservoir_train=  215    #en kg

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
    dt = 0.01
    t = 0
    for i in range (len(l_m_LP)):
        
        for n in range (len(l_m_stock)):
            kp = 0.035
            pressure =cp.PropsSI('P' ,'T', T,'Dmass', l_m_stock[n]/v_in, 'H2')
            while l_m_LP[i]< 50 and l_m_stock[n] > 60:
                print(l_m_stock)
                rho = cp.PropsSI('Dmass' ,'T', T, 'P', pressure, 'H2')
                dm = dt*rho*m.sqrt((cp.PropsSI('P' ,'T', T,'Dmass', l_m_stock[n]/v_in, 'H2') - cp.PropsSI('P' ,'T', T,'Dmass', l_m_LP[i]/V_LP, 'H2'))*2/kp*rho)
                print(dm/(dt*rho))
                l_m_LP[i] += dm
                l_m_stock[n] -= dm
                t += 1
                
    
    return (l_m_stock,l_m_LP)


Minit_LP1 = cp.PropsSI('Dmass' ,'T', T,'P', 50e5, 'H2') * V_LP
l_m_LP=[Minit_LP1]*4

print(l_m_LP)

print (remplissage_LP(T, l_m_LP, l_m_stock, v_in, V_LP)) #attention le débit est bcp trop important






