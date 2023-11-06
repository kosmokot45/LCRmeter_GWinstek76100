import numpy as np


def plotModelVoit(r1, r2, c1, c2, steps):
    z1, z2 = [], []

    rs = [r1, r2]

    for r in rs:
        for step in steps:
            w = 2 * np.pi * step
            # z1.append(r1 + (r2/(1+((w**2)*(c**2)*(r2**2)))))
            # z2.append((w*c*(r2**2))/(1+((w**2)*(c**2)*(r2**2))))

            z1.append(r/(w**2 + 1))
            z2.append()

    rez = sum(ri/(pow(w)+1))

    powZ = np.sqrt(np.power(z1, 2)+np.power(z2, 2))
    return {'z1': z1, 'z2': z2, 'powZ': powZ}
