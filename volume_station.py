import numpy as np
from scipy.optimize import fsolve

# Définir la fonction mise à jour
def equation(x):
    return (1000*10**5 + 0.0244*0.1*(10**3*16)**2)*(1/(10**3*16) - 0.0266*10**(-3)) - (350*10**5 + (0.0244*0.1*x**2)/(((16*10**(3))**2)*(x+1.6)**2))*(((x+1.6)/(x*16*10**(3))) - 0.0266*10**(-3))

# Initialiser une supposition pour le zéro
initial_guess = 1.0

# Utiliser fsolve pour trouver le zéro
zero = fsolve(equation, initial_guess)

print("Zéro de la fonction:", zero)
