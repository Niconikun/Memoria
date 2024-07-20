import math
from decimal import Decimal
from itertools import cycle
from random import Random
from shutil import get_terminal_size
from threading import Thread
from time import sleep
import numpy as np
import scipy as sp


def save_data_to_txt(data, filename):
    """Saves the given data to a .txt file."""
    with open(filename, "w") as file:
        file.write(data)

def read_data_from_txt(filename="data.txt"):
    """Reads data from a .txt file and returns it as a string."""
    with open(filename, "r") as file:
        data = file.read()
    return data

# Example usage:

t = np.linspace(0, 2, 100)

mu = [15.4, 11.5, 13.7, 14.3, 14.3, 9.4]
sigma = [10, 8.39, 9.79, 9.21, 9.21, 8.18]
theta = [2.6, 8.1, 2.6, 2.7, 2.7, 2.9]
nu = [9.1e-5, 0.0167, 8.3e-5, 0.00011, 0.00011, 0.00011]
counter = 4

for i in np.arange(100):
    print(str(t[i]) + ", " + str(sp.stats.lognorm.sf(t[i], sigma[counter], scale=np.exp(mu[counter])) * sp.stats.gompertz.sf(t[i], nu[counter] / theta[counter], scale=theta[counter])))
#save_data_to_txt(str(data_to_save), str(counter) + ".txt")

# Read the saved data back
#read_data = read_data_from_txt()
#print("Read data:", read_data)