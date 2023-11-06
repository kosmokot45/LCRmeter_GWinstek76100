from time import sleep
from numpy import geomspace
from main_utils import write_to_json

d = {1: 1}
write_to_json(d)


def autotest_each_freqs(serial):
    ser = serial
    result_dict = {}
    freqs = [10, 100000, 50]

    logSteps = geomspace(freqs[0], freqs[1], freqs[2])

    for freq in logSteps:
        tryResultX: list[float] = []
        tryResultR: list[float] = []
        Q = 200
        for step in range(Q):
            tx = bytes(f'FREQ {str(freq)}', 'UTF-8')
            ser.write(tx)

            sleep(0.5)

            ser.write(b'FETCH?')

            text = ser.readline()
            # print(text)

            result = reInOut(text)
            tryResultX.append(result[1])
            tryResultR.append(result[0])
        result_dict[f'{str(freq)}'] = {
            'X': tryResultX,
            'R': tryResultR,
        }

    write_to_json(result_dict)


def reInOut(stroka: str):
    # print(stroka)
    trueValueR = float(stroka[0:8]) * 10 ** float(stroka[9:12])
    lcdR = stroka[0:12]
    trueValueX = float(stroka[13:21]) * 10 ** float(stroka[22:25])
    lcdX = stroka[13:25]
    return trueValueR, trueValueX, lcdR, lcdX
