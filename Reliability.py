import math
from decimal import Decimal
from random import Random
import numpy as np
import scipy as sp

'''
The purpose of this code is to define several step functions. These steps allow the calculation of
the reliability curves of subsystems and systems depending on the presence of redundancy in EPS
and the mission strategy selected. This file is not meant to be run, but rather it is called by main.py.

Definition of Functions written

- rejection_sampling: Function used to generate observations from a distribution. It generates a 
random value and checks if it's inside or outside the distribution. The iteration stops until the
variable is inside the distribution. This function is not used in the process.
- Reliability_CubeSat: Function that outputs the reliability of the CubeSat based on the curves
defined by Bouwmeester et al, 2022. It builds the reliability functions of the subsystems defined 
by the author and outputs the reliability of the CubeSat system considering all subsystems in series.
If the user defines the existence of a redundancy in EPS, it will only act the EPS subsystem as parallel.
- DSM_reliability_noutofp: Function that outputs the Reliability of the DSM following an n-out-of-p system.
It calculates all of the possibilities in which the system fails, by using all of binary numbers between 0 and 2^n elements.
This function only works with time in float format and not as an array.
- phased_deployment: Function that, if selected the phased deployment, it asks if the time analyzed passes through a threshhold
where the new batch is launched. If it did, then it add new elements to the systems and their reliability curves. If not, it continues.
- no_phase: Mission strategy where the DSM is not updated or added new batches or generations, regardless of redundancy presence.
- Reliability: Mission strategy where the amount of elements in a DSM is updated or added new batches or generations every certain amount of time.
'''


def rejection_sampling(probability_distribution):
    member_count = len(probability_distribution)
    step_size = 1.00 / (member_count * 1.00)

    accept = False
    r_value = 0

    while not accept:
        # generate r_temp and use it to determine R:
        random_generator = Random()
        r_temporal = random_generator.random()

        random_ceil = math.ceil(r_temporal / step_size)
        binned_object = probability_distribution[random_ceil - 1]
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

def Reliability_CubeSat(EPS_redundancy, Time_years): # Subsystem level realibility inputs Source: Bouwmeeter et al 2022 - Fig 11
    # INPUTS for subsystems in the following collumn sequence ADCS; CDHS; COMMS; STS&DepS and P/L; EPS
    mu = [15.4, 11.5, 13.7, 14.3, 14.3, 9.4]    #Log-normal \mu
    sigma = [10, 8.39, 9.79, 9.21, 9.21, 8.18]  #Log-normal \sigma_1
    theta = [2.6, 8.1, 2.6, 2.7, 2.7, 2.9]      #Gomperts \theta
    nu = [9.1e-5, 0.0167, 8.3e-5, 0.00011, 0.00011, 0.00011]    #Gompertz \nu
    R_CubeSat = 1

#Subsystem redundancy true is redundant (red) and false (off) is no subsystem redundancy
    #Only analisis case for EPS redundancy, due to its lower reliability over time
    counter: int # counter is a variable used for the loop as counter
    for counter in np.arange(len(mu)):
        if EPS_redundancy and counter == 5:  #Counter ==5 is the position in the input vector for EPS reliability
            R_CubeSat *= 1 - np.square(
                1 - sp.stats.lognorm.sf(Time_years, sigma[counter], scale=np.exp(mu[counter])) * sp.stats.gompertz.sf(Time_years, nu[
                    counter] / theta[counter], scale=theta[counter]))
        else: #No redundancy
            R_CubeSat *= sp.stats.lognorm.sf(Time_years, sigma[counter], scale=np.exp(mu[counter])) * sp.stats.gompertz.sf(Time_years, nu[
                counter] / theta[counter], scale=theta[counter])
    return R_CubeSat #outputs the system level reliability curve


def DSM_reliability_noutofp(R_CubeSat, DSM_min_amount):
    R_DSM = 1
    for counter in np.arange(2 ** len(R_CubeSat)): # Defines the amount of possibilities the system could fail
        R_partial = 1
        bina = bin(counter)[2:].zfill(len(R_CubeSat))
        if bina.count('1') <= len(R_CubeSat) - DSM_min_amount:
            continue
        else:
            for k in np.arange(len(bina)): # Calculates and multiplies the probability of each possibility
                if bina[k] != '0':
                    R_partial *= 1 - R_CubeSat[k]
                else:
                    R_partial *= R_CubeSat[k]
            R_DSM -= R_partial
    return R_DSM # Outputs the reliability of the DSM in an instance of time


def phased_deployment(Current_Time, relaunch_rate, mission_time, DSM_initial_amount, DSM_relaunch_amount, EPS_redundancy):
    DSM_Size = np.ones(DSM_initial_amount) * Reliability_CubeSat(EPS_redundancy, Current_Time) #Defines current size of DSM
    Deployment_Dates = np.linspace(0, mission_time, (mission_time * relaunch_rate), dtype=str) # Array that gives the dates for phased deployment

    for a in Deployment_Dates: # if the current time is over the deployment date, it adds new elements to the DSM, else continues
        if Decimal(str(Current_Time)) >= Decimal(a) > Decimal('0'):
            DSM_Size = np.append(DSM_Size, np.ones(DSM_relaunch_amount) * Reliability_CubeSat(EPS_redundancy, Current_Time - float(a)))
        else:
            continue
    return DSM_Size.tolist() # outputs the updated DSM size


def no_phase(EPS_redundancy, DSM_min_amount, DSM_initial_amount, Mission_time):
    Time_years = np.linspace(0, Mission_time, Mission_time * 365) # sets mission time

    R_DSM = []
    for Current_Time in Time_years:
        R_elem = np.ones(DSM_initial_amount) * Reliability_CubeSat(EPS_redundancy, Current_Time) #sets DSM size and cubesats reliabilities
        R_DSM.append(DSM_reliability_noutofp(R_elem, DSM_min_amount)) #gets DSM reliability and appends it on the array

    return Time_years, R_DSM # returns the mission time array and the reliability of the DSM


def Reliability(EPS_redundancy, DSM_min_amount, DSM_initial_amount, DSM_relaunch_amount, relaunch_rate, Mission_time):

    year_to_day = 365
    Time_years = np.linspace(0, Mission_time, Mission_time * year_to_day) # sets mission time

    R_DSM = []
    for Current_Time in Time_years:
        R_elem = phased_deployment(Current_Time, relaunch_rate, Mission_time, DSM_initial_amount, DSM_relaunch_amount, EPS_redundancy) #sets DSM size and cubesats reliabilities, updating it to the current time
        R_DSM.append(DSM_reliability_noutofp(R_elem, DSM_min_amount)) #gets DSM reliability and appends on the array

    return Time_years, R_DSM # returns the mission time array and the reliability of the DSM

