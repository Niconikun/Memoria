import numpy as np
import scipy as sp
from matplotlib import pyplot as plt

mu = [15.4, 11.5, 13.7, 14.3, 14.3, 9.4]    #Log-normal \mu
sigma = [10, 8.39, 9.79, 9.21, 9.21, 8.18]  #Log-normal \sigma_1
theta = [2.6, 8.1, 2.6, 2.7, 2.7, 2.9]      #Gomperts \theta
nu = [9.1e-5, 0.0167, 8.3e-5, 0.00011, 0.00011, 0.00011]    #Gompertz \nu
R_simulation = []
iteration = ''
graph_labels = []
year_to_month = 12

Mission_time = 8
Time_months = np.arange(0, Mission_time * year_to_month + 1)

DSM_initial_amount = [2, 2]
EPS_redundancy = [False, False]
Phase_Deployment = [True, True]
relaunch_rate = [30, 30]
DSM_relaunch_amount = [1, 1]
Retire_sat = [False, True]

def Reliability_CubeSat(EPS_redundancy, Time_months): # Subsystem level realibility inputs Source: Bouwmeester et al 2022 - Fig 11
    R_CubeSat = 1
    Time_shift = 7 / 365
#Subsystem redundancy true is redundant (red) and false (off) is no subsystem redundancy
    #Only analisis case for EPS redundancy, due to its lower reliability over time
    counter: int # counter is a variable used for the loop as counter
    for counter in np.arange(len(mu)):
        if EPS_redundancy and counter == 5:  #Counter ==5 is the position in the input vector for EPS reliability
            R_CubeSat *= 1 - np.square(
                1 - sp.stats.lognorm.sf(Time_months + Time_shift, sigma[counter], scale=np.exp(mu[counter])) * sp.stats.gompertz.sf(Time_months + Time_shift, nu[
                    counter] / theta[counter], scale=theta[counter]))
        else: #No redundancy
            R_CubeSat *= sp.stats.lognorm.sf(Time_months + Time_shift, sigma[counter], scale=np.exp(mu[counter])) * sp.stats.gompertz.sf(Time_months + Time_shift, nu[
                counter] / theta[counter], scale=theta[counter])
    return R_CubeSat #outputs the system level reliability curve

simulation_results = []
analysis_results = []
amount_results = []

for iteration in np.arange(len(DSM_initial_amount)):
    R_DSM_6m, R_DSM_12m, R_DSM_18m, R_DSM_24m, R_DSM_3y, R_DSM_4y, R_DSM_5y, R_DSM_6y, R_DSM_7y, R_DSM_8y = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    sc_6m, sc_12m, sc_18m, sc_24m, sc_3y, sc_4y, sc_5y, sc_6y, sc_7y, sc_8y = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    Deployment_cost_pod, Deployment_cost_spacex_pod, Deployment_cost_only_spacex = 0, 0, 0
    Retirement_date = Reliability_CubeSat(EPS_redundancy[iteration], 4)
    if Phase_Deployment[iteration] == True:
        R_DSM = []
        for Current_Time in Time_months:
            print(Current_Time)
            R_elem = np.ones(DSM_initial_amount[iteration]) * Reliability_CubeSat(EPS_redundancy[iteration], Current_Time / year_to_month)
            Deployment_Dates = np.arange(relaunch_rate[iteration], (Mission_time * year_to_month) + 1, relaunch_rate[iteration], dtype=int) # Array that gives the dates for phased deployment, in months

            for a in Deployment_Dates: # if the current time is over the deployment date, it adds new elements to the DSM, else continues
                if int(Current_Time) >= int(a):
                    R_elem = np.append(R_elem, np.ones(DSM_relaunch_amount[iteration]) * Reliability_CubeSat(EPS_redundancy[iteration], Current_Time / year_to_month - float(a / year_to_month))).tolist()
                else:
                    continue #sets DSM size and cubesats reliabilities, updating it to the current time
            
            if Retire_sat == True:
                Elem_tobe_filter = np.array(R_elem)
                Elem_filter = Elem_tobe_filter[Elem_tobe_filter >= Retirement_date] 
                if len(Elem_filter) == 0:
                    Elem_filter = np.append(Elem_filter, 0)
                R_elem = Elem_filter

            
            print(R_elem)
            print(type(R_elem))
            print(type(Retirement_date))
            print(Retirement_date)
            R_DSM_partial = 1
            for R_CubeSat in np.arange(len(R_elem)):
                R_DSM_partial *= 1 - R_elem[R_CubeSat]
            R_DSM.append(1 - R_DSM_partial)
            if Current_Time == 6:
                R_DSM_6m = np.round(1 - R_DSM_partial, 4)
                sc_6m = len(R_elem)
            elif Current_Time == 12:
                R_DSM_12m = np.round(1 - R_DSM_partial, 4)
                sc_12m = len(R_elem)
            elif Current_Time == 18:
                R_DSM_18m = np.round(1 - R_DSM_partial, 4)
                sc_18m = len(R_elem)
            elif Current_Time == 24:
                R_DSM_24m = np.round(1 - R_DSM_partial, 4) #gets DSM reliability and appends on the array
                sc_24m = len(R_elem)
            elif Current_Time == 36: # 3 years
                R_DSM_3y = np.round(1 - R_DSM_partial, 4)
                sc_3y = len(R_elem)
            elif Current_Time == 48: # 4 years
                R_DSM_4y = np.round(1 - R_DSM_partial, 4)
                sc_4y = len(R_elem)
            elif Current_Time == 60: # 5 years
                R_DSM_5y = np.round(1 - R_DSM_partial, 4)
                sc_5y = len(R_elem)
            elif Current_Time == 72: # 6 years
                R_DSM_6y = np.round(1 - R_DSM_partial, 4)
                sc_6y = len(R_elem)
            elif Current_Time == 84: # 7 years
                R_DSM_7y = np.round(1 - R_DSM_partial, 4)
                sc_7y = len(R_elem)
            elif Current_Time == 96: # 8 years
                R_DSM_8y = np.round(1 - R_DSM_partial, 4)
                sc_8y = len(R_elem)
    R_simulation.append(R_DSM)
    graph_labels.append('Scenario N°' + str(iteration + 1))


plt.figure(1)

for cont in range(len(R_simulation)):
    plt.plot(Time_months / year_to_month, R_simulation[cont], label=graph_labels[cont])
plt.plot(Time_months / year_to_month, np.ones(len(Time_months)) * 0.9, 'r--')
plt.xlabel('Time (years)')
plt.ylabel('Reliability of the DSM (-)')
plt.legend()
plt.grid(True)
plt.show()