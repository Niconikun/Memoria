from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from csv import writer

print('--------------------------------------------------------------------------------')
print('////////////////////////////////        //////  /////          /                ')
print('  ************************************  ******  ***** **       ***')
print('   ************************************ ******  ***** *****    */****')
print('                                 *************  ***** *******   *******')
print('                ****************/****** ******  *****    *******  ********')
print('                *********************   ******  *****      ********  *******')
print('                                                              **/****   *******')
print('                                                                *******   ******')
print('                                                                   ****      ***')
print('                                                                     ,*        *')
print('--------------------------------------------------------------------------------')
print('Bienvenido de nuevo')
print('Programa creado por: Nicolás Sepúlveda')
print('Para Memoria de Título')
print('--------------------------------------')
print()
print()
print('--------------------------------------------------------------------------------')
R_tot = []
masa = []
volumen = []
costo = []
ciclo_et = ''
label = []
while ciclo_et != 'n' or ciclo_et != 'N':

    EPS_red = ''
    b_inicio = ''
    a_inicio = ''

    while EPS_red != 'y' or EPS_red != 'Y' or EPS_red != 'n' or EPS_red != 'N':
        EPS_red = input('EPS posee redundancia? (y/n): ')
        if EPS_red == 'y' or EPS_red == 'Y':
            EPS_red = True
            break
        elif EPS_red == 'n' or EPS_red == 'N':
            EPS_red = False
            break
        else:
            print('ERROR. Lo ingresado no es correcto, por favor intente nuevamente.')
    print('----------------------------------------------------------')
    ctd_sat_min = int(input('¿Cuál es la cantidad de satélites mínimos que debe componer el cluster? Ingrese un '
                            'número: '))
    print('----------------------------------------------------------')
    ctd_sat_ini = int(input('¿Cuál es la cantidad de satélites a comenzar? Ingrese un número: '))
    print('----------------------------------------------------------')

    Mission_time = int(input('¿Cuánto dura la misión? Ingrese un número: '))
    print('----------------------------------------------------------')

    while a_inicio != 'y' or a_inicio != 'Y' or a_inicio != 'n' or a_inicio != 'N':
        a_inicio = input('¿Despliegue en Fase? (y/n): ')
        print('----------------------------------------------------------')
        if a_inicio != 'y' and a_inicio != 'Y':
            from Reliability import no_phase

            x, R_sys, masa_d, volumen_d, costo_d = no_phase(EPS_red, ctd_sat_min, ctd_sat_ini, Mission_time)
            tasa_gen = 0
            ctd_sat_rel = 0
            break
        else:
            ctd_sat_rel = int(input('¿Cuál es la cantidad de satélites a relanzar? Ingrese un número: '))
            print('----------------------------------------------------------')
            tasa_gen = int(input('¿Cuántas veces se vuelven a lanzar los CubeSats por año? Ingrese un número: '))
            print('----------------------------------------------------------')
            from Reliability import Reliability

            x, R_sys, masa_d, volumen_d, costo_d = Reliability(EPS_red, ctd_sat_min, ctd_sat_ini, ctd_sat_rel, tasa_gen, Mission_time)
            break
    ciclo_et = input('¿Quieres realizar otra configuración? (y/n): ')
    if ciclo_et == 'n' or ciclo_et == 'N':
        print('----------------------------------------------------------')
        break
    else:
        print('----------------------------------------------------------')
        R_tot.append(R_sys)
        masa.append(masa_d)
        volumen.append(volumen_d)
        costo.append(costo_d)
        label.append('EPS_red: ' + str(EPS_red) + ', min: ' + str(ctd_sat_min) + ', ini: ' + str(ctd_sat_ini) + ', '
                                                                                                                'rel:'
                                                                                                                ' ' +
                     str(ctd_sat_rel) + ',tasa: ' + str(tasa_gen))
        continue

R_tot.append(R_sys)
masa.append(masa_d)
volumen.append(volumen_d)
costo.append(costo_d)

with open('data.csv', 'a') as file:
    writer_object = writer(file)
    writer_object.writerow([ctd_sat_min, ctd_sat_ini, ctd_sat_rel, tasa_gen])
    writer_object.writerow([R_tot])
    writer_object.writerow([masa])
    writer_object.writerow([volumen])
    writer_object.writerow([costo])
    writer_object.writerow([])
    file.close()

label.append('EPS_red: ' + str(EPS_red) + ', min: ' + str(ctd_sat_min) + ', ini: ' + str(ctd_sat_ini) + ', rel: ' + str(ctd_sat_rel) + ', tasa: ' + str(tasa_gen))

plt.figure(1)

for cont in range(len(R_tot)):
    plt.plot(x, R_tot[cont], label=label[cont])

plt.xlabel('Tiempo (años)')
plt.ylabel('Confiabilidad (-)')
plt.legend()
plt.grid(True)

fig = plt.figure(2, figsize=(12, 10))
ax = fig.add_subplot(111, projection=Axes3D.name)
ax.set_ylabel('Masa Disponible para Payload (g)')
ax.set_zlabel('Volumen Disponible para Payload (U)')
ax.set_xlabel('Costo $USD')
ax.view_init(20, -120)

for count in range(len(masa)):
    ax.scatter(costo[count], masa[count], volumen[count], 'o', label=label[count])

fig.legend()
plt.show()
