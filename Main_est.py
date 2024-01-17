from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from csv import writer

'''
This code is the one to be run. This is the file where the inputs are set and the iterations run
based on the user's desire. The inputs define the parameters of the DSM and simulation, as well as
outputing the Reliability graphs.
---------------------------------
INPUTS
Define variables

'''

'''Empty arrays and strings'''
R_simulation = []
masa = []
volumen = []
costo = []
iteration = ''
graph_labels = []

while iteration != 'n' or iteration != 'N':

    EPS_redundancy = ''
    Phase_Deployment = ''

    while EPS_redundancy != 'y' or EPS_redundancy != 'Y' or EPS_redundancy != 'n' or EPS_redundancy != 'N':
        EPS_redundancy = input('EPS posee redundancia? (y/n): ')
        if EPS_redundancy == 'y' or EPS_redundancy == 'Y':
            EPS_redundancy = True
            break
        elif EPS_redundancy == 'n' or EPS_redundancy == 'N':
            EPS_redundancy = False
            break
        else:
            print('ERROR. Please try again.')
    print('----------------------------------------------------------')
    DSM_min_amount = int(input('What is the minimal amount of CubeSats the DSM is composed of? Enter an integer: '))
    print('----------------------------------------------------------')
    DSM_initial_amount = int(input('What is the amount of CubeSats the DSM begins on the first batch? Enter an integer: '))
    print('----------------------------------------------------------')

    Mission_time = int(input('How much time does the mission last? Enter an integer: '))
    print('----------------------------------------------------------')

    while Phase_Deployment != 'y' or Phase_Deployment != 'Y' or Phase_Deployment != 'n' or Phase_Deployment != 'N':
        Phase_Deployment = input('¿¨Phased Deployment? (y/n): ')
        print('----------------------------------------------------------')
        if Phase_Deployment != 'y' and Phase_Deployment != 'Y':
            from Reliability import no_phase

            Time_years, R_DSM = no_phase(EPS_redundancy, DSM_min_amount, DSM_initial_amount, Mission_time)
            relaunch_rate = 0
            DSM_relaunch_amount = 0
            break
        else:
            DSM_relaunch_amount = int(input('How many CubeSats are to be relaunched? Enter and integer: '))
            print('----------------------------------------------------------')
            relaunch_rate = int(input('How many times per year will the CubeSats be relaunched? Enter an integer: '))
            print('----------------------------------------------------------')
            from Reliability import Reliability

            Time_years, R_DSM = Reliability(EPS_redundancy, DSM_min_amount, DSM_initial_amount, DSM_relaunch_amount, relaunch_rate, Mission_time)
            break
    iteration = input('Do you want to try another DSM setting? (y/n): ')
    if iteration == 'n' or iteration == 'N':
        print('----------------------------------------------------------')
        break
    else:
        print('----------------------------------------------------------')
        R_simulation.append(R_DSM)
        graph_labels.append('EPS_redundancy: ' + str(EPS_redundancy) + ', min: ' + str(DSM_min_amount) + ', ini: ' + str(DSM_initial_amount) + ', '
                                                                                                                'relaunch:'
                                                                                                                ' ' +
                     str(DSM_relaunch_amount) + ',rate: ' + str(relaunch_rate))
        continue

R_simulation.append(R_DSM)

graph_labels.append('EPS_redundancy: ' + str(EPS_redundancy) + ', min: ' + str(DSM_min_amount) + ', ini: ' + str(DSM_initial_amount) + ', relaunch: ' + str(DSM_relaunch_amount) + ', rate: ' + str(relaunch_rate))

plt.figure(1)

for cont in range(len(R_simulation)):
    plt.plot(Time_years, R_simulation[cont], label=graph_labels[cont])

plt.xlabel('Tiempo (años)')
plt.ylabel('Confiabilidad (-)')
plt.legend()
plt.grid(True)
plt.show()
