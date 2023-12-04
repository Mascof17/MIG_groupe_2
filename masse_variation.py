# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import CoolProp.CoolProp as cp
import matplotlib.pyplot as plt

def f(poids_stockage, temps,debit_normo =300/3600,volume_stockage = 14.8,T = 293):
    Pression_stockage = cp.PropsSI('P', 'T', T, 'Dmass',poids_stockage/volume_stockage , 'H2')/100000
    Temps = [0]
    masse_stockage =[poids_stockage]
    while Temps[-1]<temps : #le procesus dure pendant temps secondes
        debit_volumique = (debit_normo*1.01325*(T+273))/(Pression_stockage[-1]*273) #source pour la formule https://www.detendeur.fr/m3h.normo.m3h.p.html
        debit_massique = masse_stockage[-1]*debit_volumique/volume_stockage
        masse_stockage.append(masse_stockage[-1]-debit_massique*dt)  # derivee de la masse vaut -debit, m[i+1]=m[i]-debit*dt
        Pression_stockage.append(cp.PropsSI('P', 'T', T, 'Dmass', masse_stockage[-1]/volume_stockage, 'H2')/100000)
        Temps.append(Temps[-1]+dt)
    return masse_stockage[0]-masse_stockage[-1]



# -

f(30,30)


