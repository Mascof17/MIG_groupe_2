
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp


n_stockage=3
Pstockage=300
Minit_stockage=350

Pinit_MP1, Minit_MP1=450, 50
Pinit_MP2, Minit_MP2=450, 50
Pinit_MP3, Minit_MP3=450, 50
Pinit_MP4, Minit_MP4=450, 50

Pinit_LP1, Minit_LP1=30, 50
Pinit_LP2, Minit_LP2=300, 50
Pinit_LP3, Minit_LP3 = 300, 50
Pinit_LP4, Minit_LP4 = 300, 50


nb_passages_bus= 22     #par jour
nb_passages_trains=  0     #par an

reservoir_bus=  35    #en kg
reservoir_train=  215    #en kg

#le compresseur ne fontionne que pour les middle pressure storages
#Je vais donc faire à la main pour les low pressure storage





