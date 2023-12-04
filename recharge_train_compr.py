
import CoolProp.CoolProp as cp
import matplotlib.pyplot as plt

def f(poids_stockage, masse_train,debit_normo =300/3600,volume_stockage = 14.8,T = 293):
    Pression_stockage = [cp.PropsSI('P', 'T', T, 'Dmass',poids_stockage/volume_stockage , 'H2')/100000]
    Temps = [0]
    masse_stockage =[poids_stockage]
    dt =0.1
    debit_massique = debit_normo*cp.PropsSI('Dmass', 'P', 101300, 'T', T, "H2")
    while masse_train < 350: #le procesus dure pendant temps secondes
 #source pour la formule https://www.detendeur.fr/m3h.normo.m3h.p.html
        masse_train += debit_massique*dt    # derivee de la masse vaut -debit, m[i+1]=m[i]-debit*dt
      #  Pression_stockage.append(cp.PropsSI('P', 'T', T, 'Dmass', masse_stockage[-1]/volume_stockage, 'H2')/100000)
        Temps.append(Temps[-1]+dt)

    return Temps[-1], debit_massique


print(f(350, 60))
