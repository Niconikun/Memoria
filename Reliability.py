import math
from decimal import Decimal
from random import Random
import numpy as np
import scipy as sp

'''
The purpose of this code is to define several step functions. These steps allow the calculation of
the reliability curves of subsystems and systems depending on the presence of redundancy in EPS. '''


def draw_(probability_distribution):
    # método de rejection sampling
    member_count = len(probability_distribution)
    step_size = 1.00 / (member_count * 1.00)

    accept = False
    r_value = 0

    while not accept:
        # generate r_temp and use it to determine R:
        random_generator = Random()
        r_temp = random_generator.random()

        bina = math.ceil(r_temp / step_size)
        binned_object = probability_distribution[bina - 1]
        r_value = binned_object['value']
        r_probability = binned_object['probability']

        # now, after we have R (r_value), draw S:
        s = random_generator.random()

        # accept or reject this observation:
        if s <= r_probability:
            accept = True
        else:
            accept = False

    return r_value

## MODEL INPUTS
def dist(EPS_redundancy, x): # Subsystem level realibility inputs Source: Bouwmeeter et al 2022 - Fog 11
    # INPUTS for subsystems in the following sequence ADCS; CDHS; COMMS; STS&DepS and P/L; EPS
    mu = [15.4, 11.5, 13.7, 14.3, 14.3, 9.4]    #Log-normal \mu
    sigma = [10, 8.39, 9.79, 9.21, 9.21, 8.18]  #Log-normal \sigma_1
    theta = [2.6, 8.1, 2.6, 2.7, 2.7, 2.9]      #Gomperts \theta
    nu = [9.1e-5, 0.0167, 8.3e-5, 0.00011, 0.00011, 0.00011]    #Gompertz \nu
    rel = 1

#Subsystem redundancy true is redundant (red) and false (off) is no subsystem redundancy
    #Only analisis case for EPS redundancy, due to its lower reliability over time
    counter: int
    # esto tiene que entregar un número, no un array
    for counter in np.arange(len(mu)):
        if EPS_redundancy and counter == 5:  #Counter ==5 is the position in the input vector for EPS reliability
            rel *= 1 - np.square(
                1 - sp.stats.lognorm.sf(x, sigma[counter], scale=np.exp(mu[counter])) * sp.stats.gompertz.sf(x, nu[
                    counter] / theta[counter], scale=theta[counter]))
        else: #No redundancy
            rel *= sp.stats.lognorm.sf(x, sigma[counter], scale=np.exp(mu[counter])) * sp.stats.gompertz.sf(x, nu[
                counter] / theta[counter], scale=theta[counter])
    return rel


#Determines the minimum number of operational satellites required to stay at ... 
def rel_builder(R_elem, ctd_sat_min):
    R_s = 1
    for counter in np.arange(2 ** len(R_elem)):
        rel = 1
        bina = bin(counter)[2:].zfill(len(R_elem))
        if bina.count('1') <= len(R_elem) - ctd_sat_min:
            continue
        else:
            for k in np.arange(len(bina)):
                if bina[k] != '0':
                    rel *= 1 - R_elem[k]
                else:
                    rel *= R_elem[k]
            R_s -= rel
    return R_s #R_S stands for DSM reliability @Change consistency in code 


def rel_creator(t, relaunch_rate, mission_time, sat_ctd_ini, sat_ctd_rel, EPS_redundancy):
    Ans = np.ones(sat_ctd_ini) * dist(EPS_redundancy, t)
    x = np.linspace(0, mission_time, (mission_time * relaunch_rate), dtype=str)

    for a in x:
        if Decimal(str(t)) >= Decimal(a) > Decimal('0'):
            Ans = np.append(Ans, np.ones(sat_ctd_rel) * dist(EPS_redundancy, t - float(a)))
        else:
            continue
    return Ans.tolist()


def no_phase(EPS_redundancy, ctd_sat_min, ctd_sat_ini, Mission_time):
    x = np.linspace(0, Mission_time, Mission_time * 365)

    R_sys = []
    for t in x:
        R_elem = np.ones(ctd_sat_ini) * dist(EPS_redundancy, t)
        R_sys.append(rel_builder(R_elem, ctd_sat_min))

    return x, R_sys


def Reliability(EPS_redundancy, ctd_sat_min, ctd_sat_ini, DSM_relaunch_amount, relaunch_rate, Mission_time):

    year_to_day = 365
    x = np.linspace(0, Mission_time, Mission_time * year_to_day)

    R_sys = []
    for t in x:
        R_elem = rel_creator(t, relaunch_rate, Mission_time, ctd_sat_ini, DSM_relaunch_amount, EPS_redundancy)
        R_sys.append(rel_builder(R_elem, ctd_sat_min))

    return x, R_sys

