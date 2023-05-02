# import re

# def reinout(stroka):
#     print(stroka)
#     trueValueR = float(stroka[2:10]) * 10 ** float(stroka[11:14])
#     trueValueX = float(stroka[15:23]) * 10 ** float(stroka[24:27])
#     return trueValueR, trueValueX


# if __name__ == '__main__':
#     stroka = "b'+4.11660e+02,-4.54095e+02,OUT ,AUX-OK,NG\\n'"
#     valueR = float(stroka[2:10])
#     multR = float(stroka[11:14])
#     trueValueR = valueR*10**multR
#     valueX = stroka[15:23]

#     ololo = reinout(stroka)
#     print(ololo)

def reinout(measData):
    trueValueR = float(measData[2:10]) * 10 ** float(measData[11:14])
    trueValueX = float(measData[15:23]) * 10 ** float(measData[24:27])
    return trueValueR, trueValueX

def main():
    stroka = "b'+4.11660e+02,-4.54095e+02,OUT ,AUX-OK,NG\\n'"
    valueR = float(stroka[2:10])
    multR = float(stroka[11:14])
    trueValueR = valueR*10**multR
    valueX = stroka[15:23]

    ololo = reinout(stroka)
    print(ololo)
    freq()

def freq(self):
    command = 'FREQ ' + str(self.freqStop)
    command = bytes(command, 'UTF-8')
    self.ser.write(command)

def freq():
    command = 'FREQ ' + str(1000)
    print(command)
    command = bytes(command, 'UTF-8')
    print(command)

if __name__ == '__main__':
    main()
    

