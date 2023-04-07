import math
from decimal import Decimal
from itertools import cycle
from random import Random
from shutil import get_terminal_size
from threading import Thread
from time import sleep
import numpy as np
import scipy as sp

'''
ctd_sat_min ¿Cuál es la cantidad de satélites mínimos que debe componer el cluster?
ctd_sat_ini ¿Cuál es la cantidad de satélites a comenzar?
ctd_sat_rel ¿Cuál es la cantidad de satélites a relanzar?
tasa_gen ¿Cuántas veces se vuelven a lanzar los CubeSats por año?
'''


class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


if __name__ == "__main__":
    with Loader("Ejecutando..."):
        for i in range(10):
            sleep(0.25)


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


def dist(EPS_red, x):
    mu = [15.4, 11.5, 13.7, 14.3, 14.3, 9.4]
    sigma = [10, 8.39, 9.79, 9.21, 9.21, 8.18]
    theta = [2.6, 8.1, 2.6, 2.7, 2.7, 2.9]
    nu = [9.1e-5, 0.0167, 8.3e-5, 0.00011, 0.00011, 0.00011]
    rel = 1

    counter: int
    # esto tiene que entregar un número, no un array
    for counter in np.arange(len(mu)):
        if EPS_red and counter == 5:
            rel *= 1 - np.square(
                1 - sp.stats.lognorm.sf(x, sigma[counter], scale=np.exp(mu[counter])) * sp.stats.gompertz.sf(x, nu[
                    counter] / theta[counter], scale=theta[counter]))
        else:
            rel *= sp.stats.lognorm.sf(x, sigma[counter], scale=np.exp(mu[counter])) * sp.stats.gompertz.sf(x, nu[
                counter] / theta[counter], scale=theta[counter])
    return rel


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
    return R_s


def rel_creator(t, tasa_gen, mission_time, sat_ctd_ini, sat_ctd_rel, EPS_red):
    Ans = np.ones(sat_ctd_ini) * dist(EPS_red, t)
    x = np.linspace(0, mission_time, (mission_time * tasa_gen), dtype=str)

    for a in x:
        if Decimal(str(t)) >= Decimal(a) > Decimal('0'):
            Ans = np.append(Ans, np.ones(sat_ctd_rel) * dist(EPS_red, t - float(a)))
        else:
            continue
    return Ans.tolist()


def no_phase(EPS_red, ctd_sat_min, ctd_sat_ini, Mission_time):
    x = np.linspace(0, Mission_time, Mission_time * 365)

    loader = Loader(desc='Espere un momento...', end='Terminado!').start()
    R_sys = []
    for t in x:
        R_elem = np.ones(ctd_sat_ini) * dist(EPS_red, t)
        R_sys.append(rel_builder(R_elem, ctd_sat_min))

    loader.stop()

    from Env_tradespace import Env_tradespace
    masa = []
    volumen = []
    costo = []

    for Tip in ['1U', '3U', '6U']:
        masa.extend(Env_tradespace(EPS_red, Tip, len(R_elem))[0])
        volumen.extend(Env_tradespace(EPS_red, Tip, len(R_elem))[1])
        costo.extend(Env_tradespace(EPS_red, Tip, len(R_elem))[2])

    return x, R_sys, masa, volumen, costo


def Reliability(EPS_red, ctd_sat_min, ctd_sat_ini, ctd_sat_rel, tasa_gen):

    Mission_time = 7
    year_to_day = 365
    x = np.linspace(0, Mission_time, Mission_time * year_to_day)

    loader = Loader(desc='Espere un momento...', end='Terminado!').start()
    R_sys = []
    for t in x:
        R_elem = rel_creator(t, tasa_gen, Mission_time, ctd_sat_ini, ctd_sat_rel, EPS_red)
        R_sys.append(rel_builder(R_elem, ctd_sat_min))
    loader.stop()

    from Env_tradespace import Env_tradespace
    masa = []
    volumen = []
    costo = []

    for Tip in ['1U', '3U', '6U']:
        masa.extend(Env_tradespace(EPS_red, Tip, len(R_elem))[0])
        volumen.extend(Env_tradespace(EPS_red, Tip, len(R_elem))[1])
        costo.extend(Env_tradespace(EPS_red, Tip, len(R_elem))[2])

    return x, R_sys, masa, volumen, costo

