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

def f(poids_stockage, masse_train,debit_normo =300/3600,volume_stockage = 14.8,T = 293):
    Pression_stockage = [cp.PropsSI('P', 'T', T, 'Dmass',poids_stockage/volume_stockage , 'H2')/100000]
    Temps = [0]
    masse_train=masse_train
    masse_stockage =[poids_stockage]
    dt =0.1
    while masse_train[-1] < 350 : #le procesus dure pendant temps secondes
        #source pour la formule https://www.detendeur.fr/m3h.normo.m3h.p.html
        debit_massique = debit_normo*cp.PropsSI('Dmass', 'T', T, 'P', Pression_stockage[-1],'H2')
        masse_stockage.append(masse_stockage[-1]-debit_massique*dt)  # derivee de la masse vaut -debit, m[i+1]=m[i]-debit*dt
        masse_train.append(masse_train[-1] + debit_massique*dt)
        Pression_stockage.append(cp.PropsSI('P', 'T', T, 'Dmass', masse_stockage[-1]/volume_stockage, 'H2')/100000)
        Temps.append(Temps[-1]+dt)
    return Temps[-1], debit_massique




# -

print(f(350,[60]))


