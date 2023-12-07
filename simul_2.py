import CoolProp.CoolProp as cp
import numpy as np
from matplotlib import pyplot as plt

def p_inlet(t, p_i_fcv, aprr):
    return p_i_fcv+(aprr/60)*t*1e6
# p_i_fcv : pressure in fuel cell vehicle
# aprr : average pressure rate ramp according to SAE J 2601 standard
# p_inlet calculates the pressure inlet

def redvalve(p_i, p_o, T_in, kp, rho_o):
    del_p = abs(p_i-p_o)/1e5
    rho_i = cp.PropsSI('Dmass', 'T', T_in, 'P', p_i, 'H2')
    kp = kp
    vdot = (2*del_p/(kp*rho_i))**0.5
    mdot = (vdot/3600)*rho_o
    return mdot
# calculates flow rate

aprr = 2
T_ambient = 25 + 273.15
p_fcv_ini = 20e5
T_ini = T_ambient
V_fcv = 0.35
dm_dt = 0
du_dt_fcv = 0
u_fcv = cp.PropsSI('U', 'P', p_fcv_ini, 'T', T_ini, 'H2')
m_fcv = V_fcv*cp.PropsSI('D', 'P', p_fcv_ini, 'T', T_ini, 'H2')
dt = 0.1
t = 0
p_fcv = p_fcv_ini
cascade = [(300e5,50,2.4), (300e5,50,2.4), (300e5,50,2.4), (300e5,50,2.4), (500e5,50,1.6), (500e5,50,1.6), (500e5,50,1.6), (500e5,50,1.6)]

time_array = np.array([])
mdot_array = np.array([])
rho_array = np.array([])
m_fcv_array = np.array([])
T_fcv_array = np.array([])
pin_array = np.array([])
cascade_track=[]
stage = 0
p_tank = cascade[stage][0]
m_tank = cascade[stage][1]
T_tank = T_ambient
u_tank = cp.PropsSI('U', 'P', p_tank, 'T', T_tank, 'H2')
du_dt_tank = 0
cascade_track = [ [ np.array([]), np.array([]), np.array([]) ] ]

while p_fcv<350e5:
    if dm_dt<=1e-3 :
        cascade_track += [ [ np.array([]), np.array([]), np.array([]) ] ]
        stage += 1
        p_tank = cascade[stage][0]
        m_tank = cascade[stage][1]
        T_tank = T_ambient
        u_tank = cp.PropsSI('U', 'P', p_tank, 'T', T_tank, 'H2')
        du_dt_tank = 0
    u_fcv += du_dt_fcv*dt
    u_tank += du_dt_tank*dt
    m_fcv += dm_dt*dt
    m_tank -= dm_dt*dt
    rho_fcv = m_fcv/V_fcv
    rho_tank = m_tank/cascade[stage][2]
    p_fcv = p_inlet(t, p_fcv_ini, aprr)
    h_tank = cp.PropsSI('H', 'P', p_tank, 'T', T_tank, 'H2' )
    rho_m = cp.PropsSI('D', 'P', p_fcv, 'H', h_tank, 'H2') #insentalpic
    dm_dt = redvalve(p_tank, p_fcv, T_tank, 0.035, rho_m)
    T_i =  -40 + 273.15
    hin = cp.PropsSI('H', 'P', p_fcv, 'T', T_i, 'H2')
    p_tank = cp.PropsSI('P', 'U', u_tank, 'Dmass', rho_tank, 'H2')
    du_dt_fcv = dm_dt*(hin-u_fcv)/m_fcv
    du_dt_tank = dm_dt*(u_tank-h_tank)/m_tank
    T_fcv = cp.PropsSI('T', 'U', u_fcv, 'Dmass', rho_fcv, 'H2')
    T_tank = cp.PropsSI('T', 'U', u_tank, 'Dmass', rho_tank, 'H2')
    time_array = np.append(t, time_array)
    m_fcv_array = np.append(m_fcv, m_fcv_array)
    mdot_array = np.append(dm_dt, mdot_array)
    rho_array = np.append(rho_fcv, rho_array)
    T_fcv_array = np.append(T_fcv, T_fcv_array)
    pin_array = np.append(p_tank, pin_array)
    cascade_track[stage][0] = np.append(p_tank, cascade_track[stage][0])
    cascade_track[stage][1] = np.append(m_tank, cascade_track[stage][0])
    cascade_track[stage][2] = np.append(T_tank, cascade_track[stage][0])
    t += dt