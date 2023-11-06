import random
import re


def write_to_csv():
    ...


def write_to_json(data_dict: dict[any, any]):  # type: ignore
    print(data_dict)


def normalValue(value: str) -> int:
    try:
        pref = re.findall(r'\D', value)[0]
        if pref == ('k' or 'K'):
            pref = 1000
        elif pref == 'M':
            pref = 1000000
        else:
            pref = 1
    except:
        pref = 1

    freq = int(re.findall(r'\d+', value)[0]) * pref

    return freq


def reInOut(stroka: str):
    # print(stroka)
    trueValueR = float(stroka[0:8]) * 10 ** float(stroka[9:12])
    lcdR = stroka[0:12]
    trueValueX = float(stroka[13:21]) * 10 ** float(stroka[22:25])
    lcdX = stroka[13:25]
    return trueValueR, trueValueX, lcdR, lcdX


def randomAnswer(command: str):
    command = command
    print(command)
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    randOut = [a, b]
    return randOut
