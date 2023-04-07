import pandas as pd


def Env_tradespace(EPS_red, CubeSt_Tipo, sat_ctd_total):
    Data = pd.read_csv("Datos Proveedores Subsistemas.csv", sep=';')
    data = Data[Data[CubeSt_Tipo].isin(['yes'])]
    mm_to_U_conv = 1000000
    broker_data = {'1U': 70000, '3U': 145000, '6U': 295000}

    if CubeSt_Tipo == '1U':

        isis_data = data[data['Nombre'].isin(['ISISPACE'])].reset_index()  # tiene EPS
        enduro_data = data[data['Nombre'].isin(['Endurosat'])].reset_index()  # tiene EPS

        if not EPS_red:
            masa_d = [isis_data._get_value(0, 'Masa')] + [enduro_data._get_value(0, 'Masa')]
            volumen_d = [isis_data._get_value(0, 'Volumen')] + [enduro_data._get_value(0, 'Volumen')]
            costo_d = [isis_data._get_value(0, 'Costo') * sat_ctd_total * broker_data.get(CubeSt_Tipo)] + \
                      [enduro_data._get_value(0, 'Costo') * sat_ctd_total * broker_data.get(CubeSt_Tipo)]

        else:

            masa_d = [isis_data._get_value(0, 'Masa') - isis_data._get_value(1, 'Masa')] + \
                     [enduro_data._get_value(0, 'Masa') - enduro_data._get_value(1, 'Masa')]

            volumen_d = [isis_data._get_value(0, 'Volumen') - isis_data._get_value(1, 'Volumen') / mm_to_U_conv] + \
                        [enduro_data._get_value(0, 'Volumen') - enduro_data._get_value(1, 'Volumen') / mm_to_U_conv]

            costo_d = [(isis_data._get_value(0, 'Costo') + isis_data._get_value(1,
                                                                                'Costo')) * sat_ctd_total * broker_data.get(
                CubeSt_Tipo)] + \
                      [(enduro_data._get_value(0, 'Costo') + enduro_data._get_value(1,
                                                                                    'Costo')) * sat_ctd_total * broker_data.get(
                          CubeSt_Tipo)]

    elif CubeSt_Tipo == '3U':
        isis_data = data[data['Nombre'].isin(['ISISPACE'])].reset_index()  # tiene EPS
        orb_data = data[data['Nombre'].isin(['OrbAstro'])].reset_index()  # tiene EPS
        enduro_data = data[data['Nombre'].isin(['Endurosat'])].reset_index()  # tiene EPS

        if not EPS_red:
            masa_d = [isis_data._get_value(0, 'Masa')] + [orb_data._get_value(0, 'Masa')] + \
                     [enduro_data._get_value(0, 'Masa')]
            volumen_d = [isis_data._get_value(0, 'Volumen')] + [orb_data._get_value(0, 'Volumen')] + \
                        [enduro_data._get_value(0, 'Volumen')]
            costo_d = [isis_data._get_value(0, 'Costo') * sat_ctd_total * broker_data.get(CubeSt_Tipo)] + \
                      [orb_data._get_value(0, 'Costo') * sat_ctd_total * broker_data.get(CubeSt_Tipo)] + \
                      [enduro_data._get_value(0, 'Costo') * sat_ctd_total * broker_data.get(CubeSt_Tipo)]

        else:

            masa_d = [isis_data._get_value(0, 'Masa') - isis_data._get_value(1, 'Masa')] + \
                     [orb_data._get_value(0, 'Masa') - orb_data._get_value(1, 'Masa')] + \
                     [enduro_data._get_value(0, 'Masa') - enduro_data._get_value(1, 'Masa')]

            volumen_d = [isis_data._get_value(0, 'Volumen') - isis_data._get_value(1, 'Volumen') / mm_to_U_conv] + \
                        [orb_data._get_value(0, 'Volumen') - orb_data._get_value(1, 'Volumen') / mm_to_U_conv] + \
                        [enduro_data._get_value(0, 'Volumen') - enduro_data._get_value(1, 'Volumen') / mm_to_U_conv]

            costo_d = [(isis_data._get_value(0, 'Costo') + isis_data._get_value(1,
                                                                                'Costo')) * sat_ctd_total * broker_data.get(
                CubeSt_Tipo)] + \
                      [(orb_data._get_value(0, 'Costo') + orb_data._get_value(1,
                                                                              'Costo')) * sat_ctd_total * broker_data.get(
                          CubeSt_Tipo)] + \
                      [(enduro_data._get_value(0, 'Costo') + enduro_data._get_value(1,
                                                                                    'Costo')) * sat_ctd_total * broker_data.get(
                          CubeSt_Tipo)]

    elif CubeSt_Tipo == '6U':

        isis_data = data[data['Nombre'].isin(['ISISPACE'])].reset_index()  # tiene EPS
        orb_data = data[data['Nombre'].isin(['OrbAstro'])].reset_index()  # tiene EPS
        enduro_data = data[data['Nombre'].isin(['Endurosat'])].reset_index()  # tiene EPS

        if not EPS_red:
            masa_d = [isis_data._get_value(0, 'Masa')] + [orb_data._get_value(0, 'Masa')] + \
                     [enduro_data._get_value(0, 'Masa')]
            volumen_d = [isis_data._get_value(0, 'Volumen')] + \
                        [orb_data._get_value(0, 'Volumen')] + \
                        [enduro_data._get_value(0, 'Volumen')]
            costo_d = [isis_data._get_value(0, 'Costo') * sat_ctd_total * broker_data.get(CubeSt_Tipo)] + \
                      [orb_data._get_value(0, 'Costo') * sat_ctd_total * broker_data.get(CubeSt_Tipo)] + \
                      [enduro_data._get_value(0, 'Costo') * sat_ctd_total * broker_data.get(CubeSt_Tipo)]

        else:

            masa_d = [isis_data._get_value(0, 'Masa') - isis_data._get_value(1, 'Masa')] + \
                     [orb_data._get_value(0, 'Masa') - orb_data._get_value(1, 'Masa')] + \
                     [enduro_data._get_value(0, 'Masa') - enduro_data._get_value(1, 'Masa')]

            volumen_d = [isis_data._get_value(0, 'Volumen') - isis_data._get_value(1, 'Volumen') / mm_to_U_conv] + \
                        [orb_data._get_value(0, 'Volumen') - orb_data._get_value(1, 'Volumen') / mm_to_U_conv] + \
                        [enduro_data._get_value(0, 'Volumen') - enduro_data._get_value(1, 'Volumen') / mm_to_U_conv]

            costo_d = [(isis_data._get_value(0, 'Costo') + isis_data._get_value(1,
                                                                                'Costo')) * sat_ctd_total * broker_data.get(
                CubeSt_Tipo)] + \
                      [(orb_data._get_value(0, 'Costo') + orb_data._get_value(1,
                                                                              'Costo')) * sat_ctd_total * broker_data.get(
                          CubeSt_Tipo)] + \
                      [(enduro_data._get_value(0, 'Costo') + enduro_data._get_value(1,
                                                                                    'Costo')) * sat_ctd_total * broker_data.get(
                          CubeSt_Tipo)]

    return masa_d, volumen_d, costo_d
