from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from csv import writer

'''

'''

R_tot = []
masa = []
volumen = []
costo = []
ciclo_et = ''
label = []

while ciclo_et != 'n' or ciclo_et != 'N':

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
            print('ERROR. Lo ingresado no es correcto, por favor intente nuevamente.')
    print('----------------------------------------------------------')
    DSM_min_amount = int(input('¿Cuál es la cantidad de satélites mínimos que debe componer el cluster? Ingrese un '
                            'número: '))
    print('----------------------------------------------------------')
    DSM_initial_amount = int(input('¿Cuál es la cantidad de satélites a comenzar? Ingrese un número: '))
    print('----------------------------------------------------------')

    Mission_time = int(input('¿Cuánto dura la misión? Ingrese un número: '))
    print('----------------------------------------------------------')

    while Phase_Deployment != 'y' or Phase_Deployment != 'Y' or Phase_Deployment != 'n' or Phase_Deployment != 'N':
        Phase_Deployment = input('¿Despliegue en Fase? (y/n): ')
        print('----------------------------------------------------------')
        if Phase_Deployment != 'y' and Phase_Deployment != 'Y':
            from Reliability import no_phase

            x, R_sys = no_phase(EPS_redundancy, DSM_min_amount, DSM_initial_amount, Mission_time)
            relaunch_rate = 0
            DSM_relaunch_amount = 0
            break
        else:
            DSM_relaunch_amount = int(input('¿Cuál es la cantidad de satélites a relanzar? Ingrese un número: '))
            print('----------------------------------------------------------')
            relaunch_rate = int(input('¿Cuántas veces se vuelven a lanzar los CubeSats por año? Ingrese un número: '))
            print('----------------------------------------------------------')
            from Reliability import Reliability

            x, R_sys = Reliability(EPS_redundancy, DSM_min_amount, DSM_initial_amount, DSM_relaunch_amount, relaunch_rate, Mission_time)
            break
    ciclo_et = input('¿Quieres realizar otra configuración? (y/n): ')
    if ciclo_et == 'n' or ciclo_et == 'N':
        print('----------------------------------------------------------')
        break
    else:
        print('----------------------------------------------------------')
        R_tot.append(R_sys)
        label.append('EPS_redundancy: ' + str(EPS_redundancy) + ', min: ' + str(DSM_min_amount) + ', ini: ' + str(DSM_initial_amount) + ', '
                                                                                                                'rel:'
                                                                                                                ' ' +
                     str(DSM_relaunch_amount) + ',tasa: ' + str(relaunch_rate))
        continue

R_tot.append(R_sys)


with open('data.csv', 'a') as file:
    writer_object = writer(file)
    writer_object.writerow([DSM_min_amount, DSM_initial_amount, DSM_relaunch_amount, relaunch_rate])
    writer_object.writerow([R_tot])
    writer_object.writerow([masa])
    writer_object.writerow([volumen])
    writer_object.writerow([costo])
    writer_object.writerow([])
    file.close()

label.append('EPS_redundancy: ' + str(EPS_redundancy) + ', min: ' + str(DSM_min_amount) + ', ini: ' + str(DSM_initial_amount) + ', rel: ' + str(DSM_relaunch_amount) + ', tasa: ' + str(relaunch_rate))

plt.figure(1)

for cont in range(len(R_tot)):
    plt.plot(x, R_tot[cont], label=label[cont])

plt.xlabel('Tiempo (años)')
plt.ylabel('Confiabilidad (-)')
plt.legend()
plt.grid(True)

'''
fig = plt.figure(2, figsize=(12, 10))
ax = fig.add_subplot(111, projection=Axes3D.name)
ax.set_ylabel('Masa Disponible para Payload (g)')
ax.set_zlabel('Volumen Disponible para Payload (U)')
ax.set_xlabel('Costo $USD')
ax.view_init(20, -120)

for count in range(len(masa)):
    ax.scatter(costo[count], masa[count], volumen[count], 'o', label=label[count])


fig.legend()
'''
plt.show()
