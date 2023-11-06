import numpy as np


def plotModelRandls(r1, r2, c, steps):
    z1, z2 = [], []

    for step in steps:
        w = 2 * np.pi * step
        z1.append(r1 + (r2/(1+((w**2)*(c**2)*(r2**2)))))
        z2.append((w*c*(r2**2))/(1+((w**2)*(c**2)*(r2**2))))

    powZ = np.sqrt(np.power(z1, 2)+np.power(z2, 2))
    return {'z1': z1, 'z2': z2, 'powZ': powZ}
